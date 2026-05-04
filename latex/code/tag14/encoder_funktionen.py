# Etappe 14, Stufe 2 ("mit Funktionen"): derselbe Encoder wie
# encoder_roh.py, aber jeder Schritt ist als eigene Funktion gekapselt.
#
# Vorteil gegenüber Stufe roh:
#   - jede Funktion lässt sich einzeln in Thonny aufrufen und prüfen
#   - mehrere Wörter in einer Schleife encoden ist trivial
#   - Modulgröße und Quiet-Zone werden konfigurierbar
#   - perfekte Vorbereitung für die Klasse in Etappe 15

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag13"))
from placement import place_codewords  # noqa: E402

from PIL import Image  # noqa: E402


# region ascii
# --- Schritt 1: ASCII-Encoding ---
def encode_ascii(text):
    """Verwandle einen reinen ASCII-Text in Datamatrix-Datenbytes
    (ASCII-Modus, Codewert + 1)."""
    return [ord(ch) + 1 for ch in text]
# endregion


# region rs
# --- Schritt 2: Reed-Solomon-Prüfbytes ---
MOD_POLY = 0x12D  # x^8 + x^5 + x^3 + x^2 + 1 (Datamatrix-Wahl)


def gf_mul(a, b):
    """GF(2^8)-Multiplikation modulo MOD_POLY."""
    res = 0
    while b:
        if b & 1:
            res ^= a
        a <<= 1
        if a & 0x100:
            a ^= MOD_POLY
        b >>= 1
    return res


def generator_polynom(anzahl_pruefbytes):
    """g(x) = (x − α^1)(x − α^2)…(x − α^t), als Liste mit konstantem
    Term zuerst und führendem Koeffizienten (= 1) zuletzt."""
    g = [1]
    alpha = 1
    for _ in range(anzahl_pruefbytes):
        alpha = gf_mul(alpha, 2)  # α = 2 in GF(2^8) mit MOD_POLY
        neu = [0] * (len(g) + 1)
        for j, c in enumerate(g):
            neu[j] ^= gf_mul(c, alpha)
            neu[j + 1] ^= c
        g = neu
    return g


def reed_solomon_ecc(daten, anzahl_pruefbytes):
    """Polynomdivision: ECC = (daten · x^t) mod g(x)."""
    g = generator_polynom(anzahl_pruefbytes)
    rest = list(daten) + [0] * anzahl_pruefbytes
    for i in range(len(daten)):
        faktor = rest[i]
        if faktor != 0:
            for j in range(len(g)):
                rest[i + j] ^= gf_mul(g[len(g) - 1 - j], faktor)
    return rest[len(daten):]
# endregion


# region matrix
# --- Schritte 3 + 4: Datenmodule + Frame ---
def baue_matrix(codewords, n=12):
    """Liefert die fertige n×n-Matrix mit Datenmodulen UND Frame
    (L-Pattern + Zeitsignal). Werte sind 0 (weiß) oder 1 (schwarz)."""
    matrix = place_codewords(codewords, n=n)

    # L-Pattern: untere Kante + linke Kante
    for c in range(n):
        matrix[n - 1][c] = 1
    for r in range(n):
        matrix[r][0] = 1
    # Zeitsignal: obere Kante (gerade Spalten), rechte Kante (ungerade Zeilen)
    for c in range(n):
        matrix[0][c] = 1 if c % 2 == 0 else 0
    for r in range(n):
        matrix[r][n - 1] = 1 if r % 2 == 1 else 0

    return matrix
# endregion


# region render
# --- Schritt 5: PNG-Render ---
def matrix_zu_png(matrix, dateiname, modulgroesse=25, quietzone_module=1):
    """Schreibt die Matrix als PNG. modulgroesse ist die Pixelbreite
    eines einzelnen Datamatrix-Moduls; quietzone_module ist der weiße
    Rand drumrum, gemessen in Modul-Breiten."""
    n = len(matrix)
    inner = n * modulgroesse
    rand = quietzone_module * modulgroesse
    gesamt = inner + 2 * rand

    bild = Image.new("L", (gesamt, gesamt), color=255)  # weiß
    for r in range(n):
        for c in range(n):
            if matrix[r][c] == 1:
                x0 = rand + c * modulgroesse
                y0 = rand + r * modulgroesse
                for dy in range(modulgroesse):
                    for dx in range(modulgroesse):
                        bild.putpixel((x0 + dx, y0 + dy), 0)
    bild.save(dateiname)
# endregion


# region pipeline
# --- Alles in einem Aufruf ---
def datamatrix_encoden(text, dateiname, modulgroesse=25):
    """Eingabe: ASCII-Text (5 Buchstaben für 12×12). Ausgabe: PNG-Datei."""
    daten = encode_ascii(text)
    ecc = reed_solomon_ecc(daten, 7)
    codewords = daten + ecc
    matrix = baue_matrix(codewords, n=12)
    matrix_zu_png(matrix, dateiname, modulgroesse=modulgroesse)
    return codewords
# endregion


# region demo
if __name__ == "__main__":
    # Mehrere Wörter in einer Schleife — das war in Stufe roh nicht
    # so leicht möglich, weil dort alles auf Top-Level steht.
    for wort in ["GRETA", "HONIG", "BIENE"]:
        cws = datamatrix_encoden(wort, f"{wort.lower()}.png")
        print(f"{wort}: {cws}")
        print(f"  → {wort.lower()}.png")
    # Andere Wortlängen (z. B. 4 oder 6 Buchstaben) gehen mit diesem
    # Skript noch nicht — dafür braucht es Padding und ggf. eine
    # größere Symbolgröße. Beides kommt in Etappe 15.
# endregion
