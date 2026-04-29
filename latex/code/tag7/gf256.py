# GF(2^8) — Erweiterung der GF8-Klasse aus Tag 5 auf 256 Elemente.
# Standard-Polynom für AES und Reed-Solomon im Datamatrix:
#   x^8 + x^4 + x^3 + x^2 + 1 = 0b100011101 = 0x11D

# region klasse
class GF256:
    """Element von GF(2^8), repräsentiert als Zahl 0..255.

    Bit 0 ist der Koeffizient der Konstanten, Bit 7 der Koeffizient
    von x^7. Multiplikation modulo p(x) = x^8 + x^4 + x^3 + x^2 + 1.
    """

    MOD = 0b100011101   # x^8 + x^4 + x^3 + x^2 + 1

    def __init__(self, wert):
        if not 0 <= wert <= 255:
            raise ValueError("GF256-Werte müssen zwischen 0 und 255 liegen")
        self.wert = wert

    def __add__(self, anderes):
        """Addition = XOR (wie in jedem GF(2^n))."""
        return GF256(self.wert ^ anderes.wert)

    def __sub__(self, anderes):
        """In GF(2^n) ist Subtraktion = Addition."""
        return self + anderes

    def __mul__(self, anderes):
        """Polynommultiplikation modulo MOD."""
        a, b = self.wert, anderes.wert
        ergebnis = 0
        # Schulmultiplikation: für jedes Bit von b
        for i in range(8):
            if (b >> i) & 1:
                ergebnis ^= a << i
        # Reduktion: höchstes Bit ist 14 (Bit 7 mal Bit 7 ergibt x^14)
        for i in range(14, 7, -1):
            if (ergebnis >> i) & 1:
                ergebnis ^= self.MOD << (i - 8)
        return GF256(ergebnis)

    def __pow__(self, n):
        """Potenzieren via wiederholtes Multiplizieren.
        Für ernsthafte Anwendungen würde man Square-and-Multiply nehmen,
        zum Verstehen reicht das hier."""
        ergebnis = GF256(1)
        basis = self
        for _ in range(n):
            ergebnis = ergebnis * basis
        return ergebnis

    def __eq__(self, anderes):
        if isinstance(anderes, int):
            return self.wert == anderes
        return self.wert == anderes.wert

    def __hash__(self):
        return hash(self.wert)

    def __repr__(self):
        return f"GF256({self.wert})"


# Test mit Datamatrix-Standardelementen
print(f"GF256(2) * GF256(3) = {GF256(2) * GF256(3)}")
# Multiplikation in GF(2^8) sollte in der Tafel von Tag 5
# nachvollziehbar sein, wenn man die Polynomschreibweise zur Hand hat.
# endregion


# region inverse
def gf256_inverse(a):
    """Multiplikatives Inverses in GF(2^8) via Satz von Fermat:
    a^254 = a^(-1), denn die multiplikative Gruppe hat Ordnung 255,
    also a^255 = 1 für jedes a != 0."""
    if a.wert == 0:
        raise ValueError("0 hat kein Inverses")
    return a ** 254


# Probe: jedes Element mal sein Inverses sollte 1 ergeben
for w in [1, 2, 23, 100, 200, 255]:
    a = GF256(w)
    inv = gf256_inverse(a)
    print(f"{a}^(-1) = {inv}, Probe: {a} * {inv} = {a * inv}")
# endregion


# region alpha
# Primitives Element: alpha = GF256(2). Wir prüfen, dass alle 255
# Potenzen alpha^0, ..., alpha^254 verschieden sind — dann erzeugt
# alpha die ganze multiplikative Gruppe.
alpha = GF256(2)
potenzen = set()
a = GF256(1)
for i in range(255):
    potenzen.add(a.wert)
    a = a * alpha
print(f"Anzahl verschiedener Potenzen von alpha: {len(potenzen)}")
# Erwartet: 255  →  alpha hat Ordnung 255, ist also primitiv.
# endregion
