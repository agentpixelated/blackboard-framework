from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

WIRE = "#D8D8D8"
TEAL = "#5ba5bc"
RED = "#b86e64"


class LoopTheLoop(Scene):
    def construct(self):
        # ================= geometry =================
        # Loop center/radius; incline meets the loop at an exact tangent point
        # so the track (and the ball) has no kink. Ball enters lower-left and
        # travels counterclockwise (increasing theta) once around.
        Cx, Cy = 1.5, -0.5
        R = 1.8
        P0 = np.array([-4.5, 2.0])      # release point (top of incline)
        C = np.array([Cx, Cy])

        d_vec = P0 - C
        d = np.linalg.norm(d_vec)
        alpha = np.arctan2(d_vec[1], d_vec[0])
        beta = np.arccos(R / d)
        theta_T, T_pt = None, None
        for sgn in (+1, -1):
            th = alpha + sgn * beta
            T = C + R * np.array([np.cos(th), np.sin(th)])
            v_in = (T - P0) / np.linalg.norm(T - P0)
            t_ccw = np.array([-np.sin(th), np.cos(th)])
            if np.dot(v_in, t_ccw) > 0:
                theta_T, T_pt = th, T
                break
        assert theta_T is not None
        T3 = np.array([T_pt[0], T_pt[1], 0.0])
        P0_3 = np.array([P0[0], P0[1], 0.0])
        C3 = np.array([Cx, Cy, 0.0])

        L1 = float(np.linalg.norm(T_pt - P0))
        theta_top = 5 * np.pi / 2  # first pi/2 reached after theta_T
        s_top = (L1 + R * (theta_top - theta_T)) / (L1 + 2 * np.pi * R)

        # invisible, uniformly sampled motion path: incline + full loop
        spacing = 0.04
        n1 = max(2, int(L1 / spacing))
        n2 = max(2, int(2 * np.pi * R / spacing))
        pts = []
        for i in range(n1):
            t = i / (n1 - 1)
            p = P0 + (T_pt - P0) * t
            pts.append([p[0], p[1], 0.0])
        for i in range(1, n2 + 1):
            t = i / n2
            th = theta_T + t * 2 * np.pi
            pts.append([Cx + R * np.cos(th), Cy + R * np.sin(th), 0.0])
        path = VMobject()
        path.set_points_as_corners(pts)
        path.set_stroke(opacity=0)

        # ================= beat 1: title =================
        title = serif("Energi \\& Loop-the-Loop", size=60)
        stmt1 = serif("Bola meluncur dari ketinggian $h$, melewati loop $R = 0{,}5$ m.",
                      size=30, color=GRAY)
        stmt2 = serif("Berapa $h$ minimum agar tidak jatuh di puncak?",
                      size=30, color=GRAY)
        stmt1.next_to(title, DOWN, buff=0.4)
        stmt2.next_to(stmt1, DOWN, buff=0.2)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(stmt1), FadeIn(stmt2), run_time=1.0)
        self.wait(1.5)

        # ================= beat 2: the track =================
        header = serif("Lintasan", size=32)
        header.to_corner(UL, buff=0.55)
        incline = Line(P0_3, T3, color=WHITE, stroke_width=5)
        loop = Circle(radius=R, color=TEAL, stroke_width=5).move_to(C3)
        rad_line = Line(C3, C3 + np.array([R, 0, 0]), color=GRAY,
                        stroke_width=2)
        r_lab = MathTex(r"R = 0{,}5\ \text{m}", font_size=28, color=GRAY)
        r_lab.next_to(rad_line, DOWN, buff=0.15)

        y_top, y_bot = P0[1], Cy - R
        dash_top = DashedLine([P0[0], y_top, 0], [0.8, y_top, 0],
                              color=GRAY, stroke_width=2, dash_length=0.12)
        dash_bot = DashedLine([P0[0], y_bot, 0], [0.8, y_bot, 0],
                              color=GRAY, stroke_width=2, dash_length=0.12)
        h_arrow = DoubleArrow([-5.3, y_bot, 0], [-5.3, y_top, 0],
                              color=YELLOW, stroke_width=4, buff=0.05)
        h_lab = MathTex(r"h = ?", font_size=36, color=YELLOW)
        h_lab.next_to(h_arrow, LEFT, buff=0.2)

        self.play(
            FadeOut(title, run_time=0.8),
            FadeOut(stmt1, run_time=0.8),
            FadeOut(stmt2, run_time=0.8),
            FadeIn(header, run_time=0.6),
            Create(incline, run_time=1.5),
            Create(loop, run_time=2.0),
        )
        self.play(Create(rad_line, run_time=0.6), FadeIn(r_lab, run_time=0.6))
        self.wait(0.5)
        self.play(Create(dash_top, run_time=0.6), Create(dash_bot, run_time=0.6),
                  Create(h_arrow, run_time=0.8), FadeIn(h_lab, run_time=0.6))
        self.wait(1.0)

        strat = serif("Strategi: (1) syarat di puncak, (2) kekekalan energi.",
                      size=28, color=GRAY)
        strat.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(strat), run_time=0.8)
        self.wait(1.5)
        self.play(FadeOut(strat), run_time=0.6)

        # ball (updater-driven; added, never faded)
        s = ValueTracker(0.0)
        ball = Dot(point=path.point_from_proportion(0.0), radius=0.14,
                   color=YELLOW)
        ball.add_updater(
            lambda m: m.move_to(path.point_from_proportion(s.get_value())))
        self.add(ball)
        self.wait(1.0)

        # ================= beat 3: slide to the top =================
        self.play(s.animate.set_value(s_top), run_time=11, rate_func=linear)
        self.wait(1.0)

        # ================= beat 4: FBD at the top =================
        top_pt = np.array([Cx, Cy + R, 0.0])
        mg_arr = Arrow(top_pt + np.array([-0.13, -0.15, 0]),
                       top_pt + np.array([-0.13, -1.05, 0]),
                       color=RED, stroke_width=6, buff=0,
                       max_tip_length_to_length_ratio=0.25)
        n_arr = Arrow(top_pt + np.array([0.13, -0.15, 0]),
                      top_pt + np.array([0.13, -0.65, 0]),
                      color=BLUE, stroke_width=6, buff=0,
                      max_tip_length_to_length_ratio=0.3)
        mg_lab = MathTex("mg", font_size=32, color=RED)
        mg_lab.next_to(mg_arr, LEFT, buff=0.15)
        n_lab = MathTex("N", font_size=32, color=BLUE)
        n_lab.next_to(n_arr, RIGHT, buff=0.15)

        fbd_eq = MathTex(r"N + mg = \frac{mv^2}{R}", font_size=42)
        fbd_eq.set_color_by_tex("N", BLUE)
        fbd_eq.set_color_by_tex("mg", RED)
        fbd_eq.move_to(np.array([5.0, 2.3, 0.0]))
        t_key = serif("Tepat tidak jatuh $\\Rightarrow N = 0$", size=28)
        t_key.move_to(np.array([5.0, 1.5, 0.0]))
        e_v2 = MathTex(r"v^2 = gR", font_size=48, color=YELLOW)
        e_v2.move_to(np.array([5.0, 0.75, 0.0]))
        v2_box = SurroundingRectangle(e_v2, color=YELLOW, buff=0.12,
                                      stroke_width=2)

        self.play(Create(mg_arr, run_time=0.8), FadeIn(mg_lab, run_time=0.6))
        self.wait(0.5)
        self.play(Create(n_arr, run_time=0.8), FadeIn(n_lab, run_time=0.6))
        self.wait(0.5)
        self.play(Write(fbd_eq), run_time=1.2)
        self.wait(0.8)
        self.play(FadeIn(t_key), run_time=0.8)
        self.wait(0.8)
        self.play(Write(e_v2), run_time=1.0)
        self.play(Create(v2_box), run_time=0.6)
        self.wait(1.5)

        # ================= beat 5: energy =================
        self.play(
            FadeOut(mg_arr, run_time=0.6),
            FadeOut(n_arr, run_time=0.6),
            FadeOut(mg_lab, run_time=0.6),
            FadeOut(n_lab, run_time=0.6),
            FadeOut(fbd_eq, run_time=0.6),
            FadeOut(t_key, run_time=0.6),
            FadeOut(e_v2, run_time=0.6),
            FadeOut(v2_box, run_time=0.6),
        )
        self.wait(0.5)
        e1 = MathTex(r"mgh = mg(2R) + \frac{1}{2}mv^2", font_size=44)
        e1.move_to(np.array([-2.8, -3.0, 0.0]))
        intuit = serif("Butuh laju di puncak, jadi $h > 2R$", size=20,
                       color=GRAY)
        intuit.move_to(np.array([5.3, -1.2, 0.0]))
        self.play(Write(e1), run_time=1.4)
        self.play(FadeIn(intuit), run_time=0.8)
        self.wait(1.0)
        e2 = MathTex(r"mgh = 2mgR + \frac{1}{2}m(gR)", font_size=44)
        e2.move_to(e1, aligned_edge=LEFT)
        self.play(FadeTransform(e1, e2), run_time=1.2)
        self.wait(1.0)
        e3 = MathTex(r"h = 2{,}5R", font_size=48)
        e3.move_to(e2, aligned_edge=LEFT)
        self.play(FadeTransform(e2, e3), run_time=1.2)
        self.wait(1.0)
        e4 = MathTex(r"h = 1{,}25\ \text{m}", font_size=52, color=YELLOW)
        e4.move_to(e3, aligned_edge=LEFT)
        self.play(FadeTransform(e3, e4), run_time=1.2)
        self.wait(1.5)

        # ================= beat 6: complete the loop =================
        self.play(FadeOut(intuit), run_time=0.6)
        self.wait(0.5)
        self.play(s.animate.set_value(1.0), run_time=5, rate_func=linear)
        self.wait(1.0)

        # ================= beat 7: answer + options =================
        self.play(
            FadeOut(header, run_time=0.6),
            FadeOut(dash_top, run_time=0.6),
            FadeOut(dash_bot, run_time=0.6),
            FadeOut(h_arrow, run_time=0.6),
            FadeOut(h_lab, run_time=0.6),
            FadeOut(rad_line, run_time=0.6),
            FadeOut(r_lab, run_time=0.6),
        )
        big_ans = MathTex(r"h = 1{,}25\ \text{m}", font_size=64,
                          color=YELLOW)
        big_ans.move_to(np.array([0.0, 2.2, 0.0]))
        self.play(FadeTransform(e4, big_ans), run_time=1.2)
        self.wait(0.8)
        opts = VGroup(
            MathTex(r"(A)\ 0{,}50\ \text{m}", font_size=32),
            MathTex(r"(B)\ 0{,}75\ \text{m}", font_size=32),
            MathTex(r"(C)\ 1{,}00\ \text{m}", font_size=32),
            MathTex(r"(D)\ 1{,}25\ \text{m}", font_size=32),
            MathTex(r"(E)\ 1{,}50\ \text{m}", font_size=32),
        ).arrange(RIGHT, buff=0.5)
        opts.move_to(np.array([0.0, -2.8, 0.0]))
        self.play(FadeIn(opts, run_time=1.0))
        self.wait(0.5)
        box = SurroundingRectangle(opts[3], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=0.8),
                  opts[3].animate.set_color(YELLOW), run_time=0.8)
        self.wait(2.5)
