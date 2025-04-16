"""
project: manimation
april 16 2025 - XQ - LUMC
testing manim
"""

from manim import *

class NeuralNetwork(Scene):
    def construct(self):
        # Define the number of neurons in each layer
        input_neurons = 4
        hidden_neurons = 5
        output_neurons = 3

        # Create layers as VGroups of circles (neurons) without outer stroke
        input_layer = VGroup(*[Circle(radius=0.3, fill_color=BLUE, fill_opacity=0.8, stroke_width=0) for _ in range(input_neurons)])
        hidden_layer = VGroup(*[Circle(radius=0.3, fill_color=GREEN, fill_opacity=0.8, stroke_width=0) for _ in range(hidden_neurons)])
        output_layer = VGroup(*[Circle(radius=0.3, fill_color=RED, fill_opacity=0.8, stroke_width=0) for _ in range(output_neurons)])

        # Arrange neurons vertically in each layer
        input_layer.arrange(DOWN, buff=0.5)
        hidden_layer.arrange(DOWN, buff=0.5)
        output_layer.arrange(DOWN, buff=0.5)

        # Position layers horizontally
        input_layer.move_to(LEFT * 4)
        hidden_layer.move_to(ORIGIN)
        output_layer.move_to(RIGHT * 4)

        # Create labels for each layer
        input_label = Text("Input Layer").next_to(input_layer, UP)
        hidden_label = Text("Hidden Layer").next_to(hidden_layer, UP)
        output_label = Text("Output Layer").next_to(output_layer, UP)

        # Create connections (arrows) between layers
        input_to_hidden_arrows = VGroup()
        input_to_hidden_paths = []  # Store paths for glow animation
        for input_neuron in input_layer:
            for hidden_neuron in hidden_layer:
                arrow_listener = Arrow(input_neuron.get_right(), hidden_neuron.get_left(), buff=0.1, color=WHITE)
                input_to_hidden_arrows.add(arrow_listener)
                # Create a line for the glowing trail to follow
                path = Line(input_neuron.get_right(), hidden_neuron.get_left(), buff=0.1)
                input_to_hidden_paths.append(path)

        hidden_to_output_arrows = VGroup()
        hidden_to_output_paths = []  # Store paths for glow animation
        for hidden_neuron in hidden_layer:
            for output_neuron in output_layer:
                arrow = Arrow(hidden_neuron.get_right(), output_neuron.get_left(), buff=0.1, color=WHITE)
                hidden_to_output_arrows.add(arrow)
                path = Line(hidden_neuron.get_right(), output_neuron.get_left(), buff=0.1)
                hidden_to_output_paths.append(path)

        # Function to animate arrows with a tracing tail effect
        def animate_arrows_with_tracing_tail(arrows, paths, run_time=1.5):
            animations = []
            for arrow, path in zip(arrows, paths):
                # Create the arrow
                arrow_anim = Create(arrow, rate_func=smooth, run_time=run_time)
                # Create a group of fading dots for the trailing effect
                trail_dots = VGroup()
                num_dots = 10  # Number of dots in the trail
                for i in range(num_dots):
                    # Create a dot with decreasing opacity for the tail
                    opacity = 1 - (i / num_dots)
                    dot = Dot(point=path.get_start(), color=YELLOW, radius=0.05).set_opacity(opacity)
                    trail_dots.add(dot)
                # Animate each dot along the path with a slight delay
                trail_anims = []
                for i, dot in enumerate(trail_dots):
                    delay = i * (run_time / num_dots) * 0.3  # Stagger the dots
                    move_time = run_time - delay
                    if move_time > 0:
                        move = MoveAlongPath(dot, path, rate_func=linear, run_time=move_time)
                        fade_out = FadeOut(dot, run_time=0.2)
                        trail_anims.append(AnimationGroup(move, fade_out, lag_ratio=0))
                # Combine arrow creation and trail animations
                animations.append(AnimationGroup(arrow_anim, *trail_anims, lag_ratio=0))
            return animations

        # Animate the creation of the neural network with tracing tail effect
        self.play(FadeIn(input_layer), Write(input_label))
        self.play(FadeIn(hidden_layer), Write(hidden_label))
        self.play(*animate_arrows_with_tracing_tail(input_to_hidden_arrows, input_to_hidden_paths))
        self.play(FadeIn(output_layer), Write(output_label))
        self.play(*animate_arrows_with_tracing_tail(hidden_to_output_arrows, hidden_to_output_paths))

        # Wait to show the complete network
        self.wait(2)