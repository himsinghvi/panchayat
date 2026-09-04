"""Generate the Panchaayat logo + showroom trust seal as PNGs.

Identity: a "council ring" — an assembly (dots) gathered around a
confirmed resolution (check). Flat, geometric, two-colour, no gradients.
Rendered at 4x supersampling for crisp edges, then downscaled.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "brand"
OUT.mkdir(exist_ok=True)
FONTS = Path("C:/Windows/Fonts")

SS = 4  # supersample factor

# ── palette (RGBA) ───────────────────────────────────────────────────
TEAL    = (13, 148, 136, 255)
TEAL_DK = (15, 118, 110, 255)
CORAL   = (242, 106, 75, 255)
INK     = (18, 23, 43, 255)
PAPER   = (250, 246, 240, 255)
GOLD    = (224, 168, 46, 255)
MUTED   = (122, 115, 102, 255)
CLEAR   = (0, 0, 0, 0)


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), int(size))


GEO_B = "georgiab.ttf"
SEG_SB = "seguisb.ttf"
SEG_B = "segoeuib.ttf"


# ── the mark: ring + 4 council dots + coral resolution check ─────────
def draw_mark(d, cx, cy, R, ring_w=None, dot_r=None, check=True,
              ring=TEAL, dots=TEAL, mark=CORAL):
    ring_w = ring_w or R * 0.14
    dot_r = dot_r or R * 0.115
    # outer ring
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=ring, width=int(ring_w))
    # 4 assembly dots at cardinal points, sitting just inside the ring
    dr = R - ring_w * 0.5 - dot_r - R * 0.10
    for ang in (-90, 0, 90, 180):
        a = math.radians(ang)
        dx, dy = cx + dr * math.cos(a), cy + dr * math.sin(a)
        d.ellipse([dx - dot_r, dy - dot_r, dx + dot_r, dy + dot_r], fill=dots)
    # centre resolution check
    if check:
        w = int(R * 0.16)
        p1 = (cx - R * 0.30, cy + R * 0.02)
        p2 = (cx - R * 0.06, cy + R * 0.26)
        p3 = (cx + R * 0.34, cy - R * 0.26)
        d.line([p1, p2, p3], fill=mark, width=w, joint="curve")
        rr = w / 2
        for p in (p1, p2, p3):
            d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=mark)
    else:
        d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=mark)


def make_mark(px=512, bg=CLEAR, **kw):
    S = px * SS
    img = Image.new("RGBA", (S, S), bg)
    d = ImageDraw.Draw(img)
    R = S * 0.40
    draw_mark(d, S / 2, S / 2, R, **kw)
    return img.resize((px, px), Image.LANCZOS)


# ── horizontal lockup: mark + wordmark + tagline ─────────────────────
def make_horizontal(h=360, dark=False):
    S = h * SS
    R = S * 0.36
    cx = S * 0.42 + R          # mark centre
    tx = cx + R + S * 0.30     # text start x
    fw = font(GEO_B, S * 0.40)
    ft = font(SEG_SB, S * 0.125)
    tag = "C O N S U M E R   V O I C E   ·   R E S O L V E D"
    dot_gap = S * 0.03
    # measure to size the canvas exactly
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    wlen = tmp.textlength("Panchaayat", font=fw)
    tlen = tmp.textlength(tag, font=ft)
    content_r = tx + max(wlen + dot_gap + S * 0.075, tlen)
    W = int(content_r + S * 0.30)
    img = Image.new("RGBA", (W, S), CLEAR)
    d = ImageDraw.Draw(img)
    accent = TEAL if not dark else (94, 214, 203, 255)
    draw_mark(d, cx, S / 2, R, ring=accent, dots=accent, mark=CORAL)
    word_col = PAPER if dark else INK
    ty = S * 0.20
    d.text((tx, ty), "Panchaayat", font=fw, fill=word_col)
    dcx = tx + wlen + dot_gap
    d.ellipse([dcx, ty + S * 0.34, dcx + S * 0.07, ty + S * 0.34 + S * 0.07], fill=CORAL)
    d.text((tx + S * 0.02, S * 0.66), tag, font=ft, fill=(MUTED if not dark else (150, 200, 195, 255)))
    return img.resize((W // SS, h), Image.LANCZOS)


# ── curved text along an arc ─────────────────────────────────────────
def arc_text(img, text, fnt, cx, cy, radius, color, top=True, spacing=1.0):
    d = ImageDraw.Draw(img)
    widths = [d.textlength(c, font=fnt) * spacing for c in text]
    total = sum(widths)
    # angular span
    span = total / radius
    center = -math.pi / 2 if top else math.pi / 2
    if top:
        ang = center - span / 2  # go clockwise (increasing angle) L->R
    else:
        ang = center + span / 2  # go counter-clockwise so text reads L->R
    for ch, w in zip(text, widths):
        dtheta = (w / radius)
        a = ang + (dtheta / 2 if top else -dtheta / 2)
        gx = cx + radius * math.cos(a)
        gy = cy + radius * math.sin(a)
        # render glyph
        pad = int(fnt.size * 0.6)
        gi = Image.new("RGBA", (int(w) + pad * 2, int(fnt.size * 1.7) + pad), CLEAR)
        gd = ImageDraw.Draw(gi)
        gd.text((pad, pad // 2), ch, font=fnt, fill=color)
        # rotation so baseline is tangent, letters upright
        deg = math.degrees(a)
        rot = -(deg + 90) if top else -(deg - 90)
        gi = gi.rotate(rot, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(gi, (int(gx - gi.width / 2), int(gy - gi.height / 2)))
        ang += dtheta if top else -dtheta


# ── showroom trust seal ──────────────────────────────────────────────
def make_seal(px=1000, transparent_outside=True):
    S = px * SS
    img = Image.new("RGBA", (S, S), CLEAR)
    d = ImageDraw.Draw(img)
    c = S / 2
    R = S * 0.47
    # filled disc
    d.ellipse([c - R, c - R, c + R, c + R], fill=PAPER)
    # outer bold teal ring
    d.ellipse([c - R, c - R, c + R, c + R], outline=TEAL_DK, width=int(S * 0.022))
    # thin inner ring that closes the text band
    r_in = R * 0.72
    d.ellipse([c - r_in, c - r_in, c + r_in, c + r_in], outline=TEAL, width=int(S * 0.006))
    r_div = r_in
    # curved text (pulled inward so it never crowds the outer ring)
    r_text = R * 0.855
    arc_text(img, "PANCHAAYAT", font(GEO_B, S * 0.076), c, c, r_text, TEAL_DK, top=True, spacing=1.10)
    arc_text(img, "VERIFIED  RESOLUTIONS", font(SEG_SB, S * 0.049), c, c, r_text * 0.965, INK, top=False, spacing=1.10)
    # side separator dots (coral) at 3 & 9 o'clock
    for ang in (0, 180):
        a = math.radians(ang)
        sx, sy = c + r_text * math.cos(a), c + r_text * math.sin(a)
        rr = S * 0.016
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=CORAL)
    # central mark
    draw_mark(d, c, c - S * 0.01, r_div * 0.66, ring=TEAL, dots=TEAL, mark=CORAL)
    out = img.resize((px, px), Image.LANCZOS)
    if not transparent_outside:
        base = Image.new("RGBA", (px, px), (255, 255, 255, 255))
        base.alpha_composite(out)
        out = base
    return out


def build():
    make_mark(512).save(OUT / "panchaayat-mark.png")
    make_mark(512, bg=INK).save(OUT / "panchaayat-mark-on-ink.png")
    make_horizontal(360).save(OUT / "panchaayat-logo-horizontal.png")
    make_horizontal(360, dark=True).save(OUT / "panchaayat-logo-horizontal-dark.png")
    make_seal(1000).save(OUT / "panchaayat-trust-seal.png")
    print("Saved logo assets to", OUT)


if __name__ == "__main__":
    build()
