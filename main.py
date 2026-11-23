"""news-image-20261123: draw one newspaper-style image of the world's
news of Monday 23 November 2026, using only the Python standard library.

The program builds a 1024x1024 RGB canvas in memory, draws a masthead,
five labelled story panels and a footer ticker with a small 5x7 bitmap
font, then writes a deterministic PNG (zlib + CRC, no timestamps) to
/output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png for local runs).
Running it twice produces identical bytes.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 243, 232)
INK = (20, 33, 61)
NAVY = (20, 33, 61)
RED = (180, 35, 24)
TEAL = (14, 116, 110)
GOLD = (184, 134, 11)
BLUE = (37, 99, 235)
ORANGE = (217, 119, 6)
GREEN = (22, 101, 52)
WHITE = (255, 255, 255)
LIGHT = (226, 232, 240)
GREY = (71, 85, 105)

# 5x7 bitmap glyphs, one string per row, "#" = on pixel.
GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        self.fill_rect(0, 0, w, h, bg)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            for xx in range(max(0, x), min(self.w, x + w)):
                self.px[base], self.px[base + 1], self.px[base + 2] = color
                base += 3

    def rect(self, x, y, w, h, color, t=2):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, x1, y1, x2, y2, x3, y3, color):
        # Fill by scanline: sample the bounding box, point-in-triangle test.
        minx, maxx = min(x1, x2, x3), max(x1, x2, x3)
        miny, maxy = min(y1, y2, y3), max(y1, y2, y3)
        d = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        if d == 0:
            return
        for yy in range(miny, maxy + 1):
            for xx in range(minx, maxx + 1):
                a = ((y2 - y3) * (xx - x3) + (x3 - x2) * (yy - y3)) / d
                b = ((y3 - y1) * (xx - x3) + (x1 - x3) * (yy - y3)) / d
                c = 1 - a - b
                if a >= 0 and b >= 0 and c >= 0:
                    self.set(xx, yy, color)

    def text_width(self, text, scale):
        return len(text) * 6 * scale - scale

    def draw_text(self, x, y, text, scale, color):
        cx = x
        for ch in text.upper():
            glyph = GLYPHS.get(ch, GLYPHS["?"])
            for row in range(7):
                for col in range(5):
                    if glyph[row][col] == "1":
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def draw_centred(self, cx, y, text, scale, color):
        w = self.text_width(text, scale)
        self.draw_text(cx - w // 2, y, text, scale, color)

    def draw_wrapped(self, x, y, text, scale, color, max_w, line_h):
        words = text.split(" ")
        lines = []
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if self.text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        yy = y
        for line in lines:
            self.draw_text(x, yy, line, scale, color)
            yy += line_h
        return yy


def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(canvas, path):
    raw = bytearray()
    for yy in range(canvas.h):
        raw.append(0)
        start = yy * canvas.w * 3
        raw += canvas.px[start:start + canvas.w * 3]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def draw_icon(c, kind, cx, cy, r):
    """Simple geometric emblem inside a panel header circle."""
    if kind == "globe":
        c.circle(cx, cy, r, BLUE)
        c.circle(cx - r // 3, cy - r // 4, r // 3, GREEN)
        c.circle(cx + r // 3, cy + r // 4, r // 4, GREEN)
        c.circle(cx + r // 2, cy - r // 2, r // 5, GREEN)
    elif kind == "flame":
        c.circle(cx, cy, r, RED)
        c.triangle(cx, cy - r + 6, cx - r // 2, cy + r // 2,
                   cx + r // 2, cy + r // 2, ORANGE)
        c.circle(cx, cy + r // 4, r // 4, GOLD)
    elif kind == "building":
        c.circle(cx, cy, r, NAVY)
        c.fill_rect(cx - r // 2, cy - r // 3, r // 4, r // 2 + 6, WHITE)
        c.fill_rect(cx + r // 8, cy - r // 2, r // 4, r // 2 + 12, WHITE)
        c.triangle(cx - r // 2, cy - r // 3, cx, cy - r + 4,
                   cx + r // 2, cy - r // 3, ORANGE)
    elif kind == "badge":
        c.circle(cx, cy, r, GOLD)
        c.circle(cx, cy, r - 8, NAVY)
        c.triangle(cx, cy - 12, cx - 11, cy, cx + 11, cy, WHITE)
        c.triangle(cx - 11, cy, cx + 11, cy, cx, cy + 12, WHITE)
    elif kind == "mountain":
        c.circle(cx, cy, r, TEAL)
        c.triangle(cx - r + 4, cy + r // 2, cx - r // 3, cy - r + 8,
                   cx + r // 4, cy + r // 2, WHITE)
        c.triangle(cx - r // 4, cy + r // 2, cx + r // 3, cy - r // 2,
                   cx + r - 4, cy + r // 2, PAPER)


def panel(c, x, y, w, h, tag, headline, body, accent, icon, fact):
    c.fill_rect(x, y, w, h, WHITE)
    c.rect(x, y, w, h, INK, 3)
    c.fill_rect(x, y, w, 44, accent)
    c.draw_text(x + 14, y + 13, tag, 2, WHITE)
    yy = y + 58
    for line in headline:
        c.draw_text(x + 14, yy, line, 3, INK)
        yy += 26
    yy += 8
    c.draw_wrapped(x + 14, yy, body, 2, GREY, w - 28, 20)
    # Key fact strip and emblem fill the lower half of the panel.
    c.draw_text(x + 14, y + h - 72, fact, 3, accent)
    draw_icon(c, icon, x + w - 52, y + h - 56, 34)


def main():
    c = Canvas(W, H, PAPER)

    # Masthead.
    c.fill_rect(0, 0, W, 150, NAVY)
    c.fill_rect(0, 150, W, 6, RED)
    c.draw_centred(W // 2, 14, "MONDAY", 3, GOLD)
    c.draw_centred(W // 2, 48, "23 NOVEMBER 2026", 6, WHITE)
    c.draw_centred(W // 2, 118, "THE WORLD'S NEWS IN ONE IMAGE", 2, LIGHT)

    # Lead row: COP31 (left, wide) and Ukraine (right).
    panel(c, 16, 168, 620, 372, "CLIMATE  -  TURKIYE",
          ["COP31 COLLAPSES", "WITH NO DEAL"],
          "Talks in Antalya end with no agreement. "
          "The final draft leaves out fossil fuels, "
          "and the EU and others reject a deal "
          "without a phase-out. Climate diplomacy "
          "is left in doubt.",
          RED, "globe", "NO NEW TEXT")
    panel(c, 652, 168, 356, 372, "WAR  -  UKRAINE",
          ["DRONE HITS", "KYIV REGION"],
          "A Russian drone hits a building "
          "in the Kyiv region. At least 14 "
          "people are missing, President "
          "Zelenskiy says, as rescuers "
          "search the rubble.",
          NAVY, "building", "14 MISSING")

    # Second row: three panels.
    panel(c, 16, 556, 320, 312, "DISASTER  -  INDONESIA",
          ["FACTORY FIRE", "SEARCH RESUMES"],
          "Search resumes on Monday at the "
          "candy factory in Cikande, Java. "
          "Police remove 24 body bags and "
          "dozens of workers are missing.",
          ORANGE, "flame", "24 BODY BAGS")
    panel(c, 352, 556, 320, 312, "CRIME  -  MEXICO",
          ["CARTEL BOSS", "CAPTURED"],
          "Mexico captures FBI most-wanted "
          "cartel boss El Chapo Isidro. "
          "Firefights in Sinaloa leave "
          "11 people dead.",
          TEAL, "badge", "11 DEAD")
    panel(c, 688, 556, 320, 312, "DIPLOMACY  -  DELHI",
          ["NEPAL PM", "MEETS MODI"],
          "Nepal PM Balendra Shah holds "
          "bilateral talks with PM Modi "
          "in New Delhi, on a state visit "
          "to India, 22-23 November.",
          GREEN, "mountain", "22-23 NOV")

    # Footer ticker: two more stories of the day.
    c.fill_rect(16, 884, 992, 124, NAVY)
    c.draw_text(32, 900, "ALSO TODAY", 2, GOLD)
    c.draw_wrapped(32, 928, "SOUTH KOREA: EDUCATION MINISTER QUITS "
                   "OVER AI EXAM CHEATING.  SPORT: INDIA POST "
                   "A RECORD 720/9D IN THE WELLINGTON TEST "
                   "AGAINST NEW ZEALAND.",
                   2, WHITE, 960, 20)
    c.draw_text(32, 984, "REPORTED ON 23 NOVEMBER 2026", 2, LIGHT)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    write_png(c, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
