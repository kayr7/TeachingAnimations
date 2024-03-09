#%%manim -qh -v WARNING NeuralNetPredict
from manim import *
import numpy as np
from PIL import Image
import requests



def create_textbox(color, string):
    result = VGroup() # create a VGroup
    box = Rectangle(  # create a box
        height=0.5, width=1, fill_color=color, 
        fill_opacity=0.5, stroke_color=color
    )
    text = Text(string, font_size=20).move_to(box.get_center()) # create text
    result.add(box, text) # add both objects to the VGroup
    return result


#def create_decoder_box(color):
#   box = Rectangle(
#      height=2, width=1, fill_color=color,
#      fill_opacity=0.5, stroke_color=color
#   )
#   return box

def create_decoder_box(color):
    result = VGroup() # create a VGroup
    box = Rectangle(  # create a box
        height=2., width=1, fill_color=color, 
        fill_opacity=0.5, stroke_color=color
    )
    text = Text("Decoder Blocks", font_size=15).rotate(PI/2).move_to(box.get_center()) # create text
    result.add(box, text) # add both objects to the VGroup
    return result


def generate_layer_connections(source_layer: VGroup, target_layer: VGroup, unmasked: int, arrow_width=0.5):
    arrow_group = VGroup()

    for j, target_node in enumerate(target_layer):
       if j >= unmasked:
          continue
       for i, source_node in enumerate(source_layer[:j+1]):
          if i >= unmasked:
             continue
          arrow = Line(
            source_node.get_top(),
            target_node.get_bottom(),
            stroke_width=arrow_width,
          )
          arrow_group.add(arrow)

    circle_group = VGroup()
    for l in arrow_group:
            circle = Circle(radius=0.15, color=ORANGE).move_to(l.get_start())
            circle_group.add(circle)

    return (arrow_group, circle_group)





class Decoder(Scene):


  def animate_circle_along_line(self, lines, circle_group, run_time):
     
     circle_animations=[]
     for i, l in enumerate(lines):
        circle_animations.append(circle_group[i].animate.move_to(l.get_end()))

    
  
     #self.play(*circle_animations, run_time=2.0)
     return (circle_animations, circle_group)
     #self.play(FadeOut(*circle_group))



  def forward_pass(self, inputs, hidden, outputs, unmasked, text, run_time):
    first_arrows, circle_group = generate_layer_connections(inputs, hidden, unmasked=unmasked)
    self.play(FadeIn(first_arrows), FadeIn(circle_group), run_time=run_time/2.)

    (animation, circle_group) = self.animate_circle_along_line(first_arrows, circle_group, run_time=run_time)
    self.play(*animation, run_time=run_time)
    #self.play(FadeOut(first_arrows))

    hidden_activation = [FadeOut(first_arrows), FadeOut(circle_group)]
    for idx, h in enumerate(hidden):
       if idx >= unmasked:
          continue
       hidden_activation.append(h.animate.set_color(ORANGE))

    self.play(*hidden_activation, run_time=run_time/2.0)

    (second_arrows, circle_group) = generate_layer_connections(hidden, outputs, unmasked=unmasked)
    self.play(FadeIn(second_arrows), FadeIn(circle_group), run_time=run_time/2.)

    (animation, circle_group) = self.animate_circle_along_line(second_arrows, circle_group, run_time=run_time)
    self.play(*animation, run_time=run_time)


    output_animation = [FadeOut(second_arrows), FadeOut(circle_group)]
    for idx, out in enumerate(outputs):
       if idx >= unmasked:
          continue
       output_animation.append(Transform(out, 
                               create_textbox(BLUE, text[idx+1]).move_to(out.get_center())))

    self.play(*output_animation, run_time=run_time/2.0)                         





  def construct(self):
    CONFIG={
		"camera_config":{"background_color":"#475147"}
	}

    input_text = ["<BOS>", "this", "is", "a", "slide", "for", "a", "gpt", "decoder", "run", "<EOS>"]
    prompt_length = 5

    inputs = VGroup(*[create_textbox(BLUE, s if idx < prompt_length else "") for (idx, s) in enumerate(input_text[:-1])])

    inputs.arrange(RIGHT)
    inputs.shift(2*DOWN)
    self.add(inputs)

    decoder_boxes = VGroup(*[create_decoder_box(GRAY) for _ in input_text[:-1]])
    decoder_boxes.arrange(RIGHT)
    self.add(decoder_boxes)


    output_text = VGroup(*[create_textbox(GREEN, "") for _ in input_text[:-1]])
    output_text.arrange(RIGHT)
    output_text.shift(2*UP)
    self.add(output_text)

    #self.wait()
    #generate_layer_connections(inputs, hidden, unmasked=5)

    unmasked = 5
    for unmasked in range(5, 11):
        if unmasked < 6:
           run_time = 2.0
        elif unmasked == 6:
           run_time = 1.0
        else:
           run_time = 0.7

        self.forward_pass(inputs, decoder_boxes, output_text, unmasked, input_text, run_time=run_time)

        reset_hidden = []
        for idx, h in enumerate(decoder_boxes):
            if idx >= unmasked:
                continue
            reset_hidden.append(Transform(h, 
                                create_decoder_box(GRAY).move_to(h.get_center())))
        
        new_box = create_textbox(BLUE, input_text[unmasked]).move_to(output_text[unmasked-1].get_center())


        if unmasked < len(input_text)-1:
            reset_hidden.append(FadeOut(inputs[unmasked]))
            reset_hidden.append(Transform(
                new_box,
                create_textbox(BLUE, input_text[unmasked]).move_to(inputs[unmasked].get_center())
            ))
            inputs[unmasked] = new_box
                                    
        
        self.play(*reset_hidden, run_time=run_time/2.0)
       