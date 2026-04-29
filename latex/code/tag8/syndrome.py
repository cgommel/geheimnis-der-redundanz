# Reed-Solomon-Decoder — Schritt 1: Syndrom-Berechnung.
# Voraussetzung: gf256.py und rs_encoder.py aus Tag 7 im selben Ordner.

from gf256 import GF256
from rs_encoder import rs_encode


# region funktion
def berechne_syndrome(empfangen, anzahl_pruefsymbole):
    """Berechnet die Syndrome S_1, S_2, ..., S_t mit
    S_i = r(alpha^i), wobei r das empfangene Polynom ist.

    Bei einem fehlerfreien Codewort sind alle Syndrome 0 (denn das
    Codewort ist durch das Generatorpolynom teilbar — und dessen
    Wurzeln sind genau alpha^1 ... alpha^t).
    """
    alpha = GF256(2)
    syndrome = []
    for i in range(1, anzahl_pruefsymbole + 1):
        x = alpha ** i
        # Horner-Schema, höchster Koeffizient zuerst
        s = GF256(0)
        for koeff in reversed(empfangen):
            s = s * x + koeff
        syndrome.append(s)
    return syndrome
# endregion


# region test
# Test mit dem Codewort aus Tag 7
daten = [GF256(c) for c in b"GRETA"]
codewort = rs_encode(daten, 4)
print("Codewort:", [c.wert for c in codewort])

# Fehlerfrei: alle Syndrome 0
syn = berechne_syndrome(codewort, 4)
print("Syndrome (fehlerfrei):", [s.wert for s in syn])

# Mit einem Fehler: Symbol an Position 2 verfälschen
gestoert = list(codewort)
gestoert[2] = GF256(gestoert[2].wert ^ 0xFF)
print("\nGestört an Position 2:", [c.wert for c in gestoert])

syn_gestoert = berechne_syndrome(gestoert, 4)
print("Syndrome (gestört):    ", [s.wert for s in syn_gestoert])
# Die Syndrome bilden eine geometrische Folge in alpha^j (Position des
# Fehlers) mit Vorfaktor e (Fehlerwert) — aus zwei Syndromen lässt
# sich ein einzelner Fehler eindeutig rekonstruieren.
# endregion
