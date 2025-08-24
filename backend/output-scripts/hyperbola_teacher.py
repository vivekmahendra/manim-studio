from manim import *
import numpy as np
import math

class HyperbolaTeacher(Scene):
    """
    A teacher-style lesson that follows the provided transcript.
    - Uses a right-hand "board" for text that is replaced between segments (no overlap).
    - Walks through: circle & ellipse review, two hyperbola forms, solving for y, asymptotes,
      orientation tests, and vertices for both cases.
    """
    def setup(self):
        self.board_group = None  # right-side panel with text, replaced each step

    # ---------- Helper to show/replace a right-side "board" of bullet text ----------
    def show_board(self, *lines, title=None):
        # Fade out previous board (prevents overlap)
        if self.board_group is not None:
            self.play(FadeOut(self.board_group, run_time=0.3))
            self.board_group = None

        # Build new board content
        content = VGroup()
        if title is not None:
            title_m = Text(title, weight=BOLD)
            content.add(title_m)
        for ln in lines:
            # Use Text for narration lines to avoid LaTeX requirements here
            content.add(Text(ln, font_size=30))

        content.arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        # Panel background
        pad = 0.35
        panel = RoundedRectangle(corner_radius=0.2, width=6.4, height=content.height + 2*pad)
        panel.set_fill(GRAY, opacity=0.05).set_stroke(GRAY, width=1)
        panel_group = VGroup(panel, content)
        panel_group.arrange_in_grid(cols=1, buff=0)
        # Position in upper-right area
        panel_group.to_corner(UR).shift(LEFT*0.2 + DOWN*0.4)

        # Center content within panel
        content.move_to(panel.get_center())

        self.board_group = panel_group
        self.play(FadeIn(panel_group, shift=LEFT*0.2, run_time=0.4))

    def construct(self):
        # Title
        title = Text("Hyperbolas — Building Intuition", weight=BOLD).to_edge(UP)
        self.play(Write(title))

        # High-level goal
        self.show_board(
            "Goal: understand equations, asymptotes, orientation, and foci.",
            "We'll start by connecting to circle and ellipse forms.",
            title="Plan"
        )
        self.wait(0.6)

        # ---------- Review: circle & ellipse (equations only, replace text between) ----------
        circ1 = MathTex("x^2 + y^2 = r^2").scale(1.0).to_edge(LEFT).shift(DOWN*0.5 + RIGHT*0.3)
        circ2 = MathTex(r"\frac{x^2}{r^2} + \frac{y^2}{r^2} = 1").scale(1.0).next_to(circ1, DOWN, buff=0.4)
        self.play(Write(circ1))
        self.show_board(
            "Circle centered at the origin:",
            r"x^2 + y^2 = r^2",
            "Divide by r^2 → standard form.",
            title="Review — Circle"
        )
        self.wait(0.4)
        self.play(TransformFromCopy(circ1, circ2))
        self.wait(0.4)

        ell = MathTex(r"\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1").scale(1.0).next_to(circ2, DOWN, buff=0.6)
        self.show_board(
            "Ellipse standard form:",
            r"x^2/a^2 + y^2/b^2 = 1",
            "a,b control horizontal/vertical stretching.",
            title="Review — Ellipse"
        )
        self.play(Write(ell))
        self.wait(0.6)
        self.play(FadeOut(circ1, circ2, ell, run_time=0.4))  # clear formulas before moving on

        # ---------- Hyperbola: two forms ----------
        form1 = MathTex(r"\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1").scale(1.1).to_edge(LEFT).shift(DOWN*0.5 + RIGHT*0.3)
        form2 = MathTex(r"\frac{y^2}{b^2} - \frac{x^2}{a^2} = 1").scale(1.1).next_to(form1, DOWN, buff=0.6)
        self.play(Write(form1))
        self.show_board(
            "Hyperbola looks like ellipse but with a minus:",
            r"x^2/a^2 - y^2/b^2 = 1  (opens left–right)",
            r"y^2/b^2 - x^2/a^2 = 1  (opens up–down)",
            "We will derive asymptotes instead of memorizing.",
            title="Hyperbola — Standard Forms"
        )
        self.play(Write(form2))
        self.wait(0.8)

        # ---------- Axes (left side) and parameters ----------
        axes = Axes(
            x_range=[-8, 8, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=6,
            tips=False
        ).to_edge(LEFT).shift(DOWN*0.2 + RIGHT*0.3)
        self.play(Create(axes))

        # ---------- Derive asymptotes from form1 by solving for y ----------
        self.show_board(
            "Derive asymptotes for:  x^2/a^2 - y^2/b^2 = 1",
            "1) Isolate y^2 term.",
            "2) Multiply to clear fractions and sign.",
            "3) Take square root; analyze as |x|→∞.",
            title="Strategy"
        )
        step1 = MathTex(
            r"\frac{x^2}{a^2} - \frac{y^2}{b^2} = 1 \;\Rightarrow\;"
            r"-\frac{y^2}{b^2} = 1 - \frac{x^2}{a^2}"
        ).scale(0.9).next_to(axes, UP, buff=0.2).align_to(axes, LEFT).shift(RIGHT*0.2)
        self.play(Write(step1))

        step2 = MathTex(
            r"\times(-b^2)\;:\quad y^2 = \frac{b^2}{a^2}x^2 - b^2"
        ).scale(0.9).next_to(step1, DOWN, buff=0.25).align_to(step1, LEFT)
        self.play(Write(step2))

        step3 = MathTex(
            r"y = \pm\sqrt{\frac{b^2}{a^2}x^2 - b^2}"
        ).scale(0.9).next_to(step2, DOWN, buff=0.25).align_to(step2, LEFT)
        self.play(Write(step3))

        approx = MathTex(
            r"\text{As }|x|\to\infty:\quad y \approx \pm\frac{b}{a}x"
        ).scale(0.9).next_to(step3, DOWN, buff=0.25).align_to(step3, LEFT)
        self.play(Write(approx))
        self.wait(0.8)

        # ---------- Draw asymptotes y = ±(b/a)x ----------
        a, b = 3, 2
        m = b / a
        x_min, x_max = axes.x_range[0], axes.x_range[1]
        asym1 = axes.plot(lambda x:  m*x, x_range=[x_min, x_max])
        asym2 = axes.plot(lambda x: -m*x, x_range=[x_min, x_max])
        asymptotes = VGroup(
            DashedVMobject(asym1, num_dashes=60),
            DashedVMobject(asym2, num_dashes=60),
        ).set_color(GRAY_B)
        self.play(FadeIn(asymptotes))

        # ---------- Plot the horizontal-opening hyperbola (form1) ----------
        def y_top(x):
            return m*np.sqrt(x**2 - a**2)
        def y_bot(x):
            return -m*np.sqrt(x**2 - a**2)

        right_top = axes.plot(lambda x: y_top(x),  x_range=[a, x_max])
        right_bot = axes.plot(lambda x: y_bot(x),  x_range=[a, x_max])
        left_top  = axes.plot(lambda x: y_top(x),  x_range=[x_min, -a])
        left_bot  = axes.plot(lambda x: y_bot(x),  x_range=[x_min, -a])
        hyper_lr = VGroup(right_top, right_bot, left_top, left_bot).set_color(BLUE)
        self.play(Create(hyper_lr))

        # ---------- Orientation + vertices test ----------
        self.show_board(
            "Orientation (left–right) because x-term is positive:",
            "• y=0 works → x^2/a^2=1 → x=±a (vertices).",
            "• x=0 fails (square root of negative).",
            "• Asymptotes: y=±(b/a)x.",
            title="Interpretation"
        )
        V1 = Dot(axes.coords_to_point( a, 0), color=YELLOW)
        V2 = Dot(axes.coords_to_point(-a, 0), color=YELLOW)
        V1_lab = MathTex(r"(a,0)", font_size=30).next_to(V1, DOWN)
        V2_lab = MathTex(r"(-a,0)", font_size=30).next_to(V2, DOWN)
        self.play(FadeIn(V1, V2, V1_lab, V2_lab))
        self.wait(0.8)

        # ---------- Clear the algebra text before switching to the other form ----------
        self.play(FadeOut(step1, step2, step3, approx, run_time=0.4))

        # ---------- Now analyze the vertical-opening form (form2) ----------
        self.show_board(
            "Now the other standard form:  y^2/b^2 - x^2/a^2 = 1",
            "Solve for y and analyze |x|→∞ again.",
            "Expect up–down opening.",
            title="Second Case"
        )
        step1b = MathTex(
            r"\frac{y^2}{b^2} - \frac{x^2}{a^2} = 1 \;\Rightarrow\;"
            r"\frac{y^2}{b^2} = 1 + \frac{x^2}{a^2}"
        ).scale(0.9).next_to(axes, UP, buff=0.2).align_to(axes, LEFT).shift(RIGHT*0.2)
        self.play(Write(step1b))

        step2b = MathTex(
            r"\times b^2\;:\quad y^2 = \frac{b^2}{a^2}x^2 + b^2"
        ).scale(0.9).next_to(step1b, DOWN, buff=0.25).align_to(step1b, LEFT)
        self.play(Write(step2b))

        step3b = MathTex(
            r"y = \pm\sqrt{\frac{b^2}{a^2}x^2 + b^2}"
        ).scale(0.9).next_to(step2b, DOWN, buff=0.25).align_to(step2b, LEFT)
        self.play(Write(step3b))

        approxb = MathTex(
            r"\text{As }|x|\to\infty:\quad y \approx \pm\frac{b}{a}x"
        ).scale(0.9).next_to(step3b, DOWN, buff=0.25).align_to(step3b, LEFT)
        self.play(Write(approxb))
        self.wait(0.6)

        # Replace the graph with a vertical-opening hyperbola
        self.play(FadeOut(hyper_lr, V1, V2, V1_lab, V2_lab, run_time=0.4))

        # For vertical-opening:  x^2/a^2 appears with minus; vertices at (0, ±b)
        def x_allowed_for_vertical(y):
            return True  # We will parametrize by x anyway

        # Graph vertical-opening hyperbola: y = ±sqrt( (b^2/a^2)x^2 + b^2 )
        def y_top_v(x):
            return np.sqrt((b**2/a**2)*x**2 + b**2)
        def y_bot_v(x):
            return -np.sqrt((b**2/a**2)*x**2 + b**2)

        top_branch = axes.plot(lambda x: y_top_v(x), x_range=[x_min, x_max])
        bot_branch = axes.plot(lambda x: y_bot_v(x), x_range=[x_min, x_max])
        hyper_ud = VGroup(top_branch, bot_branch).set_color(GREEN)
        self.play(Create(hyper_ud))

        self.show_board(
            "Orientation (up–down) because y-term is positive:",
            "• x=0 works → y^2/b^2=1 → y=±b (vertices).",
            "• y=0 fails (impossible without imaginaries).",
            "• Asymptotes are the same slopes: y=±(b/a)x.",
            title="Interpretation"
        )
        V3 = Dot(axes.coords_to_point(0,  b), color=YELLOW)
        V4 = Dot(axes.coords_to_point(0, -b), color=YELLOW)
        V3_lab = MathTex(r"(0,b)", font_size=30).next_to(V3, RIGHT)
        V4_lab = MathTex(r"(0,-b)", font_size=30).next_to(V4, RIGHT)
        self.play(FadeIn(V3, V4, V3_lab, V4_lab))

        # ---------- Foci reminder ----------
        c = math.sqrt(a**2 + b**2)
        F1 = Dot(axes.coords_to_point( c, 0), color=RED)
        F2 = Dot(axes.coords_to_point(-c, 0), color=RED)
        F1_lab = MathTex(r"(c,0)", font_size=30).next_to(F1, DOWN)
        F2_lab = MathTex(r"(-c,0)", font_size=30).next_to(F2, DOWN)

        self.show_board(
            r"Foci distance:  c=\sqrt{a^2+b^2}.",
            r"Horizontal form → foci at (±c,0).",
            r"Vertical form → foci at (0,±c).",
            title="Foci"
        )
        # Indicate the horizontal-case foci (since axes are still on screen)
        self.play(FadeIn(F1, F2, F1_lab, F2_lab))

        # Final hold; then clear board to avoid overlap if reused
        self.wait(2)
        self.play(FadeOut(self.board_group, run_time=0.3))
