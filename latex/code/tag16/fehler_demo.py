# Etappe 16, Stufe 2: empirischer Stress-Test der RS-Korrektur.
#
# Wir nehmen ein Datamatrix-Symbol, kippen schrittweise immer mehr
# zufällige Datenmodule um und messen, in wievielen Fällen der
# Decoder den Klartext noch zurückbekommt. Das Ergebnis ist ein
# Diagramm "Fehler vs. Erfolgsquote" — die theoretische RS-Grenze
# wird sichtbar.

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag15"))
from encoder_klasse import DatamatrixEncoder  # noqa: E402

sys.path.insert(0, os.path.dirname(__file__))
from decoder import DatamatrixDecoder  # noqa: E402


# region experiment
def kippe_module(matrix, anzahl, n=12, rng=None):
    """Liefert eine Kopie der Matrix, in der `anzahl` zufällige
    Datenmodule (also nicht Frame-Module) geflippt sind."""
    if rng is None:
        rng = random.Random()
    daten_pos = [
        (r, c)
        for r in range(1, n - 1)
        for c in range(1, n - 1)
    ]
    flips = rng.sample(daten_pos, anzahl)
    neu = [row[:] for row in matrix]
    for r, c in flips:
        neu[r][c] ^= 1
    return neu


def erfolgsquote(klartext, original_matrix, anzahl_fehler,
                 versuche=200, n=12, seed=42):
    """Wie oft wird der Klartext bei `anzahl_fehler` zufällig
    geflippten Modulen noch erfolgreich rekonstruiert?"""
    rng = random.Random(seed)
    treffer = 0
    for _ in range(versuche):
        m = kippe_module(original_matrix, anzahl_fehler, n=n, rng=rng)
        d = DatamatrixDecoder(m)
        if d.erfolgreich and d.klartext == klartext:
            treffer += 1
    return treffer / versuche
# endregion


# region diagramm
def diagramm_als_tikz(daten, dateiname, theoretische_grenze=None):
    """daten: Liste von (anzahl_fehler, erfolgsquote)-Paaren.
    theoretische_grenze: x-Wert, an dem der RS-Decoder garantiert
    versagt (= Anzahl_ECC // 2 + 1).

    Schreibt einen \\begin{tikzpicture}…\\end{tikzpicture}-Block — der
    wird im Buch via \\input eingebunden und damit als saubere
    Vektorgrafik gesetzt."""
    max_fehler = max(p[0] for p in daten) or 1
    breite_in_cm = 12  # x-Achsen-Länge (Plot-Bereich)
    hoehe_in_cm = 6    # y-Achsen-Länge

    def x(p):
        return p / max_fehler * breite_in_cm

    def y(q):
        return q * hoehe_in_cm

    lines = []
    lines.append("\\begin{tikzpicture}[x=1cm, y=1cm, font=\\footnotesize]")
    # Achsen
    lines.append(f"  \\draw[->] (0,0) -- ({breite_in_cm + 0.4},0) "
                 "node[below right] {Anzahl geflippter Module};")
    lines.append(f"  \\draw[->] (0,0) -- (0,{hoehe_in_cm + 0.4}) "
                 "node[above left, rotate=90, anchor=south west] "
                 "{Erfolgsquote};")
    # y-Gitter + Beschriftung (0%, 25%, 50%, 75%, 100%)
    for q in (0.0, 0.25, 0.5, 0.75, 1.0):
        yc = y(q)
        lines.append(
            f"  \\draw[gray!30] (0,{yc:.3f}) -- "
            f"({breite_in_cm:.3f},{yc:.3f});"
        )
        lines.append(
            f"  \\node[anchor=east] at (-0.1,{yc:.3f}) "
            f"{{{int(q * 100)}\\%}};"
        )
    # x-Achsenbeschriftung
    for i in range(0, max_fehler + 1, max(1, max_fehler // 8)):
        xc = x(i)
        lines.append(
            f"  \\draw ({xc:.3f},-0.05) -- ({xc:.3f},-0.15);"
        )
        lines.append(
            f"  \\node[anchor=north] at ({xc:.3f},-0.15) {{{i}}};"
        )
    # Theoretische Grenze
    if theoretische_grenze is not None and theoretische_grenze <= max_fehler:
        xg = x(theoretische_grenze)
        lines.append(
            f"  \\draw[red, thick] ({xg:.3f},0) -- "
            f"({xg:.3f},{hoehe_in_cm:.3f});"
        )
        lines.append(
            f"  \\node[red, anchor=south west, font=\\scriptsize] "
            f"at ({xg + 0.05:.3f},{hoehe_in_cm - 0.4:.3f}) "
            f"{{RS-Grenze}};"
        )
    # Polylinie
    pfad = " -- ".join(
        f"({x(p[0]):.3f},{y(p[1]):.3f})" for p in daten
    )
    lines.append(f"  \\draw[blue, very thick] {pfad};")
    # Punkte
    for p, q in daten:
        lines.append(
            f"  \\fill[blue] ({x(p):.3f},{y(q):.3f}) circle (2pt);"
        )
    lines.append("\\end{tikzpicture}")

    with open(dateiname, "w", encoding="utf-8") as f:
        f.write("% Auto-generiert von fehler_demo.py\n")
        f.write("\n".join(lines) + "\n")
# endregion


# region demo
if __name__ == "__main__":
    klartext = "GRETA"
    encoder = DatamatrixEncoder(klartext)
    matrix = encoder.bitmap()
    print(f"Symbol: {encoder!r}")

    # Wir wissen: theoretische RS-Grenze = ECC_Anzahl // 2.
    # Bei 7 ECC-Codewords sind das 3 Codewords. Wieviele zufällig
    # geflippte MODULE entsprechen 3 betroffenen Codewords? Das hängt
    # von Streuung ab — und genau das messen wir empirisch.
    _, ecc = encoder.SYMBOL_TABLE[encoder.n]
    rs_grenze_codewords = ecc // 2

    daten = []
    for n_fehler in range(0, 17):
        q = erfolgsquote(klartext, matrix, n_fehler, versuche=200)
        daten.append((n_fehler, q))
        balken = "#" * int(round(q * 30))
        print(f"  {n_fehler:2d} Modul-Flips: {q*100:5.1f}%  {balken}")

    # Im Diagramm zeigen wir die theoretische Grenze in Codewords
    # (jedes Codeword hat 8 Bits, also kann ein einzelner Modul-Flip
    # potenziell ein Codeword kaputt machen — die untere Grenze für
    # das Versagen ist also rs_grenze_codewords + 1 Module).
    diagramm_als_tikz(
        daten, "fehler_demo_diagramm.tex",
        theoretische_grenze=rs_grenze_codewords + 1,
    )
    print("→ fehler_demo_diagramm.tex (als \\input ins Buch eingebunden)")
# endregion
