from manim import *

class ConvolutionAnimation(Scene):
    def construct(self):
        # Setup axes for the original functions
        axes_top = Axes(
            x_range=[-4, 4],
            y_range=[0, 2],
            axis_config={"color": BLUE},
            x_length=8,
            y_length=2,
            tips=False,
        ).to_edge(UP, buff=0.5)

        # Setup axes for the convolution result
        axes_bottom = Axes(
            x_range=[-4, 4],
            y_range=[0, 2],
            axis_config={"color": BLUE},
            x_length=8,
            y_length=2,
            tips=False,
        ).to_edge(DOWN, buff=0.5)

        # First rectangle (stationary)
        rect1 = Rectangle(width=1, height=1, color=RED, fill_opacity=0.5).move_to(axes_top.c2p(0, 0.5))

        # Second rectangle (moving)
        rect2 = Rectangle(width=1, height=1, color=GREEN, fill_opacity=0.5).move_to(axes_top.c2p(-4, 0.5))

        # Convolution result (initially invisible)
        

        self.add(axes_top, axes_bottom, rect1, rect2)
        conv_result = None
        new_conv_result = None
        for i in range(80):
            new_pos = axes_top.c2p(-4+i/10.0, 0.5)
            self.play(ApplyMethod(rect2.move_to, new_pos), run_time=0.01)
            if i > 30:
                poly_points = []
                poly_points.append(axes_bottom.c2p(-1, 0))
                
                # is it still rising?
                if i < 40:
                    poly_points.append(
                       axes_bottom.c2p(
                            -4 + i/10, 1-(4 - i/10)
                        )
                    )
                    poly_points.append(
                        axes_bottom.c2p(
                            -4 + i/10, 0
                        )
                    )
                # nope, it's falling again
                else:
                    poly_points.append(
                        axes_bottom.c2p(
                            0, 1
                        )
                    )

                    if i < 50:
                        poly_points.append(
                            axes_bottom.c2p(
                                -4 + i/10, 1+(4-i/10)
                            )
                        )
                        poly_points.append(
                            axes_bottom.c2p(
                                -4 + i/10, 0
                            )
                        )
                    else:
                        poly_points.append(
                            axes_bottom.c2p(
                                1,0
                            )
                        )


                new_conv_result = Polygon(*poly_points)
                if conv_result is None:
                    conv_result = new_conv_result
                    self.add(conv_result)
                    print("conv_result was 1")
                else:
                    self.play(Transform(conv_result, new_conv_result), run_time=0.001)
                    conv_result = new_conv_result

            ##self.play(rect2.animate(move_to(axes_top.c2p(-4+i/10.0, 0.5))))


        # Animate the moving rectangle and the convolution result
        #self.play(rect2.animate.shift(RIGHT * 6), rate_func=linear, run_time=4)
        self.play(conv_result.animate.set_opacity(1), run_time=0.1)  # Make convolution result visible
        self.wait(1)