# Polynome mit Koeffizienten in GF(2^3).
# Vorausgesetzt: gf8.py aus Tag 5 liegt im selben Ordner.

# region klasse
from gf8 import GF8


class Polynom:
    """Polynom über GF(2^3). Koeffizienten sind GF8-Elemente.
    Index 0 ist die Konstante, Index 1 der Koeffizient von x, usw."""

    def __init__(self, koeffizienten):
        koeff = list(koeffizienten)
        # führende Nullen abschneiden, außer beim Null-Polynom
        while len(koeff) > 1 and koeff[-1] == GF8(0):
            koeff.pop()
        self.koeff = koeff

    def grad(self):
        if len(self.koeff) == 1 and self.koeff[0] == GF8(0):
            return -1
        return len(self.koeff) - 1

    def __add__(self, anderes):
        # Polynome werden koeffizientenweise addiert.
        # In GF(2^n) ist Addition gleich XOR.
        n = max(len(self.koeff), len(anderes.koeff))
        ergebnis = []
        for i in range(n):
            a = self.koeff[i] if i < len(self.koeff) else GF8(0)
            b = anderes.koeff[i] if i < len(anderes.koeff) else GF8(0)
            ergebnis.append(a + b)
        return Polynom(ergebnis)

    def __mul__(self, anderes):
        # Polynommultiplikation: jeder Koeffizient mit jedem Koeffizienten,
        # die Ergebnisse an der passenden Position aufsummiert.
        ergebnis = [GF8(0)] * (len(self.koeff) + len(anderes.koeff) - 1)
        for i, a in enumerate(self.koeff):
            for j, b in enumerate(anderes.koeff):
                ergebnis[i + j] = ergebnis[i + j] + a * b
        return Polynom(ergebnis)

    def __repr__(self):
        return "Polynom([" + ", ".join(repr(k) for k in self.koeff) + "])"
# endregion


# region auswerten
    def auswerten(self, x):
        """Wertet das Polynom an der Stelle x aus (Horner-Schema)."""
        ergebnis = GF8(0)
        for koeff in reversed(self.koeff):
            ergebnis = ergebnis * x + koeff
        return ergebnis


# Beispiel: f(x) = 3 + 5x + 2x^2
f = Polynom([GF8(3), GF8(5), GF8(2)])
print(f"f(0) = {f.auswerten(GF8(0))}")   # → GF8(011) = 3
print(f"f(1) = {f.auswerten(GF8(1))}")   # → 3 + 5 + 2 = (XOR) GF8(100) = 4
print(f"f(2) = {f.auswerten(GF8(2))}")   # → in GF(2^3) ausrechnen
# endregion


# region rs-encode
def rs_encode(daten, stuetzstellen):
    """Reed-Solomon-Encoder durch Auswertung.

    daten:           Liste von k Datensymbolen (GF8-Elemente),
                     interpretiert als Koeffizienten eines Polynoms vom Grad < k.
    stuetzstellen:   Liste von n verschiedenen GF8-Elementen.
    Rückgabe:        Liste von n Codesymbolen (Polynom an jeder Stützstelle).
    """
    f = Polynom(daten)
    return [f.auswerten(x) for x in stuetzstellen]


# Beispiel: k=3 Datensymbole, n=5 Stützstellen → RS(5, 3) über GF(2^3)
daten = [GF8(3), GF8(5), GF8(2)]
stuetzstellen = [GF8(1), GF8(2), GF8(3), GF8(4), GF8(5)]
codewort = rs_encode(daten, stuetzstellen)
print("Codewort:", codewort)
# endregion
