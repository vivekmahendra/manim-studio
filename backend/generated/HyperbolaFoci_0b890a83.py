from manim import *
import numpy as np
import math

class HyperbolaFoci(Scene):
    def construct(self):
        # ---------- Parameters ----------
        a = 3  # semi-transverse axis
        b = 2  # semi-conjugate axis
        c = math.sqrt(a**2 + b**2)  # distance to each focus

        # ---------- Title & Formulas ----------
        title = Text("Hyperbolas & Foci", weight=BOLD).to_edge(UP)
        formula = MathTex(
            r"\frac{x^2}{a^2}-\frac{y^2}{b^2}=1,\quad",
            r"c=\sqrt{a^2+b^2}",
            font_size=38
        ).next_to(title, DOWN)

        self.play(Write(title))
        self.play(Write(formula))
        self.wait(0.5)

        # ---------- Axes ----------
        axes = Axes(
            x_range=[-8, 8, 1],
            y_range=[-6, 6, 1],
            x_length=10,
            y_length=6,
            tips=False
        )
        axes_labels = axes.get_axis_labels(MathTex("x"), MathTex("y"))
        self.play(Create(axes), FadeIn(axes_labels))
        self.wait(0.3)

        # ---------- Hyperbola branches ----------
        # y = ± (b/a) * sqrt(x^2 - a^2),  |x| >= a
        m = b / a
        x_min, x_max = axes.x_range[0], axes.x_range[1]

        right_top = axes.plot(lambda x:  m * np.sqrt(x**2 - a**2), x_range=[a, x_max])
        right_bot = axes.plot(lambda x: -m * np.sqrt(x**2 - a**2), x_range=[a, x_max])
        left_top  = axes.plot(lambda x:  m * np.sqrt(x**2 - a**2), x_range=[x_min, -a])
        left_bot  = axes.plot(lambda x: -m * np.sqrt(x**2 - a**2), x_range=[x_min, -a])

        hyperbola = VGroup(right_top, right_bot, left_top, left_bot).set_color(BLUE)
        self.play(Create(hyperbola))
        self.wait(0.3)

        # ---------- Asymptotes y = ±(b/a)x ----------
        asym1 = axes.plot(lambda x:  m * x, x_range=[x_min, x_max])
        asym2 = axes.plot(lambda x: -m * x, x_range=[x_min, x_max])
        asymptotes = VGroup(
            DashedVMobject(asym1, num_dashes=60),
            DashedVMobject(asym2, num_dashes=60),
        ).set_color(GRAY_B)
        self.play(FadeIn(asymptotes))
        self.wait(0.3)

        # ---------- Vertices & Foci ----------
        V1 = Dot(axes.coords_to_point( a, 0), color=YELLOW)
        V2 = Dot(axes.coords_to_point(-a, 0), color=YELLOW)
        F1 = Dot(axes.coords_to_point( c, 0), color=RED)
        F2 = Dot(axes.coords_to_point(-c, 0), color=RED)

        V1_label = MathTex(r"(a,0)", font_size=30).next_to(V1, DOWN)
        V2_label = MathTex(r"(-a,0)", font_size=30).next_to(V2, DOWN)
        F1_label = MathTex(r"(c,0)", font_size=30).next_to(F1, DOWN)
        F2_label = MathTex(r"(-c,0)", font_size=30).next_to(F2, DOWN)

        self.play(FadeIn(V1, V2), FadeIn(V1_label, V2_label))
        self.play(FadeIn(F1, F2), FadeIn(F1_label, F2_label))
        self.wait(0.3)

        # ---------- Explanation bullet points ----------
        steps = VGroup(
            Text("How to find the foci:", weight=BOLD),
            Text("1) Put the equation in standard form."),
            Text("2) Read off a and b."),
            Text("3) Compute c = sqrt(a² + b²)."),
            Text("4) Foci at (±c, 0)  (or (0, ±c) if y-term is positive).")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        # Place the steps to the right
        steps.to_corner(UR).shift(LEFT*0.5 + DOWN*0.3).scale(0.6)

        self.play(FadeIn(steps, lag_ratio=0.1))
        self.wait(0.5)

        # ---------- Highlight relationship: c^2 = a^2 + b^2 ----------
        pyth = MathTex(r"c^2 = a^2 + b^2", font_size=44).to_corner(DL)
        box = SurroundingRectangle(pyth, buff=0.2)
        self.play(Write(pyth), Create(box))
        self.wait(1.0)

        # ---------- Final note ----------
        note = Text(
            f"For a = {a}, b = {b}  →  c = √(a²+b²) = {c:.3f}",
            slant=ITALIC
        ).next_to(pyth, DOWN)
        self.play(Write(note))
        self.wait(2)  # hold final frame a bit
