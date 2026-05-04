#!/usr/bin/env python3
# Generiert TikZ-Code für ein farbig markiertes 12×12-Datamatrix-Symbol:
# pro Codeword eine eigene Pastellfarbe, in jedem Modul die Bit-Nummer.
#
# Aufruf: python3 gen_colored.py HONIG > honig_colored.tex

import sys
from placement import _build_layout

# 12 Pastell-Farben für die 12 Codewörter (Daten + ECC).
COLORS = [
    "red!15", "orange!20", "yellow!30", "lime!20", "green!20",
    "teal!20", "cyan!20", "blue!15", "violet!15", "magenta!15",
    "pink!25", "brown!20",
]


def render(codewords, name):
    layout = _build_layout(10)
    lines = [f"% Auto-generiert von gen_colored.py — Codewords {name}"]
    # Pro Codeword die Cursor-Position finden (= wo Bit 8 liegt) für die
    # Pfad-Linie unten.
    cursor_pos = {}  # chr_ → (symbol_row, symbol_col), Mitte des Moduls
    for r in range(10):
        for c in range(10):
            cell = layout[r][c]
            x, y = c + 1, r + 1
            if cell is None:
                lines.append(
                    f"  \\fill[gray!25] ({x},{y}) rectangle ({x+1},{y+1});"
                )
                lines.append(
                    f"  \\node[font=\\tiny, gray] at ({x+0.5},{y+0.5}) {{P}};"
                )
                continue
            chr_, bit_nr = cell
            if not (1 <= chr_ <= len(codewords)):
                continue
            if bit_nr == 8:
                cursor_pos[chr_] = (y + 0.5, x + 0.5)
            color = COLORS[chr_ - 1]
            value = codewords[chr_ - 1]
            bit = (value >> (8 - bit_nr)) & 1
            lines.append(
                f"  \\fill[{color}] ({x},{y}) rectangle ({x+1},{y+1});"
            )
            label = f"{chr_}/{bit_nr}"
            if bit == 1:
                lines.append(
                    f"  \\fill[black, opacity=0.65] ({x},{y}) rectangle ({x+1},{y+1});"
                )
                lines.append(
                    f"  \\node[font=\\tiny, white] at ({x+0.5},{y+0.5}) {{{label}}};"
                )
            else:
                lines.append(
                    f"  \\node[font=\\tiny, black!70] at ({x+0.5},{y+0.5}) {{{label}}};"
                )
    # --- Cursor-Pfad: rote Pfeillinie zwischen den Bit-8-Positionen
    # der aufeinanderfolgenden Codewörter ---
    lines.append("  % Cursor-Pfad (rote Linie zwischen den Codewort-Ankern)")
    prev = None
    for chr_ in range(1, len(codewords) + 1):
        if chr_ not in cursor_pos:
            continue
        cur = cursor_pos[chr_]
        if prev is not None:
            lines.append(
                f"  \\draw[red, very thick, opacity=0.85, ->, "
                f">=stealth] ({prev[1]},{prev[0]}) -- ({cur[1]},{cur[0]});"
            )
        prev = cur
    # Start-Marker
    if 1 in cursor_pos:
        sr, sc = cursor_pos[1]
        lines.append(
            f"  \\node[red, font=\\scriptsize\\bfseries] "
            f"at ({sc-0.6},{sr-0.6}) {{Start}};"
        )
    return "\n".join(lines)


# Wir definieren die zwei verwendeten Test-Wörter direkt hier; bei
# Bedarf kann man weitere Codeword-Listen ergänzen.
WORDS = {
    "HONIG": [73, 80, 79, 74, 72, 70, 186, 97, 167, 44, 40, 243],
    "GRETA": [72, 83, 70, 85, 66, 64, 90, 71, 128, 186, 106, 125],
}


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in WORDS:
        name = sys.argv[1]
        print(render(WORDS[name], name))
    else:
        print(f"Usage: python3 {sys.argv[0]} {{HONIG|GRETA}}", file=sys.stderr)
        sys.exit(1)
