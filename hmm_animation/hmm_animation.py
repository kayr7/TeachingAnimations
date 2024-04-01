from manim import *

SCALE = 0.5


class HMM:
    def __init__(self, scene, phone):
        self.scene = scene
        self.phone = phone
        self.states = self.create_states()
        self.transitions = []
        self.create_transitions()

    def create_states(self):
        # Create circles for beginning, middle, and end states
        states = {}
        for index, part in enumerate(["-b", "-m", "-e"]):
            state = Circle(color=BLUE, fill_opacity=1).scale(0.5 * SCALE)
            # Position states horizontally with some space
            state.shift(RIGHT * 2 * index * SCALE)
            # Scale the text down to fit better in the circle
            text = Text(f"{self.phone}{part}", font_size=18).move_to(state.get_center())
            self.scene.add(state, text)
            states[part] = {
                "state": state,
                "label": text,
            }
        return states

    def create_transitions(self):
        # Modified to include tagging arrows
        transitions_info = [
            ("-b", "-b"),
            ("-b", "-m"),
            ("-m", "-m"),
            ("-m", "-e"),
            ("-e", "-e"),
        ]
        for part1, part2 in transitions_info:
            start_state = self.states[part1]["state"]
            end_state = self.states[part2]["state"]
            if part1 == part2:  # Transition to itself
                loop = CurvedArrow(
                    start_state.get_top() + LEFT * 0.2 * SCALE,
                    start_state.get_top() + RIGHT * 0.2 * SCALE,
                    angle=-TAU / 2,
                    stroke_width=2 * SCALE,  # Adjust stroke width if needed
                    tip_length=0.15 * SCALE,
                )
                self.scene.add(loop)
                # Tag the arrow with a tuple of (start, end)
                self.transitions.append((loop, (part1, part2)))
            else:
                arrow = Arrow(
                    start=start_state.get_right(), end=end_state.get_left(), buff=0.1
                )
                self.scene.add(arrow)
                # Tag the arrow with a tuple of (start, end)
                self.transitions.append((arrow, (part1, part2)))


class ExtendedHMMAnimation(Scene):
    def construct(self):
        # Position where the final word will appear
        word_position = UP * 3 * SCALE + LEFT * 4 * SCALE
        word_parts = []  # List to keep track of moved labels

        # Define the phonemes and their sequences
        phones = ["c", "a", "t"]
        sequences = [["-b", "-m", "-e"], ["-b", "-m", "-m", "-e"], ["-b", "-m", "-e"]]
        hmms = []

        # Create and display all HMMs from the start
        start_positions = [
            LEFT * 9 * SCALE,
            LEFT * 2 * SCALE,
            RIGHT * 5 * SCALE,
        ]  # Starting positions for "c", "a", "t"
        for idx, phone in enumerate(phones):
            # Create HMM instance
            hmm = HMM(self, phone)
            # Adjust position of HMM states and transitions
            for part, info in hmm.states.items():
                info["state"].shift(start_positions[idx])
                info["label"].shift(start_positions[idx])
            for arrow, _ in hmm.transitions:
                arrow.shift(start_positions[idx])
            hmms.append(hmm)

        for idx, hmm in enumerate(hmms[:-1]):  # Loop through hmms except the last one
            end_state_of_current_hmm = hmm.states["-e"]["state"]
            start_state_of_next_hmm = hmms[idx + 1].states["-b"]["state"]

            # Calculate start and end points for the arrow
            start_point = end_state_of_current_hmm.get_right()
            end_point = start_state_of_next_hmm.get_left()

            # Create and add the arrow
            transition_arrow = Arrow(start=start_point, end=end_point, buff=0.1)
            self.add(transition_arrow)

        # Animate each HMM's states in sequence
        for idx, (hmm, sequence) in enumerate(zip(hmms, sequences)):
            for i, state in enumerate(sequence):
                current_state = hmm.states[state]
                # Highlight the current state
                self.play(current_state["state"].animate.set_fill(BLUE, opacity=0.5))
                self.play(current_state["state"].animate.set_fill(BLUE, opacity=1.0))

                # Move the label up to form the word
                state_text = current_state["label"].copy()
                target_position = word_position + RIGHT * len(word_parts) * 0.8 * SCALE
                self.play(state_text.animate.move_to(target_position))
                word_parts.append(state_text)

                if i < len(sequence) - 1:
                    next_state_id = sequence[i + 1]
                    # Animate the transition arrow
                    for arrow, (start_id, end_id) in hmm.transitions:
                        if start_id == state and end_id == next_state_id:
                            self.play(Create(arrow), run_time=1)
                            break

                self.wait(0.5)  # Pause before the next transition

        # Gather all parts to form the final word and fade out
        final_word = VGroup(*word_parts)
        self.add(final_word)


class HMMAnimation(Scene):
    def construct(self):
        phone = "/a/"
        hmm = HMM(self, phone)
        word_position = UP * 3 * SCALE  # Position where the final word will appear
        word_parts = []  # List to keep track of moved labels
