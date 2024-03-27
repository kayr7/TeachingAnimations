from manim import *

class SimpleNeuralNetwork(Scene):
    def construct(self):
        # Parameters
        n = 4  # Number of input nodes
        m = 3  # Number of output nodes
        node_radius = 0.2
        layer_spacing = 3
        node_spacing = 1
        target_output_node = 2  # Indexing from 1, adjust for the node j you want to focus on

        # Input nodes
        input_nodes = VGroup(*[
            Circle(radius=node_radius, color=WHITE).shift(LEFT * layer_spacing + DOWN * (node_spacing * (i - (n - 1) / 2)))
            for i in range(n)
        ])
        input_labels = VGroup(*[
            Tex(f"$x_{i+1}$", font_size=24).move_to(input_nodes[i].get_center())
            for i in range(n)
        ])

        # Output nodes
        output_nodes = VGroup(*[
            Circle(radius=node_radius, color=WHITE).shift(RIGHT * layer_spacing + DOWN * (node_spacing * (i - (m - 1) / 2)))
            for i in range(m)
        ])
        output_labels = VGroup(*[
            Text(f"{i+1}", font_size=24).move_to(output_nodes[i].get_center())
            for i in range(m)
        ])

        # Connections to a specific output node (j)
        connections = VGroup(*[
            Line(input_nodes[i].get_center()+RIGHT*0.2, output_nodes[target_output_node - 1].get_center()+LEFT*0.2, color=BLUE)
            for i in range(n)
        ])
        weight_labels = VGroup(*[
            Tex(f"$w_{{{i+1}{target_output_node}}}$", font_size=20).move_to(connections[i].get_center()+UP*0.15)
            for i in range(n)
        ])

        # Drawing
        self.play(Create(input_nodes), Create(output_nodes))
        self.play(Write(input_labels), Write(output_labels))
        self.play(Create(connections))
        self.play(Write(weight_labels))
        self.wait(2)
