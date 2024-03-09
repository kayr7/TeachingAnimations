from manim import *



class SpeechProcessing(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        # Create MObjects for each image
        image1 = ImageMobject("Personalpha.png").scale(0.4)
        image2 = ImageMobject("Microphonealpha.png").scale(0.2)
        image3 = ImageMobject("Laptop2alpha.png").scale(0.4)
        image4 = ImageMobject("speakeralpha.png").scale(0.3)


        # Set initial positions for the images
        image1.move_to(LEFT * 5)
        image2.move_to(ORIGIN + UP)
        image3.move_to(RIGHT * 5)
        image4.move_to(ORIGIN + DOWN)
        
        # Add images to the scene
        self.add(image1, image2, image3, image4)
        
        # Play animation to display the images
        self.wait(1)  # Wait for 1 second to see the initial state


        sound_image = ImageMobject("soundalpha.png").scale(0.1)
        
        sound_image.move_to(image1.get_center())
        self.play(FadeIn(sound_image), duration=0.1)

        new_image_target_position = sound_image.get_center() + UP * 0.6  # Move up by 0.5 units
        self.play(ApplyMethod(sound_image.move_to, new_image_target_position))

        self.play(Rotate(sound_image, angle=-PI/2))



        new_image_target_position = image2.get_center()
        self.play(ApplyMethod(sound_image.move_to, new_image_target_position))


        wave_image = ImageMobject("waveformDoodlealpha.png").scale(0.1)
        wave_image.move_to(sound_image.get_center())

        self.play(Transform(sound_image, wave_image))



        new_image_target_position = image3.get_center() + UP * 0.3
        self.play(ApplyMethod(wave_image.move_to, new_image_target_position))


        abc_image = ImageMobject("ABC.png").scale(0.1)
        abc_image.move_to(wave_image.get_center())
        self.play(Transform(wave_image, abc_image))


        number_image = ImageMobject("123.png").scale(0.1)
        number_image.move_to(abc_image.get_center())
        self.play(Transform(abc_image, number_image))


        wave_image = ImageMobject("waveformDoodlealpha.png").scale(0.1)
        wave_image.move_to(number_image.get_center())
        self.play(FadeIn(wave_image), duration=0.1)

        new_image_target_position = image4.get_center()
        self.play(ApplyMethod(wave_image.move_to, new_image_target_position))



        sound_image = ImageMobject("soundalpha.png").scale(0.1)
        sound_image.rotate(PI/2)   
        sound_image.move_to(wave_image.get_center())
        self.play(Transform(wave_image, sound_image))


        new_image_target_position = image1.get_center() + UP * 0.8
        self.play(ApplyMethod(sound_image.move_to, new_image_target_position))










            