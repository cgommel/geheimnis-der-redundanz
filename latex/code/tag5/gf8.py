# region klasse
class GF8:
    """Element von GF(2^3), repräsentiert als 3-Bit-Zahl 0..7.

    Polynom-Bits: bit 0 = 1-Term, bit 1 = x-Term, bit 2 = x^2-Term.
    Modulo-Polynom: x^3 + x + 1, also als Zahl: 0b1011 = 11.
    """

    MOD = 0b1011   # x^3 + x + 1

    def __init__(self, wert):
        if not 0 <= wert <= 7:
            raise ValueError("GF8-Werte müssen zwischen 0 und 7 liegen")
        self.wert = wert

    def __add__(self, anderes):
        """Addition = XOR."""
        return GF8(self.wert ^ anderes.wert)

    def __sub__(self, anderes):
        """In GF(2^n) ist Subtraktion = Addition."""
        return self + anderes

    def __mul__(self, anderes):
        """Polynom-Multiplikation modulo x^3 + x + 1."""
        a, b = self.wert, anderes.wert
        ergebnis = 0
        # Schulmultiplikation: für jedes Bit von b
        for i in range(3):
            if (b >> i) & 1:
                ergebnis ^= a << i
        # Reduktion: solange Grad >= 3, mit MOD reduzieren
        # höchstes Bit ist 5 (Bit 2 von a · Bit 2 von b)
        for i in range(5, 2, -1):
            if (ergebnis >> i) & 1:
                ergebnis ^= self.MOD << (i - 3)
        return GF8(ergebnis)

    def __eq__(self, anderes):
        return self.wert == anderes.wert

    def __repr__(self):
        return f"GF8({self.wert:03b})"


# Tests
a = GF8(0b011)   # x+1
b = GF8(0b110)   # x^2+x
print(a + b)     # erwartet: 0b101 = x^2+1
print(a * b)     # erwartet: rechne von Hand und vergleiche!
# endregion


# region inverse
def gf8_inverse(a):
    """Findet das multiplikative Inverse von a in GF(2^3) durch Probieren."""
    if a.wert == 0:
        raise ValueError("0 hat kein Inverses")
    eins = GF8(1)
    for kandidat in range(1, 8):
        if a * GF8(kandidat) == eins:
            return GF8(kandidat)
    raise RuntimeError("Kein Inverses gefunden – sollte nicht passieren!")


# Teste alle Elemente
for w in range(1, 8):
    a = GF8(w)
    inv = gf8_inverse(a)
    print(f"{a}^(-1) = {inv}, Probe: {a} · {inv} = {a * inv}")
# endregion
