from manim import *
import math

class RectangleDiracDistribution(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 10, 2],
            axis_config={"color": BLUE},
        )

        # Function for the Gaussian distribution
        def rectangle(x, epsilon=1):
            value = 0.0 if math.abs(x) > epsilon/2.0 else 1.0/epsilon
            return value

        # Labels for the axes
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # Initial standard deviation and its decrease rate
        epsilon = 1
        epsilon_reduction_factor = 0.75

        # Initial Gaussian curve
        graph = axes.plot(lambda x: rectangle(x, epsilon=epsilon), color=RED)
        #graph_label = axes.get_graph_label(graph, label="\\epsilon = 1.0")

        function_label = Tex(r"$f(x) = \frac{1.0}{\sqrt{2 \pi \epsilon}}\exp{-\frac{x^2}{2\epsilon}}$").move_to(axes.c2p(2, 8))
        graph_label = Tex(r"$\epsilon = 1.0$").next_to(function_label, DOWN)

        self.play(Create(axes), Write(labels), Create(graph), Write(function_label), Write(graph_label))
        self.wait(1)

        # Iteratively reduce the standard deviation to 'narrow' the Gaussian curve
        for _ in range(25):
            epsilon *= epsilon_reduction_factor
            new_graph = axes.plot(lambda x: rectangle(x, epsilon=epsilon), color=RED)
            new_graph_label = Tex(f"$\\epsilon = {epsilon:.4f}$").next_to(function_label, DOWN)

            # Adjust x_range dynamically based on epsilon
            new_x_range = max(30 * epsilon, 0.1)  # Example of dynamic adjustment
            axes.x_range = [-new_x_range, new_x_range, axes.x_range[2]]
            axes.update()

            self.play(
                ReplacementTransform(graph, new_graph),
                ReplacementTransform(graph_label, new_graph_label),
                run_time=0.1
            )
            graph = new_graph
            graph_label = new_graph_label

            #self.wait(0.1)

        self.wait(2)  # Hold the final state for 2 seconds before exiting


