from manim import *

class WERComputation(Scene):
    def construct(self):
        # Initialize ValueTracker
        upward_shift = UP * 0.5  # Adjust this value as needed
        
        ref = ["", "this", "is", "a", "test"]
        hyp = ["", "his", "is", "a", "best"]

        title = Text("Word Error Rate", font_size=36).to_edge(UP, buff=1).shift(upward_shift)
        ref_subtitle = Text("Ref: " + " ".join(ref[1:]), font_size=24).next_to(title, DOWN, buff=0.5)
        hyp_subtitle = Text("Hyp: " + " ".join(hyp[1:]), font_size=24).next_to(ref_subtitle, DOWN, buff=0.1)
        wer_text = Text("WER = ?", font_size=24).next_to(hyp_subtitle, DOWN, buff=0.5)

        self.add(title, ref_subtitle, hyp_subtitle, wer_text)


        matrix = [[ValueTracker(0) for _ in hyp] for _ in ref]


        # Use a helper function to correctly capture the cell value
        def make_updater(cell):
            return lambda v: v.set_value(cell.get_value())

        data_matrix = [[DecimalNumber(0, num_decimal_places=0).add_updater(make_updater(cell)) for cell in row] for row in matrix]
        col_labels = [Text(label, font_size=24) for label in hyp]  # Exclude the first empty string
        data_matrix.insert(0, col_labels)
        
        data_matrix[0].insert(0, Text('', font_size=24))
        for i, label in enumerate(ref):  # Exclude the first empty string
            data_matrix[i+1].insert(0, Text(label, font_size=24))



        # Create the table
        table = MobjectTable(data_matrix, include_outer_lines=True)
        table.next_to(wer_text, DOWN, buff=1).shift(upward_shift)
        self.add(table)

        # Animate the ValueTracker
        for i, _ in enumerate(ref):
            self.play(matrix[i][0].animate.set_value(i), run_time=0.2)

        for i, _ in enumerate(hyp):
            self.play(matrix[0][i].animate.set_value(i), run_time=0.2)


        def get_cell_mobject(row, col):
            # Directly accessing the cell Mobject from the table
            # Adjust indices as needed, considering header rows/columns
            return table.get_entries()[row * (len(hyp)+1) + col]


        for i in range(1, len(ref)):
            for j in range(1, len(hyp)):

                # Copy value +1 from above
                arrow = Arrow(
                    start=get_cell_mobject(i, j).get_center(), 
                    end=get_cell_mobject(i+1,j).get_center()+(0, 0.3, 0), buff=0, color=BLUE)
                self.add(arrow)
                new_val = matrix[i-1][j].get_value() + 1
                self.play(matrix[i][j].animate.set_value(new_val), run_time=0.5)
                self.remove(arrow)

                # compare with value from left
                arrow = Arrow(
                    start=get_cell_mobject(i+1, j-1).get_center(), 
                    end=get_cell_mobject(i+1,j).get_center()+(-0.3, 0, 0), buff=0, color=BLUE)
                self.add(arrow)
                new_val = matrix[i][j-1].get_value() + 1
                if new_val < matrix[i][j].get_value():
                    self.play(matrix[i][j].animate.set_value(new_val), run_time=0.5)
                else:
                    self.play(arrow.animate.set_color(RED), run_time=0.5)
                self.remove(arrow)
                
                # compare with word itself and replace or accept
                arrow = Arrow(
                    start=get_cell_mobject(i, j-1).get_center(), 
                    end=get_cell_mobject(i+1,j).get_center()+(-0.3, 0.3, 0), buff=0, color=BLUE) 
                
                self.add(arrow)
                new_val = matrix[i-1][j-1].get_value() + (
                        0 if ref[i] == hyp[j] else 1
                    )
                if new_val < matrix[i][j].get_value():
                    self.play(matrix[i][j].animate.set_value(new_val), run_time=0.5)
                else:
                    self.play(arrow.animate.set_color(RED), run_time=0.5)
                self.remove(arrow) 

        # Get the Mobject for the last cell in the table
        last_cell_mobject = get_cell_mobject(len(ref), len(hyp)-1)

        # Change the color of the last cell
        self.play(last_cell_mobject.animate.set_color(GREEN), run_time=0.5)


        last_value = last_cell_mobject.get_value()  # Ensure this is a float or int
        wer_value_text = DecimalNumber(last_value, num_decimal_places=2, font_size=24).move_to(wer_text)

        # Animation to change "?" in "WER = ?" to the last value
        self.play(ReplacementTransform(wer_text, wer_value_text))

        self.wait(1)