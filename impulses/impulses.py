from manim import *

config.background_color = WHITE

class ImpulseFunction(Scene):

    

    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-2, 2, 1],
            y_range=[-0.5, 1.5, 1],
            axis_config={"color": BLACK},
            x_length=8,
            y_length=4
        )

        # Labels for the axes
        labels = axes.get_axis_labels(x_label="x", y_label="y").set_color(BLACK)

        # Create an impulse as a vertical line
                # Add axes, impulse, and label to the scene
        self.play(Create(axes), Write(labels))

        def create_pulse(x, y, axes):
                impulse_position = x
                impulse_height = y
                return Line(
                    start=axes.c2p(impulse_position, 0), 
                    end=axes.c2p(impulse_position, impulse_height),
                    color=RED, stroke_width=6
                )
        
        self.add(create_pulse(-2, 0.2, axes))
        self.add(create_pulse(-1.5, 0.5, axes))
        self.add(create_pulse(-1, 0.3, axes))
        self.add(create_pulse(-0.5, 0.8, axes))
        self.add(create_pulse(0, 1.0, axes))
        self.add(create_pulse(0.5, 1.2, axes)) 
        self.add(create_pulse(1, 0.2, axes))
        self.add(create_pulse(1.5, 0.1, axes)) 
        self.add(create_pulse(2, 0.6, axes))



        self.wait(1)
