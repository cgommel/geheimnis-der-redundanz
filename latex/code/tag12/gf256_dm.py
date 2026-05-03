# GF(2^8) für Datamatrix.
#
# Genau wie die GF8-Klasse aus Tag 5 (und die GF256 aus Tag 7), aber
# mit dem Modulo-Polynom, das der Datamatrix-Standard vorschreibt:
#
#   x^8 + x^5 + x^3 + x^2 + 1   (= 0b1_0010_1101 = 0x12D = 301)
#
# Tag 7 hatte das übliche Reed-Solomon-Polynom 0x11D verwendet
# (x^8 + x^4 + x^3 + x^2 + 1). Datamatrix hat sich für ein anderes
# entschieden — beide sind irreduzibel über GF(2), beide ergeben
# einen Körper mit 256 Elementen, beide funktionieren. Es ist
# Konvention.

# region klasse
class GF256DM:
    """Element von GF(2^8) im Datamatrix-Standard."""

    MOD_POLY = 0x12D     # x^8 + x^5 + x^3 + x^2 + 1

    def __init__(self, wert):
        self.wert = wert & 0xFF       # auf 8 Bit beschränken

    def __add__(self, andere):
        return GF256DM(self.wert ^ andere.wert)   # XOR

    def __sub__(self, andere):
        return GF256DM(self.wert ^ andere.wert)   # XOR — Addition = Subtraktion

    def __mul__(self, andere):
        a, b = self.wert, andere.wert
        ergebnis = 0
        while b > 0:
            if b & 1:                  # niedrigstes Bit von b gesetzt?
                ergebnis ^= a
            b >>= 1
            a <<= 1
            if a & 0x100:              # über 8 Bit hinaus → Modulo
                a ^= self.MOD_POLY
        return GF256DM(ergebnis)

    def __pow__(self, n):
        ergebnis = GF256DM(1)
        basis = self
        while n > 0:
            if n & 1:
                ergebnis = ergebnis * basis
            basis = basis * basis
            n >>= 1
        return ergebnis

    def __eq__(self, andere):
        return self.wert == andere.wert

    def __repr__(self):
        return f"GF256DM({self.wert})"
# endregion


# region alpha
# Primitives Element der Datamatrix-GF(2^8): wieder α = 2.
# Das heißt α^0 = 1, α^1 = 2, α^2 = 4, ..., α^7 = 128, α^8 muss
# durch das Modulo reduziert werden.
ALPHA = GF256DM(2)


def alpha_potenzen():
    """Tabelle der ersten 256 α-Potenzen — schöne Probe, dass α
    wirklich primitiv ist (alle 255 Nicht-Null-Elemente kommen vor)."""
    pot = GF256DM(1)
    werte = []
    for i in range(256):
        werte.append(pot.wert)
        pot = pot * ALPHA
    return werte


if __name__ == "__main__":
    werte = alpha_potenzen()
    # α^0 muss 1 sein, α^255 muss wieder 1 sein (Periodizität),
    # alle 255 ersten Werte unterschiedlich
    print("alpha^0 =", werte[0])
    print("alpha^255 =", werte[255])
    print("alle Nicht-Nullen verschieden:",
          len(set(werte[:255])) == 255)
# endregion
