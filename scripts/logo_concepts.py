"""Fresh Panchaayat mark concepts — beyond the ring+check family."""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "brand"
OUT.mkdir(exist_ok=True)
FONTS = Path("C:/Windows/Fonts")
SS = 3

TEAL = (13, 148, 136, 255)
TEAL_DK = (15, 118, 110, 255)
CORAL = (242, 106, 75, 255)
INK = (18, 23, 43, 255)
PAPER = (250, 246, 240, 255)
WHITE = (255, 255, 255, 255)
GOLD = (224, 168, 46, 255)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), int(size))


def check(d, cx, cy, R, color=WHITE, wr=0.17):
    w = max(2, int(R * wr))
    p1 = (cx - R * 0.34, cy + R * 0.03)
    p2 = (cx - R * 0.07, cy + R * 0.30)
    p3 = (cx + R * 0.38, cy - R * 0.28)
    d.line([p1, p2, p3], fill=color, width=w, joint="curve")
    rr = w / 2
    for p in (p1, p2, p3):
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=color)


def dot(d, cx, cy, r, fill=TEAL):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


# ── C1: speech bubble (voice) with a check (resolved) ────────────────
def C1_bubble_check(d, cx, cy, R):
    w, h = R * 1.7, R * 1.35
    x0, y0 = cx - w / 2, cy - h / 2 - R * 0.12
    rad = R * 0.34
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=rad, fill=TEAL)
    # tail bottom-left
    d.polygon([(x0 + w * 0.22, y0 + h - 2), (x0 + w * 0.15, y0 + h + R * 0.45),
               (x0 + w * 0.48, y0 + h - 2)], fill=TEAL)
    check(d, cx, y0 + h / 2, R * 0.9, WHITE)


# ── C2: two bubbles in dialogue, resolved where they meet ────────────
def C2_dialogue(d, cx, cy, R):
    w, h = R * 1.15, R * 0.92
    # consumer bubble (teal, upper-left)
    ax, ay = cx - R * 0.62, cy - R * 0.55
    d.rounded_rectangle([ax - w / 2, ay - h / 2, ax + w / 2, ay + h / 2], radius=R * 0.28, fill=TEAL)
    d.polygon([(ax - w * 0.15, ay + h / 2 - 2), (ax - w * 0.30, ay + h / 2 + R * 0.34),
               (ax + w * 0.12, ay + h / 2 - 2)], fill=TEAL)
    # brand bubble (coral, lower-right)
    bx, by = cx + R * 0.55, cy + R * 0.5
    d.rounded_rectangle([bx - w / 2, by - h / 2, bx + w / 2, by + h / 2], radius=R * 0.28, fill=CORAL)
    d.polygon([(bx + w * 0.15, by - h / 2 + 2), (bx + w * 0.30, by - h / 2 - R * 0.34),
               (bx - w * 0.12, by - h / 2 + 2)], fill=CORAL)
    check(d, ax + R * 0.02, ay, R * 0.62, WHITE, wr=0.2)


# ── C3: shield of trust + check ──────────────────────────────────────
def _shield_pts(cx, cy, w, h):
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
            (cx + w / 2, cy + h * 0.08), (cx, cy + h / 2), (cx - w / 2, cy + h * 0.08)]


def C3_shield_check(d, cx, cy, R):
    pts = _shield_pts(cx, cy, R * 1.5, R * 1.85)
    d.polygon(pts, fill=TEAL)
    check(d, cx, cy - R * 0.08, R * 0.95, WHITE)


# ── C4: shield holding the assembly (3 dots) ─────────────────────────
def C4_shield_assembly(d, cx, cy, R):
    pts = _shield_pts(cx, cy, R * 1.5, R * 1.85)
    d.polygon(pts, outline=TEAL, width=int(R * 0.16))
    for ang, col in ((-140, TEAL), (-90, CORAL), (-40, TEAL)):
        a = math.radians(ang)
        dot(d, cx + R * 0.52 * math.cos(a), cy - R * 0.18 + R * 0.52 * math.sin(a), R * 0.16, col)
    check(d, cx, cy + R * 0.5, R * 0.6, TEAL, wr=0.2)


# ── C5: chaupal — a canopy/roof sheltering the gathering ─────────────
def C5_canopy(d, cx, cy, R):
    # arched roof
    top = cy - R * 0.7
    d.arc([cx - R * 1.0, top, cx + R * 1.0, top + R * 1.4], start=180, end=360,
          fill=CORAL, width=int(R * 0.20))
    # centre post / trunk
    d.line([(cx, top + R * 0.02), (cx, cy + R * 0.55)], fill=CORAL, width=int(R * 0.16))
    # three people gathered beneath
    for dx, col in ((-R * 0.55, TEAL), (0, TEAL_DK), (R * 0.55, TEAL)):
        dot(d, cx + dx, cy + R * 0.62, R * 0.17, col)


# ── C6: chat bubble whose pointer is the check ("voice, resolved") ───
def C6_bubble_tick(d, cx, cy, R):
    w, h = R * 1.7, R * 1.3
    x0, y0 = cx - w / 2, cy - h / 2 - R * 0.2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=R * 0.4, outline=TEAL, width=int(R * 0.16))
    # three dots inside (voices)
    for dx in (-R * 0.45, 0, R * 0.45):
        dot(d, cx + dx, y0 + h * 0.45, R * 0.11, TEAL)
    # the tail IS a coral check dropping from the bubble
    p1 = (x0 + w * 0.30, y0 + h - R * 0.02)
    p2 = (x0 + w * 0.40, y0 + h + R * 0.4)
    p3 = (x0 + w * 0.66, y0 + h - R * 0.15)
    ww = int(R * 0.17)
    d.line([p1, p2, p3], fill=CORAL, width=ww, joint="curve")
    rr = ww / 2
    for p in (p1, p2, p3):
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=CORAL)


CONCEPTS = [
    ("C1 · voice bubble + check", C1_bubble_check),
    ("C2 · dialogue → resolved", C2_dialogue),
    ("C3 · shield of trust + check", C3_shield_check),
    ("C4 · shield holds the council", C4_shield_assembly),
    ("C5 · chaupal (canopy + people)", C5_canopy),
    ("C6 · bubble w/ check-tail", C6_bubble_tick),
]


def build():
    cols, rows = 3, 2
    cell = 460 * SS
    labelh = 66 * SS
    W, H = cols * cell, rows * (cell + labelh)
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    lf = font("segoeui.ttf", 25 * SS)
    for idx, (label, fn) in enumerate(CONCEPTS):
        r, c = idx // cols, idx % cols
        x0, y0 = c * cell, r * (cell + labelh)
        cx, cy = x0 + cell / 2, y0 + cell / 2
        R = cell * 0.30
        fn(d, cx, cy, R)
        tw = d.textlength(label, font=lf)
        d.text((cx - tw / 2, y0 + cell - labelh * 0.1), label, font=lf, fill=INK)
    img.resize((W // SS, H // SS), Image.LANCZOS).save(OUT / "logo-concepts.png")
    print("Saved", OUT / "logo-concepts.png")


if __name__ == "__main__":
    build()
