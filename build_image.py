#!/usr/bin/env python3
"""Draw "The World Today" — a one-image newspaper front page summing up
Friday, 20 November 2026. Written from scratch with PIL; no photos, no
network. Run: python3 build_image.py  (writes entry.png next to this file)
or: python3 build_image.py /path/to/entry.png
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---- palette (newsprint) ----
PAPER = (248, 244, 233)
INK = (18, 18, 18)
RED = (163, 30, 30)
BLUE = (28, 68, 128)
SKY = (214, 228, 240)
RIVER = (64, 110, 168)
GRAY = (110, 110, 104)
LIGHT = (238, 232, 218)
GOLD = (198, 142, 24)
GREEN = (46, 125, 62)
ORANGE = (232, 120, 28)
YELLOW = (245, 196, 66)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
]


def load_font(names, size):
    """First matching font file from the usual system dirs, else PIL default."""
    for d in FONT_DIRS:
        for name in names:
            path = os.path.join(d, name)
            if os.path.isfile(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
    return ImageFont.load_default()


def serif_bold(size):
    return load_font(["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf",
                      "NotoSerif-Bold.ttf"], size)


def serif(size):
    return load_font(["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf",
                      "NotoSerif-Regular.ttf"], size)


def serif_italic(size):
    return load_font(["DejaVuSerif-Italic.ttf", "LiberationSerif-Italic.ttf",
                      "NotoSerif-Italic.ttf"], size)


def sans_bold(size):
    return load_font(["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf",
                      "NotoSans-Bold.ttf"], size)


def sans(size):
    return load_font(["DejaVuSans.ttf", "LiberationSans-Regular.ttf",
                      "NotoSans-Regular.ttf"], size)


def wrap(draw, text, font, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, font, color, max_w, leading):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, font, max_w):
        draw.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- icons
def icon_bridge(d, x, y, w, h):
    """A bridge over a river, hit by an explosion."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # river
    d.rectangle([x, y + h - 34, x + w, y + h], fill=RIVER)
    d.line([(x, y + h - 30), (x + w, y + h - 30)], fill=(140, 180, 215), width=2)
    d.line([(x, y + h - 18), (x + w, y + h - 18)], fill=(140, 180, 215), width=2)
    # bridge deck + arch
    deck_y = y + h - 62
    d.line([(x + 6, deck_y), (x + w - 6, deck_y)], fill=INK, width=6)
    d.arc([x + 14, deck_y - 26, x + w - 14, deck_y + 26], start=180, end=360,
          fill=INK, width=4)
    for px in (x + 34, x + w // 2, x + w - 34):
        d.line([(px, deck_y - 22), (px, deck_y)], fill=INK, width=4)
    # towers
    d.rectangle([x + 30, deck_y - 44, x + 38, deck_y], fill=INK)
    d.rectangle([x + w - 38, deck_y - 44, x + w - 30, deck_y], fill=INK)
    # explosion burst at the centre of the deck (orange, outlined, with sparks)
    cx, cy = x + w // 2, deck_y - 6
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        r = 34 if i % 2 == 0 else 15
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=ORANGE, outline=(140, 20, 10))
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=YELLOW,
              outline=(140, 20, 10))
    for sx, sy in ((cx - 44, cy - 18), (cx + 44, cy - 14), (cx - 36, cy + 12),
                   (cx + 38, cy + 14)):
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=RED)
    # smoke puffs
    for sx, sy, sr in ((cx - 52, cy - 40, 12), (cx + 50, cy - 36, 10),
                       (cx - 34, cy - 58, 9)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 116))


def icon_chart(d, x, y, w, h):
    """A falling market chart: red line down, candlesticks."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    # grid
    for gy in (y + 28, y + 58, y + 88):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(222, 222, 214), width=1)
    # candlesticks, falling
    candles = [(14, 34, 10, 26), (38, 46, 10, 30), (62, 58, 10, 34),
               (86, 74, 10, 30)]
    for cx, cy, cw, ch in candles:
        d.rectangle([x + cx, y + cy, x + cx + cw, y + cy + ch], fill=RED)
        d.line([(x + cx + cw // 2, y + cy - 8), (x + cx + cw // 2, y + cy + ch + 8)],
               fill=RED, width=2)
    # jagged falling line with arrowhead
    pts = [(x + 10, y + 26), (x + 34, y + 40), (x + 52, y + 36),
           (x + 74, y + 62), (x + 96, y + 58), (x + w - 12, y + 96)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ax, ay = x + w - 12, y + 96
    d.polygon([(ax, ay), (ax - 12, ay - 2), (ax - 2, ay - 12)], fill=RED)


def icon_intercept(d, x, y, w, h):
    """A missile intercepted in the sky above a shield dome."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # dome
    d.arc([x + 14, y + h - 52, x + w - 14, y + h + 30], start=180, end=360,
          fill=BLUE, width=4)
    d.line([(x + 14, y + h - 10), (x + w - 14, y + h - 10)], fill=BLUE, width=3)
    # rising missile (small rocket) with trail
    mx, my = x + 30, y + h - 58
    d.line([(mx - 14, my + 26), (mx, my + 4)], fill=GRAY, width=3)
    d.polygon([(mx, my), (mx - 7, my + 16), (mx + 7, my + 16)], fill=INK)
    d.rectangle([mx - 5, my + 14, mx + 5, my + 26], fill=INK)
    # interceptor burst (orange, outlined, with sparks)
    cx, cy = x + w - 34, y + 34
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        r = 26 if i % 2 == 0 else 11
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=ORANGE, outline=(140, 20, 10))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=YELLOW,
              outline=(140, 20, 10))
    for dx, dy in ((cx - 26, cy + 18), (cx + 24, cy + 20), (cx + 28, cy - 8)):
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)


def icon_game(d, x, y, w, h):
    """A game controller with a gold coin."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
    # controller body
    bx, by, bw, bh = x + 12, y + 34, w - 24, 56
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=18, fill=(52, 52, 64))
    # d-pad
    d.rectangle([bx + 12, by + 22, bx + 34, by + 32], fill=(200, 200, 210))
    d.rectangle([bx + 18, by + 16, bx + 28, by + 38], fill=(200, 200, 210))
    # buttons
    for bxx, byy, col in ((bx + bw - 34, by + 16, YELLOW),
                          (bx + bw - 24, by + 26, RED),
                          (bx + bw - 44, by + 26, GREEN),
                          (bx + bw - 34, by + 36, BLUE)):
        d.ellipse([bxx, byy, bxx + 10, byy + 10], fill=col)
    # sticks
    for sx in (bx + 44, bx + bw - 58):
        d.ellipse([sx, by + 38, sx + 14, by + 52], fill=(140, 140, 150))
    # gold coin with $
    cx, cy, r = x + w - 26, y + 22, 16
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    d.ellipse([cx - r + 4, cy - r + 4, cx + r - 4, cy + r - 4],
              outline=(255, 230, 150), width=2)
    f = sans_bold(20)
    d.text((cx - 6, cy - 12), "$", font=f, fill=(120, 84, 8))


def icon_flags(d, x, y, w, h):
    """EU flag and UK flag side by side, joined by a link."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    import math
    # EU flag: blue field, ring of 12 gold stars
    ex, ey, ew, eh = x + 8, y + 30, 48, 32
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(0, 51, 153))
    ccx, ccy = ex + ew // 2, ey + eh // 2
    for i in range(12):
        ang = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = ccx + 11 * math.cos(ang), ccy + 8 * math.sin(ang)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=YELLOW)
    # link
    d.line([(ex + ew + 2, ey + eh // 2), (x + w - 58, ey + eh // 2)],
           fill=INK, width=3)
    # UK flag: simplified Union Jack
    ux, uy, uw, uh = x + w - 56, y + 30, 48, 32
    d.rectangle([ux, uy, ux + uw, uy + uh], fill=(0, 36, 125))
    d.line([(ux, uy), (ux + uw, uy + uh)], fill=(255, 255, 255), width=7)
    d.line([(ux + uw, uy), (ux, uy + uh)], fill=(255, 255, 255), width=7)
    d.line([(ux, uy), (ux + uw, uy + uh)], fill=(200, 16, 46), width=3)
    d.line([(ux + uw, uy), (ux, uy + uh)], fill=(200, 16, 46), width=3)
    d.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)], fill=(255, 255, 255),
           width=9)
    d.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)], fill=(255, 255, 255),
           width=9)
    d.line([(ux + uw // 2, uy), (ux + uw // 2, uy + uh)], fill=(200, 16, 46),
           width=5)
    d.line([(ux, uy + uh // 2), (ux + uw, uy + uh // 2)], fill=(200, 16, 46),
           width=5)


def icon_plane(d, x, y, w, h):
    """A grounded plane on a runway with a stop sign."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # runway
    d.rectangle([x, y + h - 26, x + w, y + h - 14], fill=(90, 90, 90))
    for rx in range(x + 8, x + w - 8, 24):
        d.line([(rx, y + h - 20), (rx + 12, y + h - 20)], fill=(255, 255, 255),
               width=2)
    # plane fuselage (side view, nose right)
    px, py = x + 14, y + 44
    d.ellipse([px, py, px + 76, py + 22], fill=(30, 60, 110))
    d.polygon([(px + 66, py + 2), (px + 92, py + 10), (px + 66, py + 20)],
              fill=(30, 60, 110))
    # tail fin
    d.polygon([(px + 6, py + 6), (px + 16, py - 16), (px + 26, py + 6)],
              fill=(30, 60, 110))
    # wing
    d.polygon([(px + 30, py + 16), (px + 48, py + 16), (px + 58, py + 34),
               (px + 40, py + 34)], fill=(20, 46, 88))
    # windows
    for wx in range(px + 12, px + 62, 12):
        d.ellipse([wx, py + 6, wx + 6, py + 12], fill=(180, 220, 245))
    # stop octagon
    cx, cy, r = x + w - 28, y + 30, 20
    import math
    oct_pts = []
    for i in range(8):
        ang = math.pi * i / 4 + math.pi / 8
        oct_pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(oct_pts, fill=RED)
    f = sans_bold(11)
    tw = d.textlength("STOP", font=f)
    d.text((cx - tw / 2, cy - 7), "STOP", font=f, fill=(255, 255, 255))


def icon_globe(d, x, y, w, h):
    """A warming globe with a rising thermometer."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    # globe
    cx, cy, r = x + 48, y + h // 2 + 4, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 220))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=3)
    # land blobs
    d.ellipse([cx - 28, cy - 22, cx - 4, cy - 2], fill=GREEN)
    d.ellipse([cx - 2, cy + 2, cx + 24, cy + 22], fill=GREEN)
    d.ellipse([cx + 8, cy - 26, cx + 26, cy - 8], fill=GREEN)
    # latitude lines
    d.arc([cx - r, cy - 14, cx + r, cy + 14], start=0, end=180,
          fill=(140, 200, 240), width=2)
    d.arc([cx - r, cy - 30, cx + r, cy + 30], start=20, end=160,
          fill=(140, 200, 240), width=2)
    # thermometer
    tx = x + w - 24
    d.rounded_rectangle([tx - 6, y + 18, tx + 6, y + h - 34], radius=6,
                        fill=(255, 255, 255), outline=RED, width=3)
    d.rectangle([tx - 3, y + 30, tx + 3, y + h - 34], fill=RED)
    d.ellipse([tx - 11, y + h - 40, tx + 11, y + h - 18], fill=RED)
    # ticks
    for ty in (y + 30, y + 48, y + 66):
        d.line([(tx + 6, ty), (tx + 12, ty)], fill=RED, width=2)


# ---------------------------------------------------------------- page
STORIES = [
    # (kicker, headline, summary, icon)
    ("MIDDLE EAST", "SAUDI SHOOTS DOWN HOUTHI MISSILE",
     "Air defences intercept a ballistic missile and drones aimed at the "
     "south; alerts in Jazan, Abha and Khamis Mushait.", icon_intercept),
    ("GAMES", "GTA 6'S RECORD FIRST DAY",
     "An estimated $2.36bn from 24.6m copies \u2014 the biggest "
     "entertainment launch ever.", icon_game),
    ("EUROPE", "UK AND EU AGREE RESET DEAL",
     "Brussels summit agrees food trade, youth mobility and linked carbon "
     "markets.", icon_flags),
    ("TRAVEL", "US AIR TRAVEL HALTED",
     "FAA orders a nationwide ground stop; 1.5m passengers hit and 9,000 "
     "flights cancelled.", icon_plane),
    ("CLIMATE", "COP31 ENDS IN DEADLOCK",
     "Talks close with no fossil-fuel deal; campaigners call it the worst "
     "COP ever. Turkey leaves with $26bn in green deals.", icon_globe),
    ("MARKETS", "ASIA'S MARKETS PLUNGE",
     "Nikkei falls 5.1% to a seven-month low; SoftBank slides 14.5% as the "
     "AI sell-off spreads.", icon_chart),
]

LEAD_KICKER = "UKRAINE \u2022 LEAD"
LEAD_HEADLINE = "RUSSIA STRIKES KYIV'S BRIDGES"
LEAD_SUMMARY = (
    "Missiles hit three crossings over the Dnipro; 3 killed, 15 hurt. "
    "Power and water cut across the capital as Russia answers the "
    "Crimea bridge attacks."
)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    # outer border
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)
    d.rectangle([16, 16, W - 17, H - 17], outline=INK, width=1)

    # ---- masthead ----
    f_mast = serif_bold(74)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 34), title, font=f_mast, fill=INK)
    rule(d, M, 128, W - M, 2)
    f_date = sans_bold(30)
    date = "FRIDAY, 20 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 140), date, font=f_date, fill=RED)
    f_tag = serif_italic(19)
    tag = "Seven stories from one day around the world"
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 178), tag, font=f_tag, fill=GRAY)
    rule(d, M, 208, W - M, 4)
    rule(d, M, 214, W - M, 1)

    # ---- lead story ----
    ly = 232
    lw = 400  # lead visual width
    lh = 196
    d.rectangle([M, ly, M + lw, ly + lh], outline=INK, width=2)
    icon_bridge(d, M + 2, ly + 2, lw - 4, lh - 4)
    tx = M + lw + 20
    tw_col = W - M - tx
    f_kick = sans_bold(17)
    d.text((tx, ly + 2), LEAD_KICKER, font=f_kick, fill=RED)
    f_head = serif_bold(40)
    y = text_block(d, tx, ly + 28, LEAD_HEADLINE, f_head, INK, tw_col, 46)
    f_sum = sans(20)
    text_block(d, tx, y + 8, LEAD_SUMMARY, f_sum, INK, tw_col, 26)
    rule(d, M, ly + lh + 18, W - M, 2)

    # ---- grid of six stories: 2 columns x 3 rows ----
    gy = ly + lh + 36
    gap_x, gap_y = 20, 14
    cell_w = (W - 2 * M - gap_x) // 2
    cell_h = 148
    for i, (kicker, headline, summary, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        cx = M + col * (cell_w + gap_x)
        cy = gy + row * (cell_h + gap_y)
        # icon box
        iw = 118
        d.rectangle([cx, cy, cx + iw, cy + cell_h - 8], outline=INK, width=2)
        icon(d, cx + 2, cy + 2, iw - 4, cell_h - 12)
        tx2 = cx + iw + 12
        tw2 = cx + cell_w - tx2
        f_k2 = sans_bold(15)
        d.text((tx2, cy + 2), kicker, font=f_k2, fill=RED)
        f_h2 = sans_bold(21)
        y2 = text_block(d, tx2, cy + 24, headline, f_h2, INK, tw2, 25)
        f_s2 = sans(15)
        text_block(d, tx2, y2 + 4, summary, f_s2, INK, tw2, 19)
        if col == 0:
            d.line([(cx + cell_w + gap_x // 2, cy),
                    (cx + cell_w + gap_x // 2, cy + cell_h - 8)],
                   fill=(200, 194, 178), width=1)

    # ---- footer ----
    fy = gy + 3 * cell_h + 2 * gap_y + 10
    rule(d, M, fy, W - M, 4)
    rule(d, M, fy + 6, W - M, 1)
    f_foot = sans_bold(17)
    foot = "FRIDAY, 20 NOVEMBER 2026  \u2022  THE WORLD TODAY"
    tw = d.textlength(foot, font=f_foot)
    d.text(((W - tw) / 2, fy + 16), foot, font=f_foot, fill=INK)
    f_note = serif_italic(15)
    note = "Drawn in code \u2022 No photographs \u2022 Seven stories, one day"
    tw = d.textlength(note, font=f_note)
    d.text(((W - tw) / 2, fy + 42), note, font=f_note, fill=GRAY)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = draw_page()
    img.save(out, format="PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
