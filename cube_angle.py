from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

# ---- Oblique projection: screen = (x + 0.45 z, y - 0.45 z)
# 3Blue1Brown-style transparent wireframe: all 12 edges visible, thin
# elegant strokes, no dashes, no fills. Color grammar: EG blue, AG yellow.
K = 1.6
CX, CY = 2.7, -0.3

def proj(p):
    x, y, z = p
    return np.array([CX + K * (x + 0.45 * z), CY + K * (y - 0.45 * z), 0.0])

C0 = np.array([CX, CY, 0.0])
WIRE = "#D8D8D8"


class CubeAngle(Scene):
    def construct(self):
        # ---------- vertices: ABCD bottom, EFGH top, E above A etc. ----------
        A3 = (-1, -1, -1); B3 = (1, -1, -1); C3 = (1, -1, 1); D3 = (-1, -1, 1)
        E3 = (-1, 1, -1);  F3 = (1, 1, -1);  G3 = (1, 1, 1);  H3 = (-1, 1, 1)
        A, B, C, D, E, F, G, H = map(proj, (A3, B3, C3, D3, E3, F3, G3, H3))

        top_pairs = [(E, F), (F, G), (G, H), (H, E)]
        rest_pairs = [(A, B), (B, C), (C, D), (D, A),
                      (A, E), (B, F), (C, G), (D, H)]
        top_edges = VGroup(*[Line(p, q, color=WIRE, stroke_width=4)
                             for p, q in top_pairs])
        rest_edges = VGroup(*[Line(p, q, color=WIRE, stroke_width=4)
                              for p, q in rest_pairs])
        edges = VGroup(top_edges, rest_edges)

        # ---------- Beat 1: title + problem statement ----------
        title = serif("Sudut antara Garis dan Bidang", size=60)
        stmt = serif(r"Kubus $ABCD.EFGH$: sudut antara garis $AG$ dan bidang $EFGH$"
                     r" adalah $\alpha$. Tentukan $\cos\alpha$.", size=32, color=GRAY)
        stmt.next_to(title, DOWN, buff=0.45)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(stmt), run_time=0.8)
        self.wait(1.2)

        # ---------- Beat 2: glass cube draws itself ----------
        header = serif(r"Sudut garis $AG$ terhadap bidang $EFGH$", size=34)
        header.to_corner(UL, buff=0.55)
        self.play(
            FadeOut(title, run_time=0.8),
            FadeOut(stmt, run_time=0.8),
            Create(edges, run_time=1.6),
            FadeIn(header, run_time=0.6),
        )

        labels = VGroup()
        for letter, v3 in (("A", A3), ("B", B3), ("C", C3), ("D", D3),
                           ("E", E3), ("F", F3), ("G", G3), ("H", H3)):
            s = proj(v3)
            d = s - C0
            d = d / np.linalg.norm(d)
            lab = MathTex(letter, font_size=34).move_to(s + d * 0.55)
            labels.add(lab)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.07),
                  run_time=1.4)
        self.wait(0.6)

        # ---------- Beat 3: the plane EFGH lights up blue ----------
        plabel = serif(r"bidang $EFGH$", size=30, color=BLUE)
        plabel.move_to(np.array([6.0, 1.5, 0.0]))
        self.play(
            *[e.animate.set_color(BLUE).set_stroke_width(6) for e in top_edges],
            FadeIn(plabel, run_time=1.0),
            run_time=1.2,
        )
        self.wait(0.8)

        # ---------- Beat 4: draw AG ----------
        ag = Line(A, G, color=YELLOW, stroke_width=7)
        aglabel = serif(r"garis $AG$", size=30, color=YELLOW)
        aglabel.move_to((A + G) / 2 + np.array([1.1, -0.65, 0.0]))
        self.play(Create(ag, run_time=1.2), FadeIn(aglabel, run_time=0.9))
        self.wait(0.8)

        # ---------- Beat 5: the projection ----------
        s1 = serif(r"Proyeksi $AG$ pada bidang $EFGH$ adalah $EG$", size=28)
        s1.move_to(np.array([-3.55, 2.55, 0.0]))
        self.play(FadeIn(s1), run_time=0.8)
        dot = Dot(A, color=YELLOW, radius=0.11)
        self.add(dot)
        self.play(dot.animate.move_to(E), run_time=0.9)
        self.play(FadeOut(dot), run_time=0.3)
        eg = Line(E, G, color=BLUE, stroke_width=6)
        self.play(Create(eg, run_time=0.9))

        u1 = A - G; u1 = u1 / np.linalg.norm(u1)
        u2 = E - G; u2 = u2 / np.linalg.norm(u2)
        alpha3 = float(np.arccos(np.clip(np.dot(u1, u2), -1, 1)))
        r = 0.6
        arc = ParametricFunction(
            lambda t: G + r * (np.cos(t) * u1 + np.sin(t) * u2),
            t_range=[0, alpha3, 0.02], color=YELLOW, stroke_width=5)
        bis = u1 + u2; bis = bis / np.linalg.norm(bis)
        alphalabel = MathTex(r"\alpha", font_size=40, color=YELLOW)
        alphalabel.move_to(G + bis * (r + 0.45))
        self.play(Create(arc, run_time=0.7), FadeIn(alphalabel, run_time=0.6))

        e_alpha = MathTex(r"\alpha", r"= \angle AGE", font_size=48)
        e_alpha[0].set_color(YELLOW)
        e_alpha.next_to(s1, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(Write(e_alpha), run_time=1.0)
        self.wait(0.8)

        # ---------- Beat 6: justification + exact 2D triangle ----------
        s2 = serif(r"$AE \perp$ bidang $EFGH$ $\Rightarrow \triangle AGE$ siku-siku di $E$",
                   size=28)
        s2.next_to(e_alpha, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(FadeIn(s2), run_time=0.9)

        self.play(*[m.animate.set_opacity(0.25)
                     for m in [edges, labels, plabel, ag, aglabel, eg, arc,
                               alphalabel]],
                  run_time=0.8)

        E2 = np.array([-5.9, -3.1, 0.0])
        G2 = E2 + np.array([3.3, 0.0, 0.0])
        A2 = E2 + np.array([0.0, 3.3 / np.sqrt(2), 0.0])
        l_ae = Line(A2, E2, color="#BBBBBB", stroke_width=6)
        l_eg = Line(E2, G2, color=BLUE, stroke_width=6)
        l_ag = Line(A2, G2, color=YELLOW, stroke_width=6)
        self.play(Create(l_ae, run_time=0.6), Create(l_eg, run_time=0.6),
                  Create(l_ag, run_time=0.8))

        sq = Polygon(E2, E2 + np.array([0.32, 0, 0]), E2 + np.array([0.32, 0.32, 0]),
                     E2 + np.array([0, 0.32, 0]), color=WHITE, stroke_width=3)
        lA = MathTex("A", font_size=30).next_to(A2, UP, buff=0.14)
        lE = MathTex("E", font_size=30).move_to(E2 + np.array([-0.4, -0.4, 0]))
        lG = MathTex("G", font_size=30).move_to(G2 + np.array([0.4, -0.4, 0]))
        ls = MathTex("s", font_size=34, color="#BBBBBB").move_to(
            (A2 + E2) / 2 + np.array([-0.52, 0, 0]))
        lsg = MathTex(r"s\sqrt{2}", font_size=34, color=BLUE).move_to(
            (E2 + G2) / 2 + np.array([0, -0.52, 0]))
        lag = MathTex(r"s\sqrt{3}", font_size=34, color=YELLOW).move_to(
            (A2 + G2) / 2 + np.array([0.66, 0.12, 0]))
        a1 = float(np.arctan2(A2[1] - G2[1], A2[0] - G2[0]))
        arc2 = Arc(radius=0.85, start_angle=a1, angle=np.pi - a1,
                   arc_center=G2, color=YELLOW, stroke_width=5)
        bmid = (a1 + np.pi) / 2
        alabel2 = MathTex(r"\alpha", font_size=36, color=YELLOW)
        alabel2.move_to(G2 + 1.35 * np.array([np.cos(bmid), np.sin(bmid), 0]))
        self.play(
            LaggedStart(FadeIn(sq), FadeIn(lA), FadeIn(lE), FadeIn(lG),
                        FadeIn(ls), FadeIn(lsg), FadeIn(lag),
                        Create(arc2), FadeIn(alabel2), lag_ratio=0.08),
            run_time=1.6,
        )
        self.wait(0.6)

        # ---------- Beat 7: computation (color grammar: EG blue, AG yellow) ----------
        e_cos1 = MathTex(r"\cos\alpha=\frac{\mathrm{EG}}{\mathrm{AG}}", font_size=48)
        e_cos1.set_color_by_tex(r"\alpha", YELLOW)
        e_cos1.set_color_by_tex("EG", BLUE)
        e_cos1.set_color_by_tex("AG", YELLOW)
        e_cos1.next_to(s2, DOWN, aligned_edge=LEFT, buff=0.45)
        self.play(Write(e_cos1), run_time=1.1)

        e_cos2 = MathTex(r"\cos\alpha=\frac{s\sqrt{2}}{s\sqrt{3}}", font_size=48)
        e_cos2.set_color_by_tex(r"\alpha", YELLOW)
        e_cos2.set_color_by_tex(r"s\sqrt{2}", BLUE)
        e_cos2.set_color_by_tex(r"s\sqrt{3}", YELLOW)
        e_cos2.move_to(e_cos1, aligned_edge=LEFT)
        self.play(TransformMatchingTex(e_cos1, e_cos2), run_time=1.1)
        self.wait(0.5)

        e_cos3 = MathTex(r"\cos\alpha=\sqrt{\frac{2}{3}}=\frac{\sqrt{6}}{3}",
                         font_size=56)
        e_cos3.set_color_by_tex(r"\alpha", YELLOW)
        e_cos3.set_color_by_tex(r"\frac{\sqrt{6}}{3}", YELLOW)
        e_cos3.move_to(e_cos2, aligned_edge=LEFT)
        self.play(TransformMatchingTex(e_cos2, e_cos3), run_time=1.2)
        self.wait(0.9)

        # ---------- Beat 8: options, answer (C) ----------
        opts = VGroup(
            MathTex(r"(A)\ \frac{1}{3}\sqrt{3}", font_size=30),
            MathTex(r"(B)\ \frac{1}{2}\sqrt{3}", font_size=30),
            MathTex(r"(C)\ \frac{1}{3}\sqrt{6}", font_size=30),
            MathTex(r"(D)\ \frac{1}{2}\sqrt{6}", font_size=30),
            MathTex(r"(E)\ \frac{2}{3}\sqrt{3}", font_size=30),
        ).arrange(RIGHT, buff=0.35)
        opts.move_to(np.array([2.5, -3.55, 0.0]))
        self.play(FadeIn(opts, run_time=0.9))
        box = SurroundingRectangle(opts[2], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=0.7),
                  opts[2].animate.set_color(YELLOW), run_time=0.7)
        self.wait(2.2)
