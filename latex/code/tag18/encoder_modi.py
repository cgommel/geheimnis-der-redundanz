# Etappe 18, Stufe 3: DatamatrixEncoderModi — nutzt automatisch den
# effizientesten Kodierungs-Modus pro Textsegment.
#
# Hierarchie (erweitert):
#   Barcode (abstrakte Basisklasse)
#     └── DatamatrixEncoder   (Etappe 15, ASCII-Modus)
#           └── DatamatrixEncoderModi   (Etappe 18, Smart-Modus)

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag15"))
from encoder_klasse import DatamatrixEncoder, Barcode  # noqa: E402

from modi import kodiere_smart  # noqa: E402


# region encoder_modi
class DatamatrixEncoderModi(DatamatrixEncoder):
    """Datamatrix-Encoder mit automatischer Moduswahl.

    Statt jedes Zeichen einzeln als ASCII+1 zu kodieren, ruft dieser
    Encoder kodiere_smart() auf: Zifferpaare landen als ein Digit-Paar-
    Codeword, lange Buchstaben-Segmente im platzsparenden C40-Modus.

    Der Encoder erbt bitmap(), save() und die RS-Berechnung vollständig
    von DatamatrixEncoder — nur die Codeword-Liste in self.daten ändert
    sich."""

    def __init__(self, text, n=None):
        # Direkt Barcode.__init__ aufrufen (wie in DatamatrixEncoderGross),
        # damit self.text gesetzt wird — aber self.daten noch NICHT.
        super(DatamatrixEncoder, self).__init__(text)
        # Jetzt smart kodieren statt einfaches ASCII+1
        self.daten = kodiere_smart(self.text)
        self.n = n if n is not None else self._waehle_groesse()
        self._validiere()
        self.codewords = self._padden() + self._reed_solomon_ecc()

    def __repr__(self):
        max_daten, ecc = self.SYMBOL_TABLE[self.n]
        return (
            f"DatamatrixEncoderModi(text={self.text!r}, "
            f"{self.n}×{self.n}, {max_daten}+{ecc} CW, "
            f"{len(self.daten)} Daten-CW nach Smart-Kodierung)"
        )
# endregion


# region demo
if __name__ == "__main__":
    vergleiche = [
        ("12345678",           "Ziffernfolge"),
        ("PRAKTIKUMSWOCHE",    "langer Text"),
        ("BESTELLNR12345678",  "gemischter Text"),
    ]

    for text, beschreibung in vergleiche:
        ascii_enc = DatamatrixEncoder(text)
        smart_enc = DatamatrixEncoderModi(text)
        print(f"--- {beschreibung}: {text!r} ---")
        print(f"  ASCII: {ascii_enc.n}×{ascii_enc.n}  ({len(ascii_enc.daten)} Daten-CW)")
        print(f"  Smart: {smart_enc.n}×{smart_enc.n}  ({len(smart_enc.daten)} Daten-CW)")
        ascii_enc.save(f"{text.lower()}_ascii.png")
        smart_enc.save(f"{text.lower()}_smart.png")
        print(f"  → {text.lower()}_ascii.png  und  {text.lower()}_smart.png gespeichert")
        print()
# endregion
