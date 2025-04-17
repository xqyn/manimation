# --- arc
CircleAnimation:
	manim -pql arc_circle.py CircleAnimation
	manim -pql arc_circle.py CircleAnimation --format gif

ArcLinearMapping:
	manim -pql arc_theta.py ArcLinearMapping
	manim -pql arc_theta.py ArcLinearMapping --format gif


# --- neuron
NeuralNetwork:
	manim -pql nn_visual.py NeuralNetwork --format gif

# --- WaddingtonLandscape
WaddingtonLandscape:
	manim -pql wdd_modeling.py WaddingtonLandscape --format gif