"""Contact sheet of alternative Panchaayat mark concepts."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "brand"
OUT.mkdir(exist_ok=True)
FONTS = Path("C:/Windows/Fonts")
SS = 3

TEAL = (13, 148, 136, 255)
CORAL = (242, 106, 75, 255)
INK = (18, 23, 43, 255)
PAPER = (250, 246, 240, 255)
MUTED = (122, 115, 102, 255)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), int(size))


def draw_check(d, cx, cy, R, color=CORAL):
    w = int(R * 0.16)
    p1 = (cx - R * 0.30, cy + R * 0.02)
    p2 = (cx - R * 0.06, cy + R * 0.26)
    p3 = (cx + R * 0.34, cy - R * 0.26)
    d.line([p1, p2, p3], fill=color, width=w, joint="curve")
    rr = w / 2
    for p in (p1, p2, p3):
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=color)


def dot(d, cx, cy, r, fill=TEAL):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


# ── Concept A: full ring + dots arced above the check ────────────────
def A_arc_dots(d, cx, cy, R, n=3):
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=TEAL, width=int(R * 0.14))
    dr = R * 0.66
    ddot = R * 0.12
    spread = 70 if n == 3 else 100   # total degrees across the top
    start = -90 - spread / 2
    step = spread / (n - 1)
    for i in range(n):
        a = math.radians(start + i * step)
        dot(d, cx + dr * math.cos(a), cy + dr * math.sin(a), ddot)
    draw_check(d, cx, cy + R * 0.08, R)


def A_open_top(d, cx, cy, R):
    # ring with a gap at the top; 3 dots sit in the gap like heads at the head of the table
    d.arc([cx - R, cy - R, cx + R, cy + R], start=-55, end=235, fill=TEAL, width=int(R * 0.14))
    ddot = R * 0.13
    for ang in (-135, -90, -45):
        a = math.radians(ang)
        dot(d, cx + R * math.cos(a), cy + R * math.sin(a), ddot)
    draw_check(d, cx, cy + R * 0.08, R)


# ── Concept B: segmented ring = seats around a table ─────────────────
def B_segments(d, cx, cy, R, n=8, gap_ratio=0.42, w=None):
    w = w or R * 0.14
    seg = 360.0 / n
    for i in range(n):
        s = i * seg + seg * gap_ratio / 2
        e = (i + 1) * seg - seg * gap_ratio / 2
        d.arc([cx - R, cy - R, cx + R, cy + R], start=s, end=e, fill=TEAL, width=int(w))
    draw_check(d, cx, cy, R)


def B_seats(d, cx, cy, R):
    # fewer, thicker seat-arcs with a small "table" dot behind the check
    B_segments(d, cx, cy, R, n=6, gap_ratio=0.5, w=R * 0.19)
    draw_check(d, cx, cy, R)


VARIANTS = [
    ("A1 · 3 dots arced above", lambda d, cx, cy, R: A_arc_dots(d, cx, cy, R, 3)),
    ("A2 · 5 dots arced above", lambda d, cx, cy, R: A_arc_dots(d, cx, cy, R, 5)),
    ("A3 · open-top, heads in gap", A_open_top),
    ("B1 · 8 seats (segmented)", lambda d, cx, cy, R: B_segments(d, cx, cy, R, 8)),
    ("B2 · 12 dashes", lambda d, cx, cy, R: B_segments(d, cx, cy, R, 12, 0.5, R * 0.12)),
    ("B3 · 6 bold seats", B_seats),
]


def build():
    cols, rows = 3, 2
    cell = 460 * SS
    labelh = 60 * SS
    W, H = cols * cell, rows * (cell + labelh)
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    lf = font("segoeui.ttf", 26 * SS)
    for idx, (label, fn) in enumerate(VARIANTS):
        r, c = idx // cols, idx % cols
        x0, y0 = c * cell, r * (cell + labelh)
        cx, cy = x0 + cell / 2, y0 + cell / 2
        R = cell * 0.32
        fn(d, cx, cy, R)
        tw = d.textlength(label, font=lf)
        d.text((cx - tw / 2, y0 + cell - labelh * 0.2), label, font=lf, fill=INK)
    img.resize((W // SS, H // SS), Image.LANCZOS).save(OUT / "logo-variants.png")
    print("Saved", OUT / "logo-variants.png")


if __name__ == "__main__":
    build()
