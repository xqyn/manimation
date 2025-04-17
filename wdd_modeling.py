"""
project: manimation
april 17 2025 - XQ - LUMC
WaddingtonLandscape Landscape:
"""

from manim import *
import numpy as np

class WaddingtonLandscape(ThreeDScene):
    def construct(self):
        # Set up the 3D scene
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=1)

        # Define the Waddington landscape surface
        def waddington_surface(u, v):
            x = u
            y = v
            # Create a landscape with two valleys using a combination of Gaussian-like functions
            z = 3 * np.exp(-0.5 * ((x - 1.5)**2 + y**2)) + 2 * np.exp(-0.5 * ((x + 1.5)**2 + y**2)) - 0.1 * x**2 + 0.05 * y**2
            return np.array([x, y, z], dtype=np.float64)  # Ensure float64 output

        # Create the 3D surface
        surface = Surface(
            lambda u, v: waddington_surface(u, v),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        # Add axes for reference
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )

        # Create the ball (a small sphere)
        ball = Sphere(radius=0.1, color=RED, resolution=(10, 10))
        initial_pos = np.array([0.0, 2.0, waddington_surface(0, 2)[2] + 0.1], dtype=np.float64)  # Ensure float64
        ball.move_to(initial_pos)

        # Add surface, axes, and ball to the scene
        self.add(axes, surface, ball)
        self.begin_ambient_camera_rotation(rate=0.1)

        # Define the gradient of the surface for ball motion
        def get_gradient(x, y):
            # Approximate partial derivatives using finite differences
            h = 0.01
            dz_dx = (waddington_surface(x + h, y)[2] - waddington_surface(x - h, y)[2]) / (2 * h)
            dz_dy = (waddington_surface(x, y + h)[2] - waddington_surface(x, y - h)[2]) / (2 * h)
            return np.array([-dz_dx, -dz_dy, 0], dtype=np.float64)  # Ensure float64

        # Simulate ball rolling down using gradient descent
        pos = initial_pos.copy().astype(np.float64)  # Ensure float64
        dt = 0.1  # Time step
        velocity = np.array([0.0, 0.0, 0.0], dtype=np.float64)  # Ensure float64
        path = []  # Store path for tracing

        for _ in range(500):
            # Get gradient at current position
            grad = get_gradient(pos[0], pos[1])
            # Update velocity (simple damping and gradient-based acceleration)
            velocity += (-0.5 * grad * dt - 0.1 * velocity * dt).astype(np.float64)  # Ensure float64
            # Update position
            pos += (velocity * dt).astype(np.float64)  # Ensure float64
            # Update z-coordinate to stay on surface
            pos[2] = waddington_surface(pos[0], pos[1])[2] + 0.1
            path.append(pos.copy())

        # Animate the ball rolling
        for i in range(1, len(path)):
            self.play(
                ball.animate.move_to(path[i]),
                run_time=0.1,
                rate_func=linear,
            )

        # Trace the path with a line
        path_line = VMobject()
        path_line.set_points_as_corners(path)
        path_line.set_color(YELLOW)
        self.play(Create(path_line), run_time=2)

        # Hold the final scene
        self.wait(2)