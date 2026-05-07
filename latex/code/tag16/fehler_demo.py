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

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

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
def diagramm_als_pdf(daten, dateiname, theoretische_grenze=None):
    """daten: Liste von (anzahl_fehler, erfolgsquote)-Paaren.
    theoretische_grenze: x-Wert, an dem der RS-Decoder garantiert
    versagt (= Anzahl_ECC // 2 + 1).

    Speichert das Diagramm als PDF (Vektorgrafik, druckfertig)."""
    xs = [p[0] for p in daten]
    ys = [p[1] * 100 for p in daten]

    fig, ax = plt.subplots(figsize=(6, 3.2))
    ax.plot(xs, ys, "b-o", linewidth=2, markersize=5)

    if theoretische_grenze is not None:
        ax.axvline(x=theoretische_grenze, color="red", linewidth=1.5,
                   label="RS-Grenze")
        ax.text(theoretische_grenze + 0.1, 5, "RS-Grenze",
                color="red", fontsize=8, va="bottom")

    ax.set_xlabel("Anzahl geflippter Module")
    ax.set_ylabel("Erfolgsquote (%)")
    ax.set_ylim(-5, 105)
    ax.set_yticks([0, 25, 50, 75, 100])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v)} %"))
    ax.grid(axis="y", color="lightgray", linewidth=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    fig.savefig(dateiname, format="pdf", bbox_inches="tight")
    plt.close(fig)
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
    diagramm_als_pdf(
        daten, "fehler_demo_diagramm.pdf",
        theoretische_grenze=rs_grenze_codewords + 1,
    )
    print("→ fehler_demo_diagramm.pdf (als \\includegraphics ins Buch eingebunden)")
# endregion
