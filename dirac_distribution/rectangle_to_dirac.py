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
        def rectangle(epsilon, axes):
            #p = Polygon(
            #    axes.c2p(-epsilon/2, 0), axes.c2p(-epsilon/2, 1/epsilon),
            #    axes.c2p(epsilon/2, 1/epsilon), axes.c2p(epsilon/2, 0),
            #    color=RED
            #)
            p = [
                Line(axes.c2p(-3, 0), axes.c2p(-epsilon/2, 0), color=RED),
                Line(axes.c2p(-epsilon/2, 0), axes.c2p(-epsilon/2, 1/epsilon), color=RED),
                Line(axes.c2p(-epsilon/2, 1/epsilon), axes.c2p(epsilon/2, 1/epsilon), color=RED),
                Line(axes.c2p(epsilon/2, 1/epsilon), axes.c2p(epsilon/2, 0), color=RED),
                Line(axes.c2p(epsilon/2, 0), axes.c2p(3, 0), color=RED),
            ]
            return p

        # Labels for the axes
        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # Initial standard deviation and its decrease rate
        epsilon = 1
        epsilon_reduction_factor = 0.75

        # Initial Gaussian curve
        graph = rectangle(epsilon, axes)

        function_label = Tex(r"$\delta_\epsilon(x) = \left\{ \begin{array}{ll} 0 & |x| > \frac{\epsilon}{2}\\ \frac{1}{\epsilon} & |x| \leq \frac{\epsilon}{2} \end{array} \right.$").move_to(axes.c2p(2, 8))
        graph_label = Tex(r"$\epsilon = 1.0$").next_to(function_label, DOWN)

        self.play(Create(axes), Write(labels), Create(graph[0]), Create(graph[1]), Create(graph[2]), Create(graph[3]), Create(graph[4]), Write(function_label), Write(graph_label))
        self.wait(1)

        # Iteratively reduce the standard deviation to 'narrow' the Gaussian curve
        for _ in range(10):
            epsilon *= epsilon_reduction_factor
            new_graph =  rectangle(epsilon, axes)
            new_graph_label = Tex(f"$\\epsilon = {epsilon:.4f}$").next_to(function_label, DOWN)

            # Adjust x_range dynamically based on epsilon
            new_x_range = max(30 * epsilon, 0.1)  # Example of dynamic adjustment
            axes.x_range = [-new_x_range, new_x_range, axes.x_range[2]]
            axes.update()

            self.play(
                ReplacementTransform(graph[0], new_graph[0]),
                ReplacementTransform(graph[1], new_graph[1]),
                ReplacementTransform(graph[2], new_graph[2]),
                ReplacementTransform(graph[3], new_graph[3]),
                ReplacementTransform(graph[4], new_graph[4]),
                ReplacementTransform(graph_label, new_graph_label),
                run_time=0.1
            )
            graph = new_graph
            graph_label = new_graph_label

            #self.wait(0.1)

        self.wait(2)  # Hold the final state for 2 seconds before exiting


