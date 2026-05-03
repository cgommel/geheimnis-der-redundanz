# Reed-Solomon-Encoder für Datamatrix.
#
# Identisch zur Logik aus Tag 7 — nur dass die GF(2^8)-Klasse jetzt
# das Datamatrix-Modulo-Polynom verwendet. Der Algorithmus selbst
# ist 1:1 derselbe.

from gf256_dm import GF256DM, ALPHA


# region generator
def generator_polynom(anzahl_pruefsymbole):
    """Generator-Polynom g(x) = (x - α^1)·(x - α^2)·...·(x - α^t).

    Rückgabe: Koeffizienten als Liste von GF256DM, vom höchsten zum
    niedrigsten Grad. Beispiel für t=2: g(x) = x^2 + (α+α^2)·x + α·α^2,
    also drei Koeffizienten."""
    g = [GF256DM(1)]                                    # g(x) = 1
    for i in range(1, anzahl_pruefsymbole + 1):
        wurzel = ALPHA ** i                             # α^i
        # multipliziere g(x) mit (x - wurzel) = (x + wurzel) in GF(2):
        neu = [GF256DM(0)] * (len(g) + 1)
        for j, koeff in enumerate(g):
            neu[j]     = neu[j]     + koeff * wurzel    # konstanter Anteil
            neu[j + 1] = neu[j + 1] + koeff             # x-Anteil
        g = neu
    return g
# endregion


# region encoder
def reed_solomon_ecc(daten_bytes, anzahl_pruefsymbole):
    """Berechne die Reed-Solomon-Prüfbytes für eine Datenfolge.

    Der Algorithmus ist die klassische Polynomdivision modulo g(x):
      1. Hänge `anzahl_pruefsymbole` Nullen an die Daten an.
      2. Teile durch g(x) — wie schriftliche Division, nur mit
         GF(2^8)-Arithmetik (XOR statt Subtraktion).
      3. Der Rest ist die Prüfbyte-Folge."""
    g = generator_polynom(anzahl_pruefsymbole)
    grad_g = len(g) - 1                                 # Polynom-Grad

    # Daten in GF256DM verpacken; mit Nullen auffüllen.
    rest = [GF256DM(b) for b in daten_bytes] \
         + [GF256DM(0)] * anzahl_pruefsymbole

    # Polynomdivision: pro Daten-Koeffizient einen Schritt.
    # generator_polynom liefert g mit konstantem Term zuerst, daher
    # nehmen wir g[grad_g - j] beim Aufaddieren (höchster Grad zuerst).
    for i in range(len(daten_bytes)):
        leitkoeff = rest[i]
        if leitkoeff.wert == 0:
            continue                                    # nichts zu tun
        for j in range(grad_g + 1):
            rest[i + j] = rest[i + j] + leitkoeff * g[grad_g - j]

    # Die letzten `anzahl_pruefsymbole` Koeffizienten sind der Rest.
    return [b.wert for b in rest[-anzahl_pruefsymbole:]]
# endregion


# region demo
if __name__ == "__main__":
    # HONIG aus Etappe 11 — fünf Datenbytes für ein 12x12-Symbol.
    # Datamatrix 12x12: 5 Daten + 7 ECC = 12 Codewords.
    daten = [73, 80, 79, 74, 72]
    ecc = reed_solomon_ecc(daten, 7)
    print("Daten:", daten)
    print("ECC :", ecc)
    print("Komplettes Codewort:", daten + ecc)
    # Erwartete Ausgabe:
    #   Daten: [73, 80, 79, 74, 72]
    #   ECC : [70, 186, 97, 167, 44, 40, 243]
# endregion
