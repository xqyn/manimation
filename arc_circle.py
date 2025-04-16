from manim import *

class CircleAnimation(Scene):
    def construct(self):
        # Create a circle with radius 2
        circle = Circle(radius=2, color=BLUE)
        
        # Create a ValueTracker to track angle progression
        t_tracker = ValueTracker(0)

        # Create a dot that moves along the circumference of the circle
        dot = always_redraw(lambda: Dot(point=circle.point_from_proportion(t_tracker.get_value()), color=RED))
        
        # Create angle text that updates with the dot
        angle_text = always_redraw(
            lambda: Text(f"{int(t_tracker.get_value() * 360)}°").move_to(UP * 3)
        )
        
        # Add circle, dot, and text to the scene
        self.add(circle, dot, angle_text)
        
        # Animate the ValueTracker from 0 to 1 over 4 seconds
        self.play(t_tracker.animate.set_value(1), run_time=4, rate_func=linear)