# Etappe 14, Stufe 1 ("roh"): alle Theorie-Bausteine zu einem
# kompletten Datamatrix-Encoder verbunden.
#
# Eingabe: ein 5-Buchstaben-Wort (z. B. "GRETA").
# Ausgabe: ein scanbares PNG.
#
# Diese Stufe hat bewusst keine eigenen Funktionen (außer dem
# Placement-Algorithmus aus Etappe 13, der zu lang wäre, um ihn
# hier nochmal aufzuschreiben). Alles fließt von oben nach unten,
# damit du den ganzen Datenfluss in einem Stück siehst.

import os
import sys

# place_codewords aus Etappe 13 nutzen (~150 Zeilen, hier nicht doppeln)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag13"))
from placement import place_codewords  # noqa: E402

from PIL import Image  # noqa: E402


# region eingabe
TEXT = "GRETA"
print(f"Klartext: {TEXT}")
# endregion


# region ascii
# --- Schritt 1: ASCII-Encoding (Etappe 11) ---
# Im ASCII-Modus wird jedes Zeichen zu (Zeichen-Wert + 1).
daten = [ord(ch) + 1 for ch in TEXT]
print(f"Schritt 1 — Datenbytes: {daten}")
# Für GRETA: G→72, R→83, E→70, T→85, A→66 → [72, 83, 70, 85, 66]
# endregion


# region ecc
# --- Schritt 2: Reed-Solomon-Prüfbytes (Etappe 12) ---
# 12×12-Symbol braucht 7 Prüfbytes. GF(2^8)-Multiplikation mit dem
# Datamatrix-Modulo-Polynom 0x12D, Generator-Polynom
# g(x) = (x − α^1)(x − α^2)…(x − α^7).

MOD_POLY = 0x12D  # x^8 + x^5 + x^3 + x^2 + 1


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


# Generator-Polynom für 7 Prüfbytes aufbauen.
g = [1]
alpha = 1
for i in range(7):
    alpha = gf_mul(alpha, 2)  # α^(i+1) = α^i · α   (α = 2)
    # Multipliziere g(x) mit (x − α^(i+1)). Im GF(2^8) ist
    # − α das gleiche wie + α, also XOR.
    neu = [0] * (len(g) + 1)
    for j, c in enumerate(g):
        neu[j] ^= gf_mul(c, alpha)
        neu[j + 1] ^= c
    g = neu

print(f"Generator g(x): {g}")

# Polynomdivision: ECC = (daten · x^7) mod g(x).
# Achtung: g hat den konstanten Term zuerst (g[0]), den führenden
# Koeffizienten (Grad 7, immer 1) zuletzt. Beim Aufaddieren wollen
# wir mit dem führenden Koeffizienten beginnen, also g[len(g)-1-j].
arbeitskopie = list(daten) + [0] * 7
for i in range(len(daten)):
    faktor = arbeitskopie[i]
    if faktor != 0:
        for j in range(len(g)):
            arbeitskopie[i + j] ^= gf_mul(g[len(g) - 1 - j], faktor)
ecc = arbeitskopie[len(daten):]  # die letzten 7 sind der Rest = ECC
print(f"Schritt 2 — ECC-Bytes: {ecc}")

codewords = daten + ecc
print(f"Alle 12 Codewords: {codewords}")
# endregion


# region matrix
# --- Schritt 3: Datenmodule platzieren (Etappe 13) ---
# place_codewords liefert eine 12×12-Matrix mit 0/1 für die Datenmodule
# und None für die Frame-Module (L-Pattern + Zeitsignal).
matrix = place_codewords(codewords, n=12)
print("Schritt 3 — Datenmodule gesetzt (Frame noch leer)")
# endregion


# region frame
# --- Schritt 4: Frame zeichnen (L-Pattern + Zeitsignal) ---
# L-Pattern: untere Kante (Zeile 11) und linke Kante (Spalte 0)
# vollständig schwarz.
# Zeitsignal: obere Kante alterniert (gerade Spalten schwarz),
# rechte Kante alterniert (ungerade Zeilen schwarz).
for c in range(12):
    matrix[11][c] = 1
for r in range(12):
    matrix[r][0] = 1
for c in range(12):
    matrix[0][c] = 1 if c % 2 == 0 else 0
for r in range(12):
    matrix[r][11] = 1 if r % 2 == 1 else 0
print("Schritt 4 — Frame ergänzt; Matrix komplett")
# endregion


# region render
# --- Schritt 5: PNG schreiben ---
# Erst die "rohe" 12×12-Pixel-Version (winzig), dann hochskaliert mit
# Quiet-Zone für Druck und Scan.

bild = Image.new("1", (12, 12), color=1)  # 1-Bit s/w, Default weiß
for r in range(12):
    for c in range(12):
        if matrix[r][c] == 1:
            bild.putpixel((c, r), 0)
bild.save("schritt_5_roh.png")
print("Schritt 5 — schritt_5_roh.png (12×12 Pixel)")

gross = bild.resize((300, 300), Image.NEAREST)
# Quiet-Zone: 30 Pixel weißer Rand drumrum (~ Modul-Breite × 1).
# Im Modus "L" (8-Bit-Graustufen) ist 0 = schwarz, 255 = weiß. Den
# Modus brauchen die meisten Scanner-Bibliotheken; reines 1-Bit-PNG
# wird oft abgelehnt.
mit_quietzone = Image.new("L", (360, 360), color=255)
mit_quietzone.paste(gross.convert("L"), (30, 30))
mit_quietzone.save(f"{TEXT.lower()}.png")
print(f"Schritt 5 — {TEXT.lower()}.png (360×360 mit Quiet-Zone)")
# endregion
