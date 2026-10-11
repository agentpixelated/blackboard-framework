"""Koreksi No.31 Day 1 (F1-No.9): Hukum III Newton, tarik tambang di es.

Naby menjawab (A): pasangan aksi-reaksi saling meniadakan -> tak bergerak.
Video menurunkan dari rumus dasar:
  Hukum III : F_aksi = -F_reaksi   (sama besar, berlawanan arah)
  Hukum II  : Sigma F = ma  berlaku PER BENDA
-> tiap benda tetap berakselerasi oleh gayanya sendiri:
   a_Budi = F/60 < F/40 = a_Ani -> keduanya saling mendekat -> (E).
Pengecoh (B) dan (D) dimatikan singkat di akhir.
"""
from manim import *
from visual_system import BG, BLUE, YELLOW, GREEN, WHITE, GRAY, serif
import numpy as np

config.pixel_width = 1280
config.pixel_height = 720
config.frame_rate = 60
config.background_color = BG

W_RED = "#b86e64"
GOLD = "#d4b84a"


def tline(parts, size=30):
    mob = VGroup(*[serif(t, size=size, color=c or WHITE) for t, c in parts])
    mob.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
    return mob


def xmark(pos, size=0.34, color=W_RED):
    d = size / 2
    l1 = Line(pos + [-d, d, 0], pos + [d, -d, 0], color=color, stroke_width=8)
    l2 = Line(pos + [-d, -d, 0], pos + [d, d, 0], color=color, stroke_width=8)
    return VGroup(l1, l2)


def person(x, color, name, mass):
    head = Circle(radius=0.30, color=color, stroke_width=5,
                  fill_opacity=0).move_to([x, 0.85, 0])
    body = Rectangle(width=0.62, height=1.05, color=color, stroke_width=5,
                     fill_opacity=0).move_to([x, -0.02, 0])
    tag = serif(name, size=26, color=color).move_to([x, 1.58, 0])
    mtag = serif(mass + " kg", size=22, color=color).move_to([x, 1.30, 0])
    return VGroup(head, body, tag, mtag)


class KoreksiHukum3(Scene):
    def construct(self):
        LX = -3.55  # left text column center

        # ---------------- beat 1: title ----------------
        title = serif("Koreksi No. 31: Hukum III Newton", size=52)
        self.play(Write(title), run_time=1.3)
        self.wait(0.9)
        self.play(FadeOut(title, run_time=0.5))

        # ---------------- beat 1b: the setup ----------------
        s1 = tline([("Budi (60 kg) dan Ani (40 kg)", WHITE)],
                   size=34).move_to([0, 0.6, 0])
        s2 = tline([("tarik tambang di atas es licin.", WHITE)],
                   size=34).move_to([0, -0.05, 0])
        s3 = tline([("Gaya tarik sama besar. Apa yang terjadi?", YELLOW)],
                   size=32).move_to([0, -0.75, 0])
        self.play(Write(s1, run_time=1.0))
        self.play(Write(s2, run_time=1.0))
        self.play(Write(s3, run_time=1.0))
        self.wait(1.2)
        self.play(*[FadeOut(m, run_time=0.4) for m in (s1, s2, s3)])

        # ---------------- beat 2: the misconception ----------------
        head = tline([("Pikiranmu:", YELLOW)], size=32).move_to([LX, 3.1, 0])
        w1 = tline([("$F$ dan $-F$ sama besar, berlawanan arah", WHITE)],
                   size=30).move_to([LX, 2.45, 0])
        w2 = tline([("pasangan aksi-reaksi: benar.", GREEN)],
                   size=26).move_to([LX, 1.9, 0])
        w3 = tline([("$\\Rightarrow$ saling meniadakan $\\Rightarrow$ diam (A)", W_RED)],
                   size=30).move_to([LX, 1.2, 0])
        w4 = tline([("lompatan logika yang salah.", GRAY)],
                   size=24).move_to([LX, 0.65, 0])
        xm = xmark(np.array([-0.7, 1.2, 0]), size=0.42)

        ice = Line([-7.11, -0.62, 0], [7.11, -0.62, 0], color=GRAY, stroke_width=3)
        ice_label = serif("es licin", size=22, color=GRAY).move_to([5.9, -0.98, 0])
        budi = person(1.3, BLUE, "Budi", "60")
        ani = person(4.3, GOLD, "Ani", "40")
        rope = Line([1.66, 0.12, 0], [3.94, 0.12, 0], color=WHITE, stroke_width=4)
        arr_b = Arrow([1.95, 0.55, 0], [2.75, 0.55, 0], color=BLUE,
                      stroke_width=6, buff=0.05)
        lab_b = serif("$F$", size=30, color=BLUE).next_to(arr_b, UP, buff=0.1)
        arr_a = Arrow([3.65, 0.55, 0], [2.85, 0.55, 0], color=GOLD,
                      stroke_width=6, buff=0.05)
        lab_a = serif("$F$", size=30, color=GOLD).next_to(arr_a, UP, buff=0.1)

        self.play(FadeIn(head, run_time=0.4))
        self.play(Create(ice, run_time=0.4), FadeIn(ice_label, run_time=0.3),
                  FadeIn(budi, run_time=0.6), FadeIn(ani, run_time=0.6))
        self.play(Create(rope, run_time=0.5))
        self.wait(0.4)
        self.play(Write(w1, run_time=1.0),
                  FadeIn(arr_b, run_time=0.4), FadeIn(lab_b, run_time=0.3),
                  FadeIn(arr_a, run_time=0.4), FadeIn(lab_a, run_time=0.3))
        self.play(FadeIn(w2, run_time=0.5))
        self.wait(0.9)
        self.play(Write(w3, run_time=1.0), FadeIn(xm, run_time=0.4))
        self.play(FadeIn(w4, run_time=0.4))
        self.wait(1.1)

        # ---------------- beat 3: from the fundamental laws ----------------
        g0 = tline([("Dari rumus dasar:", YELLOW)], size=32).move_to([LX, 3.1, 0])
        h3 = tline([("Hukum III: ", GRAY),
                    ("$F_{\\text{aksi}} = -F_{\\text{reaksi}}$", WHITE)],
                   size=30).move_to([LX, 2.5, 0])
        g1 = tline([("$\\sum F = ma$", WHITE), ("  (Hukum II)", GRAY)],
                   size=38).move_to([LX, 1.9, 0])
        g2 = tline([("berlaku untuk ", WHITE), ("SATU", YELLOW), (" benda", WHITE)],
                   size=28).move_to([LX, 1.35, 0])
        g3 = tline([("es licin: hanya gaya tali.", GRAY)],
                   size=24).move_to([LX, 0.85, 0])
        p1 = tline([("Pada ", WHITE), ("Budi", BLUE), (": $\\sum F = F$", WHITE)],
                   size=30).move_to([LX, 0.25, 0])
        p2 = tline([("$\\Rightarrow a = F/60$", BLUE)],
                   size=32).move_to([LX, -0.3, 0])
        p3 = tline([("Pada ", WHITE), ("Ani", GOLD), (": $\\sum F = F$", WHITE)],
                   size=30).move_to([LX, -0.85, 0])
        p4 = tline([("$\\Rightarrow a = F/40$", GOLD)],
                   size=32).move_to([LX, -1.4, 0])
        key = tline([("gaya aksi dan reaksi bekerja pada", WHITE)],
                    size=26).move_to([LX, -2.05, 0])
        key2 = tline([("benda yang BERBEDA", GREEN)],
                     size=34).move_to([LX, -2.55, 0])

        box_b = SurroundingRectangle(VGroup(budi, arr_b, lab_b),
                                     color=GRAY, buff=0.14, stroke_width=2)
        box_a = SurroundingRectangle(VGroup(ani, arr_a, lab_a),
                                     color=GRAY, buff=0.14, stroke_width=2)

        self.play(*[FadeOut(m, run_time=0.4)
                    for m in (head, w1, w2, w3, w4, xm)])
        self.play(FadeIn(g0, run_time=0.4))
        self.play(Write(h3, run_time=0.9))
        self.wait(0.4)
        self.play(Write(g1, run_time=0.9))
        self.play(Write(g2, run_time=0.7))
        self.play(FadeIn(g3, run_time=0.4))
        self.wait(0.6)
        self.play(Write(p1, run_time=0.9), Create(box_b, run_time=0.5))
        self.play(Write(p2, run_time=0.8))
        self.wait(0.5)
        self.play(Write(p3, run_time=0.9), Create(box_a, run_time=0.5))
        self.play(Write(p4, run_time=0.8))
        self.wait(0.6)
        self.play(Write(key, run_time=0.9))
        self.play(Write(key2, run_time=0.8))
        self.wait(2.4)

        # ---------------- beat 4: derive + motion + answer ----------------
        d1 = tline([("$a_{\\text{Budi}} = F/60$", BLUE), ("$<$", WHITE),
                    ("$F/40 = a_{\\text{Ani}}$", GOLD)],
                   size=30).move_to([LX, 2.7, 0])
        d2 = tline([("keduanya saling mendekat,", WHITE)],
                   size=30).move_to([LX, 2.1, 0])
        d3 = tline([("Budi berakselerasi lebih kecil.", WHITE)],
                   size=30).move_to([LX, 1.55, 0])
        n1 = tline([("Misal ", WHITE), ("$F = 120$ N:", YELLOW)],
                   size=30).move_to([LX, 1.0, 0])
        n2 = tline([("$a_{\\text{Budi}} = 2\\ \\text{m/s}^2$", BLUE), (",  ", WHITE),
                    ("$a_{\\text{Ani}} = 3\\ \\text{m/s}^2$", GOLD)],
                   size=28).move_to([LX, 0.45, 0])
        ans = tline([("Jawaban: (E)", YELLOW)], size=44).move_to([LX, 0.7, 0])

        self.play(*[FadeOut(m, run_time=0.4)
                    for m in (g0, h3, g1, g2, g3, p1, p2, p3, p4, key, key2,
                              box_b, box_a)])
        self.play(Write(d1, run_time=1.0))
        self.play(Write(d2, run_time=0.7), Write(d3, run_time=0.7))
        self.wait(0.6)
        self.play(Write(n1, run_time=0.8))
        self.play(Write(n2, run_time=1.0))
        self.wait(1.0)
        self.play(FadeOut(n1, run_time=0.3), FadeOut(n2, run_time=0.3))
        self.play(FadeOut(arr_b, run_time=0.3), FadeOut(lab_b, run_time=0.3),
                  FadeOut(arr_a, run_time=0.3), FadeOut(lab_a, run_time=0.3))
        self.play(budi.animate.shift(RIGHT * 0.7),
                  ani.animate.shift(LEFT * 1.15),
                  rope.animate.put_start_and_end_on([2.36, 0.12, 0],
                                                    [2.79, 0.12, 0]),
                  run_time=1.5)
        self.wait(1.8)
        abox = SurroundingRectangle(ans, color=YELLOW, buff=0.18, stroke_width=3)
        self.play(Write(ans, run_time=0.9), Create(abox, run_time=0.5))
        self.wait(1.0)

        # ---------------- beat 5: kill the distractors ----------------
        k1 = tline([("(B) salah: $F$ sama, $m$ beda $\\Rightarrow$ $a$ beda", GRAY)],
                   size=26).move_to([LX, -0.15, 0])
        xm1 = xmark(np.array([-0.85, -0.15, 0]), size=0.32)
        k2 = tline([("(D) salah: $\\sum F = 0$ pada sistem,", GRAY)],
                   size=26).move_to([LX, -0.7, 0])
        k3 = tline([("tidak berarti nol pada tiap benda.", GRAY)],
                   size=26).move_to([LX, -1.15, 0])
        xm2 = xmark(np.array([-0.85, -0.92, 0]), size=0.32)
        fin = tline([("Ingat: ", WHITE), ("$\\sum F = ma$", YELLOW),
                     (" selalu per benda.", WHITE)],
                    size=30).move_to([LX, -1.8, 0])

        self.play(Write(k1, run_time=0.8), FadeIn(xm1, run_time=0.3))
        self.wait(0.5)
        self.play(Write(k2, run_time=0.7), Write(k3, run_time=0.7),
                  FadeIn(xm2, run_time=0.3))
        self.wait(0.6)
        self.play(Write(fin, run_time=1.0))
        self.wait(3.2)
