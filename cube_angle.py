from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

# ---- Oblique projection: screen = (x + 0.45 z, y - 0.45 z)
# Viewer above/front: sees top (EFGH), back, left faces.
# Hidden vertex is B -> dashed edges: AB, BC, BF.
K = 1.5
CX, CY = 2.7, -0.3

def proj(p):
    x, y, z = p
    return np.array([CX + K * (x + 0.45 * z), CY + K * (y - 0.45 * z), 0.0])

C0 = np.array([CX, CY, 0.0])


class CubeAngle(Scene):
    def construct(self):
        # ---------- vertices: ABCD bottom, EFGH top, E above A etc. ----------
        A3 = (-1, -1, -1); B3 = (1, -1, -1); C3 = (1, -1, 1); D3 = (-1, -1, 1)
        E3 = (-1, 1, -1);  F3 = (1, 1, -1);  G3 = (1, 1, 1);  H3 = (-1, 1, 1)
        A, B, C, D, E, F, G, H = map(proj, (A3, B3, C3, D3, E3, F3, G3, H3))

        solid_pairs = [(B, C), (C, D), (D, A),
                       (F, G), (G, H), (H, E),
                       (A, E), (C, G), (D, H)]
        dashed_pairs = [(A, B), (B, C), (B, F)]

        # ---------- Beat 1: title + problem statement ----------
        title = serif("Sudut antara Garis dan Bidang", size=52)
        stmt = serif(r"Kubus $ABCD.EFGH$: sudut antara garis $AG$ dan bidang $EFGH$"
                     r" adalah $\alpha$. Tentukan $\cos\alpha$.", size=30, color=GRAY)
        stmt.next_to(title, DOWN, buff=0.45)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(stmt), run_time=0.8)
        self.wait(1.2)

        # ---------- Beat 2: build the cube (title leaves as it arrives) ----------
        header = serif(r"Sudut garis $AG$ terhadap bidang $EFGH$", size=30)
        header.to_corner(UL, buff=0.55)
        edges_s = VGroup(*[Line(p, q, color=WHITE, stroke_width=3)
                           for p, q in solid_pairs])
        edges_d = VGroup(*[DashedLine(p, q, color=GRAY, stroke_width=3)
                           for p, q in dashed_pairs])
        self.play(
            FadeOut(title, run_time=0.8),
            FadeOut(stmt, run_time=0.8),
            Create(edges_s, run_time=1.6),
            Create(edges_d, run_time=1.6),
        )
        self.play(FadeIn(header), run_time=0.5)

        labels = VGroup()
        for letter, v3 in (("A", A3), ("B", B3), ("C", C3), ("D", D3),
                           ("E", E3), ("F", F3), ("G", G3), ("H", H3)):
            s = proj(v3)
            d = s - C0
            d = d / np.linalg.norm(d)
            lab = MathTex(letter, font_size=30).move_to(s + d * 0.52)
            labels.add(lab)
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.07),
                  run_time=1.4)
        self.wait(0.6)

        # ---------- Beat 3: highlight the plane EFGH ----------
        topface = Polygon(E, F, G, H, fill_color=BLUE, fill_opacity=0.32,
                          stroke_width=0)
        plabel = serif(r"bidang $EFGH$", size=28, color=BLUE)
        plabel.move_to(np.array([5.85, 1.45, 0.0]))
        self.play(
            FadeIn(topface, run_time=1.0),
            *[m.animate.set_color(GRAY).set_opacity(0.55) for m in edges_s],
            FadeIn(plabel, run_time=1.0),
        )
        self.wait(0.8)

        # ---------- Beat 4: draw AG ----------
        ag = Line(A, G, color=YELLOW, stroke_width=7)
        aglabel = serif(r"garis $AG$", size=28, color=YELLOW)
        aglabel.move_to((A + G) / 2 + np.array([1.05, -0.62, 0.0]))
        self.play(Create(ag, run_time=1.2), FadeIn(aglabel, run_time=0.9))
        self.wait(0.8)

        # ---------- Beat 5: the projection ----------
        s1 = serif(r"Proyeksi $AG$ pada bidang $EFGH$ adalah $EG$", size=25)
        s1.move_to(np.array([-3.55, 2.55, 0.0]))
        self.play(FadeIn(s1), run_time=0.8)
        dot = Dot(A, color=YELLOW, radius=0.09)
        self.add(dot)
        self.play(dot.animate.move_to(E), run_time=0.9)
        self.play(FadeOut(dot), run_time=0.3)
        eg = Line(E, G, color=WHITE, stroke_width=5)
        self.play(Create(eg, run_time=0.9))

        # angle marker at G between GA and GE (schematic, marks identity of alpha)
        u1 = A - G; u1 = u1 / np.linalg.norm(u1)
        u2 = E - G; u2 = u2 / np.linalg.norm(u2)
        alpha3 = float(np.arccos(np.clip(np.dot(u1, u2), -1, 1)))
        r = 0.55
        arc = ParametricFunction(
            lambda t: G + r * (np.cos(t) * u1 + np.sin(t) * u2),
            t_range=[0, alpha3, 0.02], color=YELLOW, stroke_width=4)
        bis = u1 + u2; bis = bis / np.linalg.norm(bis)
        alphalabel = MathTex(r"\alpha", font_size=36, color=YELLOW)
        alphalabel.move_to(G + bis * (r + 0.42))
        self.play(Create(arc, run_time=0.7), FadeIn(alphalabel, run_time=0.6))

        e_alpha = MathTex(r"\alpha", r"= \angle AGE", font_size=44)
        e_alpha[0].set_color(YELLOW)
        e_alpha.next_to(s1, DOWN, aligned_edge=LEFT, buff=0.35)
        self.play(Write(e_alpha), run_time=1.0)
        self.wait(0.8)

        # ---------- Beat 6: right triangle justification + exact 2D triangle ----------
        s2 = serif(r"$AE \perp$ bidang $EFGH$ $\Rightarrow \triangle AGE$ siku-siku di $E$",
                   size=25)
        s2.next_to(e_alpha, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(FadeIn(s2), run_time=0.9)

        # dim the cube, focus shifts to the exact triangle
        cube_parts = [edges_s, edges_d, labels, topface, plabel, ag, aglabel,
                      eg, arc, alphalabel]
        self.play(*[m.animate.set_opacity(0.28) for m in cube_parts],
                  run_time=0.8)

        E2 = np.array([-5.9, -3.1, 0.0])
        G2 = E2 + np.array([3.3, 0.0, 0.0])
        A2 = E2 + np.array([0.0, 3.3 / np.sqrt(2), 0.0])
        tri = Polygon(E2, G2, A2, color=WHITE, stroke_width=4, fill_opacity=0)
        self.play(Create(tri, run_time=1.0))

        sq = Polygon(E2, E2 + np.array([0.32, 0, 0]), E2 + np.array([0.32, 0.32, 0]),
                     E2 + np.array([0, 0.32, 0]), color=WHITE, stroke_width=3)
        lA = MathTex("A", font_size=28).next_to(A2, UP, buff=0.14)
        lE = MathTex("E", font_size=28).move_to(E2 + np.array([-0.38, -0.38, 0]))
        lG = MathTex("G", font_size=28).move_to(G2 + np.array([0.38, -0.38, 0]))
        ls = MathTex("s", font_size=32).move_to((A2 + E2) / 2 + np.array([-0.5, 0, 0]))
        lsg = MathTex(r"s\sqrt{2}", font_size=32).move_to((E2 + G2) / 2 + np.array([0, -0.5, 0]))
        lag = MathTex(r"s\sqrt{3}", font_size=32).move_to((A2 + G2) / 2 + np.array([0.62, 0.12, 0]))
        a1 = float(np.arctan2(A2[1] - G2[1], A2[0] - G2[0]))
        arc2 = Arc(radius=0.8, start_angle=a1, angle=np.pi - a1,
                   arc_center=G2, color=YELLOW, stroke_width=4)
        bmid = (a1 + np.pi) / 2
        alabel2 = MathTex(r"\alpha", font_size=34, color=YELLOW)
        alabel2.move_to(G2 + 1.3 * np.array([np.cos(bmid), np.sin(bmid), 0]))
        self.play(
            LaggedStart(FadeIn(sq), FadeIn(lA), FadeIn(lE), FadeIn(lG),
                        FadeIn(ls), FadeIn(lsg), FadeIn(lag),
                        Create(arc2), FadeIn(alabel2), lag_ratio=0.08),
            run_time=1.6,
        )
        self.wait(0.6)

        # ---------- Beat 7: computation ----------
        e_cos1 = MathTex(r"\cos", r"\alpha", r"=\frac{\mathrm{EG}}{\mathrm{AG}}",
                         font_size=44)
        e_cos1[1].set_color(YELLOW)
        e_cos1.next_to(s2, DOWN, aligned_edge=LEFT, buff=0.45)
        self.play(Write(e_cos1), run_time=1.1)

        e_cos2 = MathTex(r"\cos", r"\alpha", r"=\frac{s\sqrt{2}}{s\sqrt{3}}",
                         font_size=44)
        e_cos2[1].set_color(YELLOW)
        e_cos2.move_to(e_cos1, aligned_edge=LEFT)
        self.play(TransformMatchingTex(e_cos1, e_cos2), run_time=1.1)
        self.wait(0.5)

        e_cos3 = MathTex(r"\cos", r"\alpha", r"=\sqrt{\frac{2}{3}}",
                         r"=\frac{\sqrt{6}}{3}", font_size=44)
        e_cos3[1].set_color(YELLOW)
        e_cos3[3].set_color(YELLOW)
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
        ).arrange(RIGHT, buff=0.38)
        opts.move_to(np.array([2.0, -3.45, 0.0]))
        self.play(FadeIn(opts, run_time=0.9))
        box = SurroundingRectangle(opts[2], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=0.7),
                  opts[2].animate.set_color(YELLOW), run_time=0.7)
        self.wait(2.2)
