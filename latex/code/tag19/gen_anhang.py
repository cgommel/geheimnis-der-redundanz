#!/usr/bin/env python3
# Generiert das Anhang-Material zu Tag 19:
#   - Log- und Antilog-Tafel für GF(256) als LaTeX-tabulars
#   - Farbig markierte UTAH-Raster für 10×10 (MUT) und 14×14 (GESCHAFFT)
#
# Aufruf (alle Outputs auf einmal in latex/abbildungen/tag19/):
#   python3 gen_anhang.py
#
# Verzeichnis-Konvention: dieses Skript liegt in latex/code/tag19/, das
# Output landet relativ dazu unter ../../abbildungen/tag19/.

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag13"))
from placement import _build_layout

from log_tabelle import (
    baue_tabellen, generator_polynom, rs_encode_mit_spur,
    ascii_codewords, c40_codewords_mit_spur,
)


# 18 Pastell-Farben, damit auch das 14×14-Symbol (18 Codewords) noch
# gut unterscheidbar ist. Für 10×10 (8 CW) reichen die ersten 8.
COLORS = [
    "red!15",     "orange!20",  "yellow!35",  "lime!25",
    "green!25",   "teal!25",    "cyan!25",    "blue!20",
    "violet!20",  "magenta!20", "pink!30",    "brown!25",
    "red!40",     "orange!50",  "yellow!60",  "lime!50",
    "green!50",   "teal!55",
]


# region grid
def render_grid_blank(n_inner):
    """Erzeugt TikZ-Inhalt für ein farbig markiertes Datamatrix-Symbol
    mit n_inner × n_inner Innenfläche (Symbol-Außenmaß: n_inner+2).

    Blank-Variante: jeder Datenslot bekommt Pastell-Hintergrund + ein
    "c/b"-Label (Codeword-Nummer / Bit-Nummer), aber kein Bit-Wert ist
    gesetzt. Greta füllt selbst aus."""
    layout = _build_layout(n_inner)
    n_cw = max(
        chr_ for row in layout for cell in row
        if cell is not None for chr_, _ in [cell]
    )
    lines = [
        f"% Auto-generiert von gen_anhang.py — n_inner={n_inner}, "
        f"n_codewords={n_cw}"
    ]
    for r in range(n_inner):
        for c in range(n_inner):
            cell = layout[r][c]
            x, y = c + 1, r + 1
            if cell is None:
                # Padding-Slot: graues Schraffur-Kästchen.
                lines.append(
                    f"  \\fill[gray!25] ({x},{y}) rectangle ({x+1},{y+1});"
                )
                lines.append(
                    f"  \\node[font=\\tiny, gray] at ({x+0.5},{y+0.5}) {{P}};"
                )
                continue
            chr_, bit_nr = cell
            color = COLORS[(chr_ - 1) % len(COLORS)]
            label = f"{chr_}/{bit_nr}"
            lines.append(
                f"  \\fill[{color}] ({x},{y}) rectangle ({x+1},{y+1});"
            )
            lines.append(
                f"  \\node[font=\\tiny, black!70] at "
                f"({x+0.5},{y+0.5}) {{{label}}};"
            )
    return "\n".join(lines)
# endregion


# region tabellen
def render_log_tabelle(log):
    """Liefert die log-Tabelle als LaTeX tabular (16×16)."""
    lines = [
        r"\begin{center}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.05}",
        r"\begin{tabular}{r|" + "r" * 16 + "}",
        r"\toprule",
        r"$v$ & " + " & ".join(f"\\textbf{{{c}}}" for c in range(16)) + r" \\",
        r"\midrule",
    ]
    for r in range(16):
        cells = []
        for c in range(16):
            v = r * 16 + c
            if v == 0:
                cells.append("---")
            else:
                cells.append(f"{log[v]}")
        lines.append(
            f"\\textbf{{{r * 16:3d}}} & " + " & ".join(cells) + r" \\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    return "\n".join(lines)


def render_antilog_tabelle(antilog):
    """Liefert die antilog-Tabelle als LaTeX tabular (16×16)."""
    lines = [
        r"\begin{center}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\renewcommand{\arraystretch}{1.05}",
        r"\begin{tabular}{r|" + "r" * 16 + "}",
        r"\toprule",
        r"$i$ & " + " & ".join(f"\\textbf{{{c}}}" for c in range(16)) + r" \\",
        r"\midrule",
    ]
    for r in range(16):
        cells = []
        for c in range(16):
            i = r * 16 + c
            if i >= 255:
                cells.append("---")
            else:
                cells.append(f"{antilog[i]}")
        lines.append(
            f"\\textbf{{{r * 16:3d}}} & " + " & ".join(cells) + r" \\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    return "\n".join(lines)
# endregion


# region grid_filled
def render_grid_filled(n_inner, codewords):
    """Wie render_grid_blank, aber mit gesetzten Bits (schwarz halb-
    transparent), Bit-Labels in weiß bei Bit=1 und grau bei Bit=0.
    Zum Quervergleich: Greta legt ihr handgemaltes Symbol daneben und
    sucht Diskrepanzen."""
    layout = _build_layout(n_inner)
    n_cw = len(codewords)
    lines = [
        f"% Auto-generiert von gen_anhang.py — n_inner={n_inner}, "
        f"n_codewords={n_cw} (gefüllt)"
    ]
    for r in range(n_inner):
        for c in range(n_inner):
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
            if chr_ > n_cw:
                continue
            color = COLORS[(chr_ - 1) % len(COLORS)]
            label = f"{chr_}/{bit_nr}"
            value = codewords[chr_ - 1]
            bit = (value >> (8 - bit_nr)) & 1
            lines.append(
                f"  \\fill[{color}] ({x},{y}) rectangle ({x+1},{y+1});"
            )
            if bit == 1:
                lines.append(
                    f"  \\fill[black, opacity=0.7] ({x},{y}) "
                    f"rectangle ({x+1},{y+1});"
                )
                lines.append(
                    f"  \\node[font=\\tiny, white] at "
                    f"({x+0.5},{y+0.5}) {{{label}}};"
                )
            else:
                lines.append(
                    f"  \\node[font=\\tiny, black!70] at "
                    f"({x+0.5},{y+0.5}) {{{label}}};"
                )
    return "\n".join(lines)
# endregion


# region loesung_steps
def render_g_polynom(schritte, n_ecc):
    """Tabular mit dem Aufbau von g_n(x) Schritt für Schritt."""
    lines = [
        r"\begin{center}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        r"\begin{tabular}{r|" + "r" * (n_ecc + 1) + "}",
        r"\toprule",
        r"$g_i(x)$ & " + " & ".join(
            f"$x^{{{k}}}$" for k in range(n_ecc + 1)
        ) + r" \\",
        r"\midrule",
    ]
    for i, koef in enumerate(schritte, start=1):
        cells = []
        for k in range(n_ecc + 1):
            if k < len(koef):
                cells.append(f"{koef[k]}")
            else:
                cells.append("")
        lines.append(
            f"$g_{{{i}}}$ & " + " & ".join(cells) + r" \\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    return "\n".join(lines)


def render_rs_iterationen(iterationen):
    """Pro Iteration ein eigenes tabular mit jeder GF-Multiplikation
    inkl.\\ log/antilog-Lookups. Greta kann an jeder Zelle einsteigen."""
    lines = []
    for it in iterationen:
        lines.append(r"\paragraph{Iteration " + str(it["i"])
                     + r" — Faktor $f = " + str(it["faktor"]) + r"$}")
        lines.append(
            r"\textit{Rest vorher:} "
            + r"\texttt{[" + ", ".join(str(v) for v in it["rest_vor"]) + r"]}\par"
        )
        if it["faktor"] == 0:
            lines.append(
                r"\textit{Faktor ist Null — keine Multiplikationen, "
                r"Rest bleibt unverändert.}\par"
            )
        else:
            lines.append(r"\begin{center}")
            lines.append(r"\footnotesize")
            lines.append(r"\setlength{\tabcolsep}{4pt}")
            lines.append(r"\renewcommand{\arraystretch}{1.1}")
            lines.append(r"\begin{tabular}{r|rr|rrrr|rrr}")
            lines.append(r"\toprule")
            lines.append(
                r"$j$ & $g$ & $f$ & $\log g$ & $\log f$ & $\Sigma$ "
                r"& $\Sigma\bmod 255$ & Pos & vor $\oplus$ Prod & nach \\"
            )
            lines.append(r"\midrule")
            for m in it["mults"]:
                # log-Tabellen-Lookups (für die Anzeige)
                from log_tabelle import baue_tabellen as _bt
                log, antilog = _bt()
                la = log[m["g_koeff"]]
                lb = log[m["faktor"]]
                summe_raw = la + lb
                summe = summe_raw % 255
                lines.append(
                    f"{m['j']} & {m['g_koeff']} & {m['faktor']} & "
                    f"{la} & {lb} & {summe_raw} & {summe} & "
                    f"{m['rest_pos']} & "
                    f"{m['rest_vor_pos']} $\\oplus$ {m['produkt']} & "
                    f"{m['rest_neu_pos']} \\\\"
                )
            lines.append(r"\bottomrule")
            lines.append(r"\end{tabular}")
            lines.append(r"\end{center}")
        lines.append(
            r"\textit{Rest nachher:} "
            + r"\texttt{[" + ", ".join(str(v) for v in it["rest_nach"]) + r"]}"
            + r"\par\medskip"
        )
    return "\n".join(lines)


def render_bitzerlegung(codewords):
    """Tabular mit Bit-Zerlegung (CW-Nummer, Wert, 8 Bits)."""
    lines = [
        r"\begin{center}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{4pt}",
        r"\renewcommand{\arraystretch}{1.2}",
        r"\begin{tabular}{r|r|cccccccc}",
        r"\toprule",
        r"\textbf{CW} & \textbf{Wert} & "
        r"\textbf{1} & \textbf{2} & \textbf{3} & \textbf{4} & "
        r"\textbf{5} & \textbf{6} & \textbf{7} & \textbf{8} \\",
        r"& & "
        r"\tiny 128 & \tiny 64 & \tiny 32 & \tiny 16 & "
        r"\tiny 8 & \tiny 4 & \tiny 2 & \tiny 1 \\",
        r"\midrule",
    ]
    for i, cw in enumerate(codewords, start=1):
        bits = format(cw, "08b")
        cells = " & ".join(bits)
        lines.append(f"{i} & {cw} & {cells} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    return "\n".join(lines)


def render_platzierung(n_inner):
    """Tabular für die Platzierung: Zeile/Spalte → (CW, Bit). Diente als
    Cross-Reference zum farbigen Anhang-Raster."""
    layout = _build_layout(n_inner)
    lines = [
        r"\begin{center}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{2pt}",
        r"\renewcommand{\arraystretch}{1.05}",
        r"\begin{tabular}{c|" + "c" * n_inner + "}",
        r"\toprule",
        r"$r\backslash c$ & " + " & ".join(
            str(c + 1) for c in range(n_inner)
        ) + r" \\",
        r"\midrule",
    ]
    for r in range(n_inner):
        cells = []
        for c in range(n_inner):
            cell = layout[r][c]
            if cell is None:
                cells.append(r"\textit{P}")
            else:
                chr_, bit = cell
                cells.append(f"{chr_}/{bit}")
        lines.append(f"{r + 1} & " + " & ".join(cells) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    return "\n".join(lines)


def render_c40_triplets(triplets):
    """Tabular mit C40-Triplet-Rechnungen."""
    lines = [
        r"\begin{center}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{6pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        r"\begin{tabular}{l|rrr|r|rr}",
        r"\toprule",
        r"\textbf{Tripel} & $V_1$ & $V_2$ & $V_3$ & "
        r"$\mathit{tmp}$ & $b_1$ & $b_2$ \\",
        r"\midrule",
    ]
    for t in triplets:
        z = "".join(t["zeichen"])
        v1, v2, v3 = t["werte"]
        lines.append(
            f"\\texttt{{{z}}} & {v1} & {v2} & {v3} & "
            f"{t['tmp']} & {t['b1']} & {t['b2']} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    return "\n".join(lines)
# endregion


def main():
    out_dir = os.path.join(
        os.path.dirname(__file__), "..", "..", "abbildungen", "tag19"
    )
    os.makedirs(out_dir, exist_ok=True)

    log, antilog = baue_tabellen()

    # MUT — 10×10, ASCII, n_ecc = 5
    mut_daten = ascii_codewords("MUT")
    mut_g, mut_g_steps = generator_polynom(5, log, antilog)
    mut_ecc, mut_iter = rs_encode_mit_spur(mut_daten, 5, log, antilog)
    mut_codewords = list(mut_daten) + list(mut_ecc)

    # GESCHAFFT — 14×14, C40, n_ecc = 10
    g_daten, g_triplets = c40_codewords_mit_spur("GESCHAFFT")
    g_g, g_g_steps = generator_polynom(10, log, antilog)
    g_ecc, g_iter = rs_encode_mit_spur(g_daten, 10, log, antilog)
    g_codewords = list(g_daten) + list(g_ecc)

    files = {
        # Anhang-Material (Werkstatt)
        "log_tafel.tex":          render_log_tabelle(log),
        "antilog_tafel.tex":      render_antilog_tabelle(antilog),
        "mut_blank_colored.tex":  render_grid_blank(8),
        "geschafft_blank_colored.tex": render_grid_blank(12),
        # Lösungs-Bausteine MUT
        "mut_g_polynom.tex":      render_g_polynom(mut_g_steps, 5),
        "mut_rs_iterationen.tex": render_rs_iterationen(mut_iter),
        "mut_bitzerlegung.tex":   render_bitzerlegung(mut_codewords),
        "mut_platzierung.tex":    render_platzierung(8),
        "mut_filled_colored.tex": render_grid_filled(8, mut_codewords),
        # Lösungs-Bausteine GESCHAFFT
        "geschafft_c40_triplets.tex":  render_c40_triplets(g_triplets),
        "geschafft_g_polynom.tex":     render_g_polynom(g_g_steps, 10),
        "geschafft_rs_iterationen.tex": render_rs_iterationen(g_iter),
        "geschafft_bitzerlegung.tex":  render_bitzerlegung(g_codewords),
        "geschafft_platzierung.tex":   render_platzierung(12),
        "geschafft_filled_colored.tex": render_grid_filled(12, g_codewords),
    }
    for name, content in files.items():
        path = os.path.join(out_dir, name)
        with open(path, "w") as fh:
            fh.write(content + "\n")
        print(f"  geschrieben: {path}")


if __name__ == "__main__":
    main()
