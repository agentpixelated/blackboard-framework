import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from visual_system3 import *

config.background_color = BG

# ---- semantic colors (one concept = one color, whole video) ----
WATER_FILL = "#14384a"   # dark muted blue for water bodies
WOOD_FILL = RECT_FILL    # block / piston machinery fill (dark teal)
MACHINE = "#666666"


def title(text):
    t = serif(text, size=40, color=WHITE)
    t.to_corner(UL, buff=0.45)
    return t


def big_formula(parts, colors, size=72):
    m = MathTex(*parts, font_size=size)
    for idx, c in colors.items():
        m[idx].set_color(c)
    return m


class FluidaAcrossCases(Scene):
    def construct(self):
        self.act1_hidrostatis()
        self.act2_pascal()
        self.act3_archimedes()
        self.act4_kontinuitas()
        self.act5_torricelli()
        self.closing()

    # ---------- helpers ----------
    def wipe(self, run_time=0.9):
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=run_time)

    # ---------- ACT 1: Hydrostatic pressure ----------
    def act1_hidrostatis(self):
        t = title("1. Tekanan Hidrostatis: Penyelam")
        water = Rectangle(width=4.6, height=4.8, color=BLUE, stroke_width=2,
                          fill_color=WATER_FILL, fill_opacity=0.85)
        water.move_to([-3.9, -0.8, 0])
        surface = Line([-6.2, 1.6, 0], [-1.6, 1.6, 0], color=BLUE, stroke_width=4)
        surf_label = serif("permukaan air", size=24, color=BLUE)
        surf_label.next_to(surface, UP, buff=0.12).shift(LEFT * 0.9)
        self.play(FadeIn(t), Create(water), Create(surface),
                  FadeIn(surf_label), run_time=1.2)

        dot = Dot(point=[-3.9, 1.45, 0], radius=0.1, color=YELLOW)
        dlabel = serif("penyelam", size=24, color=YELLOW)
        dlabel.next_to(dot, RIGHT, buff=0.18)
        diver = VGroup(dot, dlabel)
        arrow = Arrow([-5.7, 1.6, 0], [-5.7, 1.45, 0], color=YELLOW,
                      stroke_width=3, buff=0.05)
        h_lab = MathTex("h", "=", "0", "\\ \\mathrm{m}", font_size=34, color=YELLOW)
        h_lab.next_to(arrow, RIGHT, buff=0.15)
        self.play(FadeIn(diver), Create(arrow), FadeIn(h_lab), run_time=0.9)

        gauge_lab = serif("tekanan terukur:", size=30)
        gauge_lab.move_to([3.4, 2.3, 0])
        gauge = MathTex("P", "=", "1{,}0", "\\times", "10^{5}", "\\ \\mathrm{Pa}",
                        font_size=54)
        gauge[0].set_color(YELLOW)
        gauge.move_to([3.4, 1.55, 0])
        self.play(FadeIn(gauge_lab), Write(gauge), run_time=1.0)
        self.wait(0.5)

        # --- brief derivation: rho g h from weight of the column ---
        cap = serif("dari berat kolom air di atasnya:", size=28, color=GRAY)
        cap.move_to([3.4, 0.75, 0])
        d1 = MathTex("W", "=", "\\rho", "A", "h", "g", font_size=42)
        d1[2].set_color(BLUE)
        d1.move_to([3.4, 0.05, 0])
        d2 = MathTex("P", "=", "\\frac{W}{A}", "=",
                     "\\frac{\\rho A h g}{A}", font_size=42)
        d2.move_to([3.4, 0.05, 0])
        d3 = MathTex("P", "=", "\\rho", "g", "h", font_size=48)
        d3[0].set_color(YELLOW)
        d3[2].set_color(BLUE)
        d3.move_to([3.4, 0.05, 0])
        self.play(FadeIn(cap), Write(d1), run_time=1.0)
        self.play(FadeTransform(d1, d2), run_time=1.0)
        self.play(FadeTransform(d2, d3), run_time=1.0)

        form = big_formula(["P", "=", "P_0", "+", "\\rho", "g", "h"],
                           {0: YELLOW, 4: BLUE, 6: YELLOW}, size=72)
        form.move_to([3.4, -1.15, 0])
        self.play(Write(form), run_time=1.1)
        self.wait(0.4)

        # --- diver descends: h = 5 m, then h = 10 m ---
        for y_new, h_txt, p_txt in [(-0.8, "5", "1{,}5"), (-3.0, "10", "2{,}0")]:
            new_arrow = Arrow([-5.7, 1.6, 0], [-5.7, y_new, 0], color=YELLOW,
                              stroke_width=3, buff=0.05)
            new_h = MathTex("h", "=", h_txt, "\\ \\mathrm{m}",
                            font_size=34, color=YELLOW)
            new_h.next_to(new_arrow, RIGHT, buff=0.15)
            new_g = MathTex("P", "=", p_txt, "\\times", "10^{5}", "\\ \\mathrm{Pa}",
                            font_size=54)
            new_g[0].set_color(YELLOW)
            new_g.move_to([3.4, 1.55, 0])
            self.play(diver.animate.shift(DOWN * (dot.get_y() - y_new)),
                      Transform(arrow, new_arrow),
                      FadeTransform(h_lab, new_h),
                      FadeTransform(gauge, new_g), run_time=1.4)
            h_lab, gauge = new_h, new_g
            self.wait(0.4)

        sub = MathTex("P", "=", "10^{5}", "+", "(1000)(10)(10)", "=",
                      "2", "\\times", "10^{5}", "\\ \\mathrm{Pa}", font_size=40)
        sub[0].set_color(YELLOW)
        sub.move_to([3.4, -2.5, 0])
        self.play(Write(sub), run_time=1.1)
        self.wait(1.2)
        self.wipe()

    # ---------- ACT 2: Pascal ----------
    def act2_pascal(self):
        t = title("2. Hukum Pascal: Dongkrak Hidrolik")
        walls = VGroup(
            Line([-5.8, 0.2, 0], [-5.8, -2.3, 0], color=GRAY, stroke_width=3),
            Line([-4.8, 0.2, 0], [-4.8, -2.3, 0], color=GRAY, stroke_width=3),
            Line([1.0, 0.2, 0], [1.0, -2.3, 0], color=GRAY, stroke_width=3),
            Line([4.6, 0.2, 0], [4.6, -2.3, 0], color=GRAY, stroke_width=3),
            Line([-5.8, -3.1, 0], [4.6, -3.1, 0], color=GRAY, stroke_width=3),
            Line([-5.8, -2.3, 0], [-5.8, -3.1, 0], color=GRAY, stroke_width=3),
            Line([4.6, -2.3, 0], [4.6, -3.1, 0], color=GRAY, stroke_width=3),
        )

        def fluid(left_h, right_h):
            lc = Rectangle(width=1.0, height=left_h, stroke_width=0,
                           fill_color=WATER_FILL, fill_opacity=0.9)
            lc.move_to([-5.3, -2.3 + left_h / 2, 0])
            ch = Rectangle(width=10.4, height=0.8, stroke_width=0,
                           fill_color=WATER_FILL, fill_opacity=0.9)
            ch.move_to([-0.6, -2.7, 0])
            rc = Rectangle(width=3.6, height=right_h, stroke_width=0,
                           fill_color=WATER_FILL, fill_opacity=0.9)
            rc.move_to([2.8, -2.3 + right_h / 2, 0])
            return VGroup(lc, ch, rc)

        fl = fluid(1.1, 1.1)
        fl_after = fluid(0.2, 1.35)

        piston_l = Rectangle(width=1.0, height=0.45, color=WHITE, stroke_width=2,
                             fill_color=MACHINE, fill_opacity=1)
        piston_l.move_to([-5.3, -0.98, 0])
        f_arrow = Arrow([-5.3, 0.75, 0], [-5.3, -0.6, 0], color=YELLOW,
                        stroke_width=4, buff=0.05)
        f_lab = MathTex("F_1", "=", "100", "\\ \\mathrm{N}", font_size=36,
                        color=YELLOW)
        f_lab.next_to(f_arrow, RIGHT, buff=0.15)
        left_press = VGroup(piston_l, f_arrow, f_lab)

        piston_r = Rectangle(width=3.6, height=0.45, color=WHITE, stroke_width=2,
                             fill_color=MACHINE, fill_opacity=1)
        piston_r.move_to([2.8, -0.98, 0])
        body = Rectangle(width=3.0, height=0.6, color=WHITE, stroke_width=2,
                         fill_color=WOOD_FILL, fill_opacity=1)
        body.move_to([2.8, 0.05, 0])
        cabin = Rectangle(width=1.6, height=0.5, color=WHITE, stroke_width=2,
                          fill_color=WOOD_FILL, fill_opacity=1)
        cabin.move_to([2.6, 0.6, 0])
        w1 = Circle(radius=0.26, color=WHITE, stroke_width=2,
                    fill_color=BLACK, fill_opacity=1).move_to([1.85, -0.62, 0])
        w2 = Circle(radius=0.26, color=WHITE, stroke_width=2,
                    fill_color=BLACK, fill_opacity=1).move_to([3.75, -0.62, 0])
        car = VGroup(body, cabin, w1, w2)
        car_lab = serif("mobil 200 kg", size=28)
        car_lab.next_to(cabin, RIGHT, buff=0.2)
        right_lift = VGroup(piston_r, car, car_lab)

        a1_lab = MathTex("A_1", "=", "10", "\\ \\mathrm{cm}^2", font_size=32,
                         color=GREEN)
        a1_lab.move_to([-5.3, -3.6, 0])
        a2_lab = MathTex("A_2", "=", "200", "\\ \\mathrm{cm}^2", font_size=32,
                         color=GREEN)
        a2_lab.move_to([2.8, -3.6, 0])

        self.play(FadeIn(t), Create(walls), FadeIn(fl), run_time=1.2)
        self.play(FadeIn(left_press), FadeIn(right_lift),
                  FadeIn(a1_lab), FadeIn(a2_lab), run_time=1.0)
        self.wait(0.4)

        form = MathTex("\\frac{F_1}{A_1}", "=", "\\frac{F_2}{A_2}",
                       font_size=58)
        form.set_color_by_tex("F_2", YELLOW)
        form.move_to([1.1, 2.82, 0])
        self.play(Write(form), run_time=1.0)

        self.play(left_press.animate.shift(DOWN * 0.9),
                  Transform(fl, fl_after),
                  right_lift.animate.shift(UP * 0.25), run_time=1.6)
        self.wait(0.3)

        sub = MathTex("F_2", "=", "100", "\\times", "\\frac{200}{10}", "=",
                      "2000", "\\ \\mathrm{N}", font_size=42)
        sub[0].set_color(YELLOW)
        sub[6].set_color(YELLOW)
        sub.move_to([0.4, 1.85, 0])
        check = MathTex("W", "=", "200", "\\times", "10", "=", "2000",
                        "\\ \\mathrm{N}", "\\ \\Rightarrow\\ \\text{terangkat}",
                        font_size=34)
        check.move_to([-1.3, 1.22, 0])
        vol1 = MathTex("A_1", "x_1", "=", "A_2", "x_2", font_size=32,
                       color=GREEN)
        vol1.move_to([-2.45, 0.78, 0])
        vol2 = MathTex("x_2", "=", "20", "\\times", "\\frac{10}{200}", "=",
                       "1", "\\ \\mathrm{cm}", font_size=32, color=GREEN)
        vol2.move_to([-2.45, 0.02, 0])
        self.play(Write(sub), run_time=1.0)
        self.play(FadeIn(check), run_time=0.8)
        self.play(FadeIn(vol1), FadeIn(vol2), run_time=0.8)
        self.wait(1.2)
        self.wipe()

    # ---------- ACT 3: Archimedes ----------
    def act3_archimedes(self):
        t = title("3. Archimedes: Balok Kayu Terapung")
        water = Rectangle(width=5.0, height=3.8, color=BLUE, stroke_width=2,
                          fill_color=WATER_FILL, fill_opacity=0.85)
        water.move_to([-3.8, -1.4, 0])
        water_after = Rectangle(width=5.0, height=4.15, color=BLUE,
                                stroke_width=2, fill_color=WATER_FILL,
                                fill_opacity=0.85)
        water_after.move_to([-3.8, -1.225, 0])
        block = Rectangle(width=2.2, height=2.2, color=RECT_EDGE, stroke_width=2,
                          fill_color=WOOD_FILL, fill_opacity=1)
        block.move_to([-3.8, 2.3, 0])
        b_lab = serif("kayu", size=26)
        b_lab.move_to(block.get_center())
        b_rho = MathTex("\\rho", "=", "600", "\\ \\mathrm{kg/m}^3", font_size=26)
        b_rho.next_to(b_lab, DOWN, buff=0.08)
        block_g = VGroup(block, b_lab, b_rho)
        self.play(FadeIn(t), Create(water), FadeIn(block_g), run_time=1.2)
        self.wait(0.3)

        # block descends into the water; water level rises
        self.play(block_g.animate.move_to([-3.8, 0.63, 0]),
                  Transform(water, water_after), run_time=1.6)
        dash = DashedLine([-5.1, 0.85, 0], [-2.5, 0.85, 0], color=WHITE,
                          stroke_width=2)
        sub_lab = serif("60\\% tercelup (6 cm)", size=24, color=YELLOW)
        sub_lab.move_to([-1.5, 1.18, 0])
        self.play(Create(dash), FadeIn(sub_lab), run_time=0.8)

        # pressure arrows: longer at the bottom, shorter at the top
        a_down = Arrow([-3.8, 2.15, 0], [-3.8, 1.8, 0], color=BLUE,
                       stroke_width=4, buff=0.02)
        a_up = Arrow([-3.8, -1.05, 0], [-3.8, -0.35, 0], color=YELLOW,
                     stroke_width=4, buff=0.02)
        self.play(Create(a_down), Create(a_up), run_time=0.8)

        cap = serif("tekanan di bawah lebih besar dari di atas:", size=28,
                    color=GRAY)
        cap.move_to([3.3, 2.5, 0])
        e1 = MathTex("\\Delta", "P", "=", "\\rho", "g", "\\Delta", "h",
                     font_size=42)
        e1[3].set_color(BLUE)
        e1.move_to([3.3, 1.8, 0])
        e2 = MathTex("F_A", "=", "\\Delta", "P", "\\cdot", "A", "=", "\\rho",
                     "g", "V_{tercelup}", font_size=42)
        e2[0].set_color(YELLOW)
        e2[7].set_color(BLUE)
        e2.move_to([3.3, 1.8, 0])
        self.play(FadeIn(cap), Write(e1), run_time=1.0)
        self.play(FadeTransform(e1, e2), run_time=1.0)

        form = big_formula(["F_A", "=", "\\rho_{fluida}", "g", "V_{tercelup}"],
                           {0: YELLOW, 2: BLUE}, size=64)
        form.move_to([3.3, 0.55, 0])
        self.play(Write(form), run_time=1.0)

        sub = MathTex("F_A", "=", "1000", "\\times", "10", "\\times",
                      "0{,}6", "\\times", "10^{-3}", "=", "6",
                      "\\ \\mathrm{N}", font_size=38)
        sub[0].set_color(YELLOW)
        sub[10].set_color(YELLOW)
        sub.move_to([3.3, -0.55, 0])
        check = MathTex("W", "=", "0{,}6", "\\times", "10", "=", "6",
                        "\\ \\mathrm{N}", "=", "F_A", "\\ \\Rightarrow\\ ",
                        "\\text{terapung}", font_size=36)
        check.move_to([3.3, -1.45, 0])
        self.play(Write(sub), run_time=1.0)
        self.play(FadeIn(check), run_time=0.8)
        self.wait(1.2)
        self.wipe()

    # ---------- ACT 4: Continuity ----------
    def act4_kontinuitas(self):
        t = title("4. Kontinuitas: Pipa Menyempit")
        pts = [[-6.6, 1.2, 0], [-0.8, 1.2, 0], [0.8, 0.5, 0], [6.6, 0.5, 0],
               [6.6, -0.5, 0], [0.8, -0.5, 0], [-0.8, -1.2, 0], [-6.6, -1.2, 0]]
        pipe = Polygon(*pts, color=BLUE, stroke_width=2,
                       fill_color=WATER_FILL, fill_opacity=0.55)
        a1 = MathTex("A_1", "=", "20", "\\ \\mathrm{cm}^2", font_size=34,
                     color=GREEN)
        a1.move_to([-4.3, 1.85, 0])
        v1 = MathTex("v_1", "=", "1{,}5", "\\ \\mathrm{m/s}", font_size=34)
        v1.move_to([-4.3, -1.85, 0])
        a2 = MathTex("A_2", "=", "5", "\\ \\mathrm{cm}^2", font_size=34,
                     color=GREEN)
        a2.move_to([3.9, 1.15, 0])
        v2q = MathTex("v_2", "=", "?", font_size=40, color=YELLOW)
        v2q.move_to([3.9, -1.25, 0])
        self.play(FadeIn(t), Create(pipe), FadeIn(a1), FadeIn(v1),
                  FadeIn(a2), FadeIn(v2q), run_time=1.2)

        dots = VGroup(*[Dot(point=[x, 0, 0], radius=0.09, color=WHITE)
                        for x in (-6.0, -5.0, -4.0, -3.0, -2.0)])
        self.play(FadeIn(dots), run_time=0.6)
        # slow through the wide part...
        self.play(dots.animate.shift(RIGHT * 2.2), run_time=2.2)
        # ...then fast and stretched out through the narrow part
        targets = [1.8, 2.9, 4.0, 5.1, 6.2]
        self.play(*[d.animate.move_to([tx, 0, 0])
                    for d, tx in zip(dots, targets)], run_time=1.0)
        self.wait(0.3)

        form = big_formula(["A_1", "v_1", "=", "A_2", "v_2"],
                           {0: GREEN, 3: GREEN, 4: YELLOW}, size=68)
        form.move_to([0, 3.0, 0])
        self.play(Write(form), run_time=1.0)

        v2 = MathTex("v_2", "=", "6", "\\ \\mathrm{m/s}", font_size=40,
                     color=YELLOW)
        v2.move_to([3.9, -1.25, 0])
        sub = MathTex("v_2", "=", "\\frac{A_1 v_1}{A_2}", "=",
                      "\\frac{20 \\times 1{,}5}{5}", "=", "6",
                      "\\ \\mathrm{m/s}", font_size=44)
        sub[0].set_color(YELLOW)
        sub[6].set_color(YELLOW)
        sub.move_to([0, -3.0, 0])
        self.play(FadeTransform(v2q, v2), Write(sub), run_time=1.1)
        self.wait(1.2)
        self.wipe()

    # ---------- ACT 5: Bernoulli / Torricelli ----------
    def act5_torricelli(self):
        t = title("5. Bernoulli: Tangki Bocor (Torricelli)")
        ground = Line([-6.9, -2.13, 0], [6.9, -2.13, 0], color=GRAY,
                      stroke_width=2)
        walls = VGroup(
            Line([-6.4, 2.7, 0], [-6.4, -1.0, 0], color=GRAY, stroke_width=3),
            Line([-2.6, 2.7, 0], [-2.6, -0.72, 0], color=GRAY, stroke_width=3),
            Line([-2.6, -0.88, 0], [-2.6, -1.0, 0], color=GRAY, stroke_width=3),
            Line([-6.4, -1.0, 0], [-2.6, -1.0, 0], color=GRAY, stroke_width=3),
            Line([-6.0, -1.0, 0], [-6.0, -2.13, 0], color=GRAY, stroke_width=3),
            Line([-3.0, -1.0, 0], [-3.0, -2.13, 0], color=GRAY, stroke_width=3),
        )
        water = Rectangle(width=3.7, height=3.15, color=BLUE, stroke_width=2,
                          fill_color=WATER_FILL, fill_opacity=0.85)
        water.move_to([-4.5, 0.625, 0])
        hole = Dot(point=[-2.6, -0.8, 0], radius=0.08, color=YELLOW)
        hole_lab = serif("lubang", size=24, color=YELLOW)
        hole_lab.next_to(hole, RIGHT, buff=0.2).shift(UP * 0.3)
        self.play(FadeIn(t), Create(ground), Create(walls), Create(water),
                  FadeIn(hole), FadeIn(hole_lab), run_time=1.2)

        h_arrow = Arrow([-3.15, 2.2, 0], [-3.15, -0.8, 0], color=YELLOW,
                        stroke_width=3, buff=0.05)
        h_lab = MathTex("h", "=", "1{,}8", "\\ \\mathrm{m}", font_size=32,
                        color=YELLOW)
        h_lab.next_to(h_arrow, RIGHT, buff=0.12)
        self.play(Create(h_arrow), FadeIn(h_lab), run_time=0.8)

        # Bernoulli, briefly: surface (slow, height h) vs hole (fast, height 0)
        chain = MathTex("P_0", "+", "\\rho", "g", "h", "+", "0", "=", "P_0",
                        "+", "0", "+", "\\frac{1}{2}", "\\rho", "v^2",
                        font_size=34)
        chain[2].set_color(BLUE)
        chain[12].set_color(BLUE)
        chain.move_to([3.2, 3.08, 0])
        self.play(Write(chain), run_time=1.2)

        form = big_formula(["v", "=", "\\sqrt{2", "g", "h}"],
                           {0: YELLOW, 4: YELLOW}, size=72)
        form.move_to([3.4, 2.0, 0])
        self.play(Write(form), run_time=1.0)

        sub = MathTex("v", "=", "\\sqrt{2 \\times 10 \\times 1{,}8}", "=",
                      "\\sqrt{36}", "=", "6", "\\ \\mathrm{m/s}", font_size=40)
        sub[0].set_color(YELLOW)
        sub[6].set_color(YELLOW)
        sub.move_to([3.4, 1.02, 0])
        self.play(Write(sub), run_time=1.0)

        # the jet: parabola
        jet = ParametricFunction(
            lambda s: np.array([-2.6 + 4.0 * s, -0.8 - 1.33 * s * s, 0]),
            t_range=[0, 1], color=BLUE, stroke_width=4)
        land = Dot(point=[1.4, -2.13, 0], radius=0.09, color=YELLOW)
        self.play(Create(jet), run_time=1.4)
        self.play(FadeIn(land), run_time=0.4)

        fall = DashedLine([1.4, -0.8, 0], [1.4, -2.13, 0], color=GRAY,
                          stroke_width=2)
        fall_lab = MathTex("0{,}8", "\\ \\mathrm{m}", font_size=28, color=GRAY)
        fall_lab.next_to(fall, RIGHT, buff=0.12)
        x_arrow = Arrow([-2.6, -2.5, 0], [1.4, -2.5, 0], color=YELLOW,
                        stroke_width=3, buff=0.05)
        x_lab = MathTex("x", "=", "2{,}4", "\\ \\mathrm{m}", font_size=32,
                        color=YELLOW)
        x_lab.next_to(x_arrow, DOWN, buff=0.12)
        rng1 = MathTex("t", "=", "\\sqrt{\\frac{2 \\times 0{,}8}{10}}", "=",
                       "0{,}4", "\\ \\mathrm{s}", font_size=36)
        rng1.move_to([3.4, 0.15, 0])
        rng2 = MathTex("x", "=", "v", "t", "=", "6", "\\times", "0{,}4", "=",
                       "2{,}4", "\\ \\mathrm{m}", font_size=36)
        rng2[9].set_color(YELLOW)
        rng2.move_to([3.4, -0.6, 0])
        self.play(Create(fall), FadeIn(fall_lab), Create(x_arrow),
                  FadeIn(x_lab), run_time=0.9)
        self.play(Write(rng1), run_time=0.9)
        self.play(Write(rng2), run_time=0.9)
        self.wait(1.2)
        self.wipe()

    # ---------- closing ----------
    def closing(self):
        head = serif("Lima rumus, satu fluida: semua dari hukum dasar.",
                     size=38)
        head.move_to([0, 3.1, 0])
        lines = [
            MathTex("P", "=", "P_0", "+", "\\rho", "g", "h", font_size=40),
            MathTex("\\frac{F_1}{A_1}", "=", "\\frac{F_2}{A_2}", font_size=40),
            MathTex("F_A", "=", "\\rho", "g", "V_{tercelup}", font_size=40),
            MathTex("A_1", "v_1", "=", "A_2", "v_2", font_size=40),
            MathTex("v", "=", "\\sqrt{2gh}", font_size=40),
        ]
        for i, ln in enumerate(lines):
            ln.move_to([0, 2.0 - i * 1.05, 0])
        grp = VGroup(head, *lines)
        self.play(FadeIn(head), run_time=0.8)
        self.play(*[FadeIn(ln) for ln in lines], run_time=1.2)
        self.wait(2.0)
        self.play(FadeOut(grp), run_time=1.0)
