from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif, math
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

WIRE = "#D8D8D8"


class CoinToss(Scene):
    def construct(self):
        # ---------- Beat 1: title + problem statement ----------
        title = serif("Frekuensi Harapan", size=60)
        stmt = serif(r"Tiga keping uang logam dilempar 40 kali.", size=32, color=GRAY)
        stmt2 = serif(r"Frekuensi harapan muncul 2 angka dan 1 gambar?", size=32, color=GRAY)
        stmt.next_to(title, DOWN, buff=0.35)
        stmt2.next_to(stmt, DOWN, buff=0.2)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(stmt), FadeIn(stmt2), run_time=0.8)
        self.wait(1.0)

        # ---------- Beat 2: sample space — 8 outcomes as coin triples ----------
        header = serif(r"Ruang sampel 3 keping uang logam", size=32)
        header.to_corner(UL, buff=0.55)
        outcomes = ["AAA", "AAG", "AGA", "AGG", "GAA", "GAG", "GGA", "GGG"]
        fav = {"AAG", "AGA", "GAA"}
        GRAD_A, GRAD_B = "#223544", "#0d1319"  # dark blue-grey gradient fill
        cells = {}
        for i, o in enumerate(outcomes):
            row, col = divmod(i, 4)
            coins = VGroup()
            for ch in o:
                fill = Circle(radius=0.28, fill_color=[GRAD_A, GRAD_B],
                              fill_opacity=0.95, stroke_width=0)
                ring = Circle(radius=0.28, color=WIRE, stroke_width=3)
                t = MathTex(ch, font_size=26).move_to(fill.get_center())
                coins.add(VGroup(fill, ring, t))
            coins.arrange(RIGHT, buff=0.1)
            x = (col - 1.5) * 2.48
            y = (0.5 - row) * 1.25
            coins.move_to(np.array([1.2 + x, -0.2 + y, 0.0]))
            cells[o] = coins

        self.play(
            FadeOut(title, run_time=0.7),
            FadeOut(stmt, run_time=0.7),
            FadeOut(stmt2, run_time=0.7),
            FadeIn(header, run_time=0.6),
            LaggedStart(*[FadeIn(cells[o]) for o in outcomes], lag_ratio=0.08),
            run_time=2.0,
        )
        self.wait(0.6)

        # ---------- Beat 3: highlight the 3 favorable outcomes ----------
        t1 = serif(r"3 dari 8 hasil: tepat 2 angka dan 1 gambar", size=28)
        t1.move_to(np.array([-3.9, 2.45, 0.0]))
        fav_anims = []
        for o in fav:
            for coin in cells[o]:
                fav_anims.append(coin[1].animate.set_color(YELLOW))
                fav_anims.append(coin[2].animate.set_color(YELLOW))
        self.play(
            FadeIn(t1, run_time=0.8),
            *fav_anims,
            *[cells[o].animate.set_opacity(0.18) for o in outcomes if o not in fav],
            run_time=1.2,
        )
        self.wait(0.8)

        # ---------- Beat 4: probability then expected frequency ----------
        e1 = MathTex(r"P = \frac{3}{8}", font_size=48)
        e1.set_color_by_tex("3", YELLOW)
        e1.next_to(t1, DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(e1), run_time=1.0)
        self.wait(0.4)

        e2 = MathTex(r"F_h = \frac{3}{8} \times 40", font_size=48)
        e2.set_color_by_tex("3", YELLOW)
        e2.move_to(e1, aligned_edge=LEFT)
        self.play(TransformMatchingTex(e1, e2), run_time=1.1)
        self.wait(0.4)

        e3 = MathTex(r"F_h = 15", font_size=60)
        e3.set_color_by_tex("15", YELLOW)
        e3.move_to(e2, aligned_edge=LEFT)
        self.play(TransformMatchingTex(e2, e3), run_time=1.1)
        self.wait(0.9)

        # ---------- Beat 5: options, answer (C) ----------
        opts = VGroup(
            MathTex(r"(A)\ 5", font_size=34),
            MathTex(r"(B)\ 10", font_size=34),
            MathTex(r"(C)\ 15", font_size=34),
            MathTex(r"(D)\ 30", font_size=34),
            MathTex(r"(E)\ 45", font_size=34),
        ).arrange(RIGHT, buff=0.55)
        opts.move_to(np.array([1.2, -3.3, 0.0]))
        self.play(FadeIn(opts, run_time=0.9))
        box = SurroundingRectangle(opts[2], color=YELLOW, buff=0.14,
                                   stroke_width=3)
        self.play(Create(box, run_time=0.7),
                  opts[2].animate.set_color(YELLOW), run_time=0.7)
        self.wait(2.0)
