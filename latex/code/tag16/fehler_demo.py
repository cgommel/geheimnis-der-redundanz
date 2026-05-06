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

from PIL import Image, ImageDraw  # noqa: E402


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
def diagramm_speichern(daten, dateiname, titel,
                       theoretische_grenze=None):
    """daten: Liste von (anzahl_fehler, erfolgsquote)-Paaren.
    theoretische_grenze: x-Wert, an dem der RS-Decoder garantiert
    versagt (= Anzahl_ECC // 2 + 1)."""
    breite, hoehe = 600, 360
    rand = 50
    plot_b = breite - 2 * rand
    plot_h = hoehe - 2 * rand

    bild = Image.new("RGB", (breite, hoehe), color="white")
    d = ImageDraw.Draw(bild)

    # Achsen
    d.line([(rand, hoehe - rand), (breite - rand, hoehe - rand)],
           fill="black", width=2)
    d.line([(rand, hoehe - rand), (rand, rand)], fill="black", width=2)

    max_fehler = max(p[0] for p in daten) or 1
    schritt_x = plot_b / max_fehler

    # y-Gitter (0%, 25%, 50%, 75%, 100%)
    for q in (0, 0.25, 0.5, 0.75, 1.0):
        y = hoehe - rand - int(q * plot_h)
        d.line([(rand - 4, y), (breite - rand, y)], fill="lightgray")
        d.text((rand - 38, y - 8), f"{int(q*100):3d}%", fill="black")

    # x-Achsenbeschriftung
    for i in range(0, max_fehler + 1, max(1, max_fehler // 8)):
        x = rand + int(i * schritt_x)
        d.line([(x, hoehe - rand), (x, hoehe - rand + 4)], fill="black")
        d.text((x - 6, hoehe - rand + 6), str(i), fill="black")

    # Theoretische Grenze als senkrechte Linie
    if theoretische_grenze is not None and theoretische_grenze <= max_fehler:
        x = rand + int(theoretische_grenze * schritt_x)
        d.line([(x, rand), (x, hoehe - rand)],
               fill="red", width=1)
        d.text((x + 4, rand + 2), "RS-Grenze", fill="red")

    # Datenpunkte + Linie
    punkte = [
        (rand + int(p[0] * schritt_x),
         hoehe - rand - int(p[1] * plot_h))
        for p in daten
    ]
    for a, b in zip(punkte, punkte[1:]):
        d.line([a, b], fill="blue", width=2)
    for x, y in punkte:
        d.ellipse([x - 4, y - 4, x + 4, y + 4],
                  fill="blue", outline="blue")

    # Titel + Achsenbeschriftungen
    d.text((breite // 2 - 100, 12), titel, fill="black")
    d.text((breite // 2 - 60, hoehe - 24),
           "Anzahl geflippter Module", fill="black")

    bild.save(dateiname)
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
    diagramm_speichern(
        daten, "fehler_demo_diagramm.png",
        f"GRETA in 12×12: Erfolgsquote bei zufälligen Modul-Flips",
        theoretische_grenze=rs_grenze_codewords + 1,
    )
    print("→ fehler_demo_diagramm.png")
# endregion
