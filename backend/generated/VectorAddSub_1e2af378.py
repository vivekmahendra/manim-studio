# file: vector_add_sub.py
from manim import *

class VectorAddSub(Scene):
    """
    Topic: Vector addition and subtraction
    Non-negotiables implemented:
      - Two-pane layout (left 62% graph, right 38% board)
      - One idea per beat (1 equation + 1 visual + 1 small label group)
      - No overlap (previous board/visuals FadeOut and replaced via VGroups)
      - Title small, at top with margin
      - Contrast panels for text/equations (rounded, light background)
      - Scaling guards (scale_to_fit_width on board)
      - Gentle transitions (FadeIn/Create/TransformFromCopy/FadeOut)
      - Axes centered left; limited ticks; small labels
      - Color discipline: a=BLUE, b=GREEN, r/d=YELLOW, -b=RED
    """

    # -------------------------
    # ----- Layout helpers ----
    # -------------------------
    def setup_layout(self):
        fw, fh = config.frame_width, config.frame_height

        # Title (persistent)
        self.title = Text("Vector Addition & Subtraction", weight=BOLD)
        self.title.scale(0.6).to_edge(UP, buff=0.4)

        # Left / right safe areas
        self.left_rect  = Rectangle(width=fw * 0.62, height=fh * 0.78, stroke_opacity=0)
        self.right_rect = Rectangle(width=fw * 0.38, height=fh * 0.78, stroke_opacity=0)

        self.left_rect.to_edge(LEFT, buff=0.4)
        self.right_rect.to_edge(RIGHT, buff=0.4)

        # Axes in left pane (persistent)
        self.axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-1, 4, 1],
            x_length=self.left_rect.width * 0.92,
            y_length=self.left_rect.height * 0.92,
            axis_config=dict(
                include_tip=True,
                stroke_width=2.5,
                tick_size=0.04,
                include_numbers=False,
            ),
        )
        self.axes.move_to(self.left_rect.get_center())

        # Small axis labels
        xlab = MathTex("x").scale(0.5).next_to(self.axes.x_axis.get_end(), DOWN, buff=0.1)
        ylab = MathTex("y").scale(0.5).next_to(self.axes.y_axis.get_end(), LEFT, buff=0.1)

        self.add(self.title, self.axes, xlab, ylab)

        # State holders
        self.board_group = VGroup()  # right pane current panel
        self.visual_group = VGroup() # left pane current visual

    def show_board(self, *lines, title=None):
        """Render a rounded, light panel with 2–5 concise lines on the right.
        Accepts strings and/or prebuilt Mobjects (e.g., MathTex). Replaces previous panel."""
        # Fade out previous board
        if len(self.board_group) > 0:
            self.play(FadeOut(self.board_group, duration=0.3))
            self.remove(self.board_group)

        panel = RoundedRectangle(corner_radius=0.2, width=self.right_rect.width, height=self.right_rect.height)
        panel.set_fill(WHITE, opacity=0.06).set_stroke(opacity=0)
        panel.move_to(self.right_rect.get_center())

        content = VGroup()
        items = []

        # Optional title (small, single line)
        if title:
            t = Text(title, weight=BOLD).scale(0.42)
            items.append(t)

        # Build bullet/equation lines
        for entry in lines:
            if isinstance(entry, Mobject):
                obj = entry
                # Ensure equations have contrast
                if isinstance(obj, MathTex):
                    obj.add_background_rectangle(opacity=0.15, buff=0.06)
                items.append(obj.scale(0.9))
            else:
                # Plain text bullet
                bullet = Tex(r"$\bullet$ " + str(entry), substrings_to_isolate=["$\\bullet$"])
                bullet.scale(0.7)
                items.append(bullet)

        content = VGroup(*items)
        content.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        # Keep inside panel margins
        max_w = panel.width * 0.86
        for m in content:
            if m.width > max_w:
                m.scale_to_fit_width(max_w)

        # Position content near top-left inside the panel
        content.move_to(panel.get_top(), aligned_edge=UL).shift(DOWN * 0.45 + RIGHT * 0.35)

        self.board_group = VGroup(panel, content)
        self.play(FadeIn(self.board_group, duration=0.3))
        self.wait(0.5)  # breath

    def set_visual(self, group_builder, animate=True):
        """Replace left visual (everything besides the persistent axes/title)."""
        if len(self.visual_group) > 0:
            self.play(FadeOut(self.visual_group, duration=0.3))
            self.remove(self.visual_group)
        self.visual_group = group_builder()
        if animate:
            # Gentle construction of the visual (Create for arrows, FadeIn labels)
            builds = []
            for m in self.visual_group:
                if isinstance(m, (Arrow, Line, Vector)):
                    builds.append(Create(m, run_time=0.6))
                else:
                    builds.append(FadeIn(m, run_time=0.4))
            self.play(*builds)
            self.wait(0.6)

    # -------------------------
    # ----- Visual helpers ----
    # -------------------------
    def v(self, x, y):
        return self.axes.c2p(x, y)

    def make_vector(self, start_xy, end_xy, color=WHITE, tip_length=0.15, stroke_width=5):
        return Arrow(
            start=self.v(*start_xy),
            end=self.v(*end_xy),
            buff=0,
            max_tip_length_to_length_ratio=0.15,
            tip_length=tip_length,
            stroke_width=stroke_width,
            color=color,
        )

    def small_label(self, tex, at_point_xy, direction=UR, color=WHITE):
        lab = MathTex(tex).scale(0.6).set_color(color)
        lab.add_background_rectangle(opacity=0.15, buff=0.04)
        lab.next_to(self.v(*at_point_xy), direction, buff=0.12)
        return lab

    # -------------------------
    # --------- Scene ---------
    # -------------------------
    def construct(self):
        self.setup_layout()

        # Predefine a and b (nice numbers for visibility)
        a = (2.0, 1.0)         # BLUE
        b = (2.4, 1.6)         # GREEN
        a_head = a
        b_head_from_a = (a[0] + b[0], a[1] + b[1])
        minus_b = (-b[0], -b[1])
        a_minus_b_head = (a[0] + minus_b[0], a[1] + minus_b[1])

        # -------------
        # Beat 1: What is a vector?
        # -------------
        def visual_1():
            g = VGroup()
            va = self.make_vector((0, 0), a, color=BLUE)
            la = self.small_label(r"\vec{a}", a, UR, BLUE)
            g.add(va, la)
            return g

        self.show_board(
            "A vector has magnitude and direction.",
            "Drawn as an arrow from tail (start) to head (end).",
            "We’ll work in 2D with simple coordinates.",
            title="Vectors"
        )
        self.set_visual(visual_1)

        # -------------
        # Beat 2: Addition (tip-to-tail)
        # -------------
        eq_add = MathTex(r"\vec{r}=\vec{a}+\vec{b}").scale(0.9)
        def visual_2():
            g = VGroup()
            va = self.make_vector((0, 0), a, color=BLUE)
            vb_tail_at_a = self.make_vector(a, b_head_from_a, color=GREEN)
            vr = self.make_vector((0, 0), b_head_from_a, color=YELLOW)
            la = self.small_label(r"\vec{a}", a, UR, BLUE)
            lb = self.small_label(r"\vec{b}", b_head_from_a, UR, GREEN)
            lr = self.small_label(r"\vec{r}", b_head_from_a, UL, YELLOW)
            # tiny label group (counted as one small group)
            labels = VGroup(la, lb, lr)
            g.add(va, vb_tail_at_a, vr, labels)
            return g

        self.show_board(
            "Addition = tip-to-tail: place tail of \\(\\vec b\\) at the head of \\(\\vec a\\).",
            eq_add,
            "Result \\(\\vec r\\) goes from the original tail to the final head.",
            title="Vector Addition"
        )
        self.set_visual(visual_2)

        # -------------
        # Beat 3: Component-wise addition
        # -------------
        eq_comp = MathTex(
            r"\vec{a}+\vec{b}=\langle a_x+b_x,\ a_y+b_y\rangle"
        ).scale(0.9)

        def visual_3():
            g = VGroup()
            # Re-show result cleanly (same single visual)
            vr = self.make_vector((0, 0), b_head_from_a, color=YELLOW)
            lr = self.small_label(r"\langle a_x{+}b_x,\ a_y{+}b_y\rangle", b_head_from_a, UL, YELLOW)
            g.add(vr, lr)
            return g

        self.show_board(
            "Add components: x with x, y with y.",
            eq_comp,
            "Same geometry; components explain why tip-to-tail works.",
            title="Components"
        )
        self.set_visual(visual_3)

        # -------------
        # Beat 4: Subtraction as adding the negative
        # -------------
        eq_sub = MathTex(r"\vec{d}=\vec{a}-\vec{b}=\vec{a}+(-\vec{b})").scale(0.9)

        def visual_4():
            g = VGroup()
            va = self.make_vector((0, 0), a, color=BLUE)
            vneg_b_from_a = self.make_vector(a, a_minus_b_head, color=RED)
            vd = self.make_vector((0, 0), a_minus_b_head, color=YELLOW)
            la = self.small_label(r"\vec{a}", a, UR, BLUE)
            lnb = self.small_label(r"-\vec{b}", a_minus_b_head, UL, RED)
            ld = self.small_label(r"\vec{d}", a_minus_b_head, UR, YELLOW)
            labels = VGroup(la, lnb, ld)
            g.add(va, vneg_b_from_a, vd, labels)
            return g

        self.show_board(
            "Subtraction = add the negative of \\(\\vec b\\).",
            eq_sub,
            "Reverse \\(\\vec b\\), tip-to-tail with \\(\\vec a\\), then connect the overall tail to head.",
            title="Vector Subtraction"
        )
        self.set_visual(visual_4)

        # -------------
        # Beat 5: Quick recap / clean final frame
        # -------------
        def visual_5():
            g = VGroup()
            # Show only the two results side-by-side notion by reusing same origin but lighter a for context
            va_faint = self.make_vector((0, 0), a, color=BLUE_E)
            vr = self.make_vector((0, 0), b_head_from_a, color=YELLOW)
            vd = self.make_vector((0, 0), a_minus_b_head, color=YELLOW)
            lr = self.small_label(r"\vec{a}{+}\vec{b}", b_head_from_a, UL, YELLOW)
            ld = self.small_label(r"\vec{a}{-}\vec{b}", a_minus_b_head, UL, YELLOW)
            g.add(va_faint, vr, vd, VGroup(lr, ld))
            return g

        self.show_board(
            "Addition: tip-to-tail, \\(\\vec r=\\vec a+\\vec b\\).",
            "Components: add x with x, y with y.",
            "Subtraction: \\(\\vec a-\\vec b=\\vec a+(-\\vec b)\\).",
            "Keep 1 equation + 1 visual + 1 tiny label group per beat.",
            title="Summary"
        )
        self.set_visual(visual_5)

        # Uncluttered final hold
        self.wait(1.2)


# -------------------------
# -------- Render ---------
# -------------------------
# Preview (low quality, quick):
#   manim -pql vector_add_sub.py VectorAddSub
#
# High quality:
#   manim -pqh vector_add_sub.py VectorAddSub -o vector_add_sub_hq
