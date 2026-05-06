# Etappe 15, Stufe 2: der Datamatrix-Encoder als Klasse —
# eingebettet in eine kleine Klassenhierarchie für Barcodes überhaupt.
#
# Hierarchie:
#   Barcode (abstrakte Basisklasse)
#     ├── DatamatrixEncoder   (Etappe 15)
#     └── EAN13Encoder        (deine Aufgabe — siehe ean13_aufgabe.py)
#
# Die Basisklasse beschreibt das gemeinsame Verhalten (Text speichern,
# Matrix als PNG ausgeben, Wiederholungs-Repräsentation). Konkrete
# Codes liefern nur ihre eigene Bit-Matrix; das Drumherum kommt aus
# der Basisklasse — geschenkt durch Vererbung.

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag13"))
from placement import place_codewords  # noqa: E402

from PIL import Image  # noqa: E402


# region barcode
class Barcode:
    """Abstrakte Basisklasse für jeden Barcode-Typ.

    Ein Barcode hat einen Klartext und kann eine Bit-Matrix liefern
    (0 = weiß, 1 = schwarz). Die Matrix wird hier gemeinsam für alle
    Subklassen als PNG ausgegeben — egal ob Datamatrix, EAN-13 oder
    irgendwas anderes mit Strichen und Modulen.

    Diese Klasse selbst funktioniert nicht eigenständig — sie ist
    *abstrakt*. Erst eine Unterklasse wie DatamatrixEncoder macht sie
    benutzbar."""

    def __init__(self, text):
        self.text = text.upper()

    @property
    def name(self):
        return self.__class__.__name__

    def bitmap(self):
        """Liefert die Bit-Matrix (2D-Liste, Werte 0/1)."""
        # Eine sogenannte "abstrakte Methode": jede Subklasse muss
        # sie selbst implementieren. Wenn jemand sie auf der
        # Basisklasse aufruft, gibt's eine klare Fehlermeldung.
        raise NotImplementedError(
            f"{self.name} muss eine eigene bitmap()-Methode mitbringen"
        )

    def save(self, dateiname, modulgroesse=25, quietzone_module=1):
        """Schreibt die Bitmap als PNG. Quiet-Zone wird in Modulbreiten
        angegeben."""
        m = self.bitmap()
        h, w = len(m), len(m[0])
        rand = quietzone_module * modulgroesse
        bild = Image.new(
            "L",
            (w * modulgroesse + 2 * rand, h * modulgroesse + 2 * rand),
            color=255,
        )
        for r in range(h):
            for c in range(w):
                if m[r][c] == 1:
                    x0 = rand + c * modulgroesse
                    y0 = rand + r * modulgroesse
                    for dy in range(modulgroesse):
                        for dx in range(modulgroesse):
                            bild.putpixel((x0 + dx, y0 + dy), 0)
        bild.save(dateiname)
        return self
# endregion


# region datamatrix
class DatamatrixEncoder(Barcode):
    """Datamatrix-Encoder für quadratische ECC-200-Symbole von 10×10
    bis 26×26 (ohne Interleaving). Erbt von Barcode — den PNG-Export
    bekommen wir geschenkt."""

    SYMBOL_TABLE = {
        # Innenkante n → (Datencodewords, ECC-Codewords)
        10: (3, 5),
        12: (5, 7),
        14: (8, 10),
        16: (12, 12),
        18: (18, 14),
        20: (22, 18),
        22: (30, 20),
        24: (36, 24),
        26: (44, 28),
    }
    MOD_POLY = 0x12D
    PAD_BYTE = 129

    def __init__(self, text, n=None):
        super().__init__(text)  # Konstruktor der Elternklasse → setzt self.text
        self.daten = [ord(ch) + 1 for ch in self.text]
        self.n = n if n is not None else self._waehle_groesse()
        self._validiere()
        self.codewords = self._padden() + self._reed_solomon_ecc()

    # --- bitmap() ist die einzige Methode, die die Basisklasse einfordert ---
    def bitmap(self):
        return self._matrix_bauen()

    # --- Symbolgröße + Padding ---
    def _waehle_groesse(self):
        for n in sorted(self.SYMBOL_TABLE):
            if len(self.daten) <= self.SYMBOL_TABLE[n][0]:
                return n
        raise ValueError(
            f"Text mit {len(self.daten)} Zeichen passt in keine "
            f"unterstützte Symbolgröße"
        )

    def _validiere(self):
        if self.n not in self.SYMBOL_TABLE:
            raise ValueError(f"Symbolgröße {self.n}×{self.n} nicht unterstützt")
        max_daten, _ = self.SYMBOL_TABLE[self.n]
        if len(self.daten) > max_daten:
            raise ValueError(
                f"{len(self.daten)} Datenbytes passen nicht in {self.n}×{self.n}"
            )

    def _padden(self):
        max_daten, _ = self.SYMBOL_TABLE[self.n]
        ergebnis = list(self.daten)
        if len(ergebnis) < max_daten:
            ergebnis.append(self.PAD_BYTE)  # erstes Pad: fest 129
        while len(ergebnis) < max_daten:
            pos = len(ergebnis) + 1  # 1-basiert
            pseudo = ((149 * pos) % 253) + 1
            wert = self.PAD_BYTE + pseudo
            if wert > 254:
                wert -= 254
            ergebnis.append(wert)
        return ergebnis

    # --- Reed-Solomon-ECC (Etappe 12 in Klassen-Form) ---
    @classmethod
    def _gf_mul(cls, a, b):
        res = 0
        while b:
            if b & 1:
                res ^= a
            a <<= 1
            if a & 0x100:
                a ^= cls.MOD_POLY
            b >>= 1
        return res

    @classmethod
    def _generator_polynom(cls, anzahl_pruefbytes):
        g = [1]
        alpha = 1
        for _ in range(anzahl_pruefbytes):
            alpha = cls._gf_mul(alpha, 2)
            neu = [0] * (len(g) + 1)
            for j, c in enumerate(g):
                neu[j] ^= cls._gf_mul(c, alpha)
                neu[j + 1] ^= c
            g = neu
        return g

    def _reed_solomon_ecc(self):
        _, anzahl_pruefbytes = self.SYMBOL_TABLE[self.n]
        daten_padded = self._padden()
        g = self._generator_polynom(anzahl_pruefbytes)
        rest = list(daten_padded) + [0] * anzahl_pruefbytes
        for i in range(len(daten_padded)):
            faktor = rest[i]
            if faktor != 0:
                for j in range(len(g)):
                    rest[i + j] ^= self._gf_mul(g[len(g) - 1 - j], faktor)
        return rest[len(daten_padded):]

    # --- Matrix bauen (Datenmodule + Frame) ---
    def _matrix_bauen(self):
        matrix = place_codewords(self.codewords, n=self.n)
        n = self.n
        for c in range(n):
            matrix[n - 1][c] = 1
        for r in range(n):
            matrix[r][0] = 1
        for c in range(n):
            matrix[0][c] = 1 if c % 2 == 0 else 0
        for r in range(n):
            matrix[r][n - 1] = 1 if r % 2 == 1 else 0
        return matrix

    def __repr__(self):
        max_daten, ecc = self.SYMBOL_TABLE[self.n]
        return (
            f"DatamatrixEncoder(text={self.text!r}, "
            f"{self.n}×{self.n}, {max_daten}+{ecc} Codewords)"
        )
# endregion


# region demo
if __name__ == "__main__":
    for text in ["GRETA", "BLAUB", "BLAUBE", "BLAUBEERE", "PRAKTIKUMSWOCHE"]:
        e = DatamatrixEncoder(text)
        e.save(f"{text.lower()}.png")
        print(f"{e!r}  →  {text.lower()}.png")
# endregion
