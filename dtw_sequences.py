from manim import *

class DTWVisualization(Scene):
    def construct(self):
        # Define the sequences
        X = list(range(17))
        r_k = list(range(15))

        # Convert sequences to strings for display
        X_str = "X = [" + ", ".join(map(str, X)) + "]"
        r_k_str = "r_k = [" + ", ".join(map(str, r_k)) + "]"

        alignments = [
            (0,0),
            (1,0),
            (2,0),
            (2,1),
            (2,2),
            (2,3),
            (2,4),
            (3,5),
            (4,6),
            (4,7),
            (5,8),
            (6,9),
            (7,9),
            (8,9),
            (9,9),
            (10,10),
            (11,11),
            (12,11),
            (13,11),
            (14,12),
            (15,13),
            (16,14),
        ]

        # Create text objects for sequences
        sequence_X = Text(X_str, font_size=24).shift(UP)
        sequence_r_k = Text(r_k_str, font_size=24).shift(DOWN)

        # Display sequences
        #self.play(Write(sequence_X), Write(sequence_r_k))
        #self.wait(1)

        Xs = []
        for x in X:
            x_pos = Text(f"X[{x}]", font_size=18).shift(UP + RIGHT * (x - len(X) / 2) * 0.8)
            Xs.append(x_pos)
            self.play(Write(Xs[-1]), run_time=0.1)

        Rs = []
        for r in r_k:
            r_pos = Text(f"R[{r}]", font_size=18).shift(DOWN + RIGHT * (r - len(r_k) / 2) * 0.7)
            Rs.append(r_pos)
            self.play(Write(Rs[-1]), run_time=0.1)

        # Visualize alignments with thick red bars
        for (x,r) in alignments:
            x_pos = Xs[x].get_center() + DOWN * 0.2
            r_pos = Rs[r].get_center() + UP * 0.2
            # Draw a red line between the elements
            line = Line(x_pos, r_pos, stroke_width=6, color=RED)
            self.play(Create(line), run_time=0.3)

        self.wait(2)
