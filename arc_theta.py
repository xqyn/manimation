from manim import *
from manim import DashedLine, always_redraw
import math

#config.background_color = WHITE

class ArcLinearMapping(Scene):
    def construct(self):
        # Set camera frame size to accommodate all elements with square aspect ratio
        #self.camera.frame_height = 12  # Covers vertical span (~9 units)
        #self.camera.frame_width = 12   # Square to prevent distortion

        # Specified arc degrees
        arc_degs = [25, 40, 65, 140]
        arc_rads = [math.radians(d) for d in arc_degs]

        # Colors for each arc
        colors = [RED, GREEN, BLUE, ORANGE]

        # Create base circle
        circle = Circle(radius=2, color=WHITE).shift(UP * 1.25)

        # Accumulate angle to place arcs correctly
        angle_acc = 0

        # Storage
        trackers = []

        # Adjust vertical spacing based on scene height
        y_offsets = [DOWN * (i * 0.65 + 0.75) for i in range(4)]

        # Add circle to scene
        self.add(circle)

        for i in range(4):
            arc_deg = arc_degs[i]
            arc_rad = arc_rads[i]
            color = colors[i]
            start_angle = math.radians(angle_acc)
            angle_acc += arc_deg

            # ValueTracker for animation
            tracker = ValueTracker(0)
            trackers.append((tracker, arc_rad, start_angle))

            # Arc on circle
            arc = Arc(
                radius=2.3,
                start_angle=start_angle,
                angle=arc_rad,
                color=color,
                stroke_width=5
            ).shift(UP * 1.25)

            # Circular dot moving within arc
            circular_dot = always_redraw(
                lambda t=tracker, start=start_angle, color=color: Dot(color=color).move_to(
                    circle.point_at_angle(start + t.get_value())
                )
)
            # Number line corresponding to arc_deg, centered, no numbers
            number_line = NumberLine(
                x_range=[0, arc_deg, arc_deg / 3],
                length=arc_deg/30,
                include_numbers=False,  # Remove numbers from scale
            #).shift(y_offsets[i])  # Centered
            #).align_to(ORIGIN, LEFT).shift(y_offsets[i])  # Left-aligned
            ).next_to(circle, DOWN).align_to(circle, LEFT).shift(y_offsets[i])

            # Dot on number line
            linear_dot = always_redraw(
                lambda t=tracker, line=number_line, color=color: Dot(color=color).move_to(
                    line.n2p(math.degrees(t.get_value()))
                )
            )

            # Mapping line
            # mapping_line = always_redraw(
            #     lambda a=linear_dot, b=circular_dot, color=color: Line(
            #         start=a.get_center(),
            #         end=b.get_center(),
            #         color=color,
            #         #dash_length=0.1 # optional: adjust dash size
            #     )
            # )
            mapping_line = always_redraw(
                lambda a=linear_dot, b=circular_dot, color=color: DashedLine(
                    a.get_center(),
                    b.get_center(),
                    color=color
                )
            )
            # Degree text
            angle_text = always_redraw(
                lambda t=tracker, d=linear_dot: Text(
                    f"{int(math.degrees(t.get_value()))}°"
                ).scale(0.5).next_to(d, UP, buff=0.2)
            )

            # Arc size label
            arc_label = MathTex(f"{int(arc_deg)}^\circ").scale(0.6).move_to(
                arc.point_from_proportion(0.5) + 0.3 * OUT
            )

            # Add to scene
            self.add(
                arc, number_line, linear_dot, circular_dot,
                mapping_line, angle_text, arc_label
            )
        # Coordinate transformation label
        coord_equations = MathTex(
            r"x(\theta) = r \cos(\theta), \quad y(\theta) = r \sin(\theta)"
        ).scale(0.6).to_corner(UR).shift(DOWN * 0.5)
        self.add(coord_equations)
        
        # Animate all arcs together
        self.play(
            *[t.animate.set_value(rad) for t, rad, _ in trackers],
            run_time=5,
            rate_func=linear
        )
        
        # Wait briefly before playing backward
        self.wait(1)

        # Animate all arcs backward
        self.play(
            *[t.animate.set_value(0) for t, _, _ in trackers],
            run_time=5,
            rate_func=linear
        )