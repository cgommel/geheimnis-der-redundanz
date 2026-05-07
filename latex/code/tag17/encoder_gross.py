# Etappe 17, Stufe 2: DatamatrixEncoderGross — Subklasse mit Interleaving.
#
# DatamatrixEncoder (Etappe 15) unterstützt Symbole bis 26×26 mit
# genau einem RS-Block. DatamatrixEncoderGross erweitert die Klasse:
# - SYMBOL_TABLE enthält auch 32×32 bis 64×64
# - Für Symbole mit k>1 RS-Blöcken wird die Codeword-Sequenz
#   interleaved (mit den Funktionen aus interleaving.py)
# - Das Rendering großer Symbole übernimmt pylibdmtx — die
#   Multi-Bereich-Platzierung ist komplexer als unsere tag13-Funktion

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag15"))
from encoder_klasse import DatamatrixEncoder  # noqa: E402

sys.path.insert(0, os.path.dirname(__file__))
from interleaving import (  # noqa: E402
    SYMBOL_TABLE as _SYMBOL_TABLE_VOLL,
    teile_in_bloecke,
    reed_solomon_pro_block,
    verschachtle_bloecke,
)


# region klasse
class DatamatrixEncoderGross(DatamatrixEncoder):
    """Datamatrix-Encoder für Symbole von 10×10 bis 64×64.

    Erbt von DatamatrixEncoder (Etappe 15). Für Symbole mit einem
    RS-Block (bis 32×32) wird alles von der Elternklasse erledigt.
    Für Symbole ab 36×36 (k=2 RS-Blöcke) überschreibt diese Klasse
    die Codeword-Erzeugung: Daten werden aufgeteilt, jeder Block
    bekommt eigene ECC, dann werden alle Blöcke verschachtelt.

    Das Rendering großer Symbole (≥ 36×36) delegiert save_png()
    an pylibdmtx, weil die Datenplatzierung in Multi-Bereich-Symbolen
    aus vielen Regeln besteht, die wir nicht selbst implementieren."""

    # Überschreibe SYMBOL_TABLE mit erweiterter Version
    # (Format wie Elternklasse: n → (data_cw, ecc_cw))
    SYMBOL_TABLE = {n: (d, e) for n, (d, e, _) in _SYMBOL_TABLE_VOLL.items()}

    # Block-Anzahl pro Größe
    _RS_BLOECKE = {n: k for n, (_, _, k) in _SYMBOL_TABLE_VOLL.items()}

    def __init__(self, text, n=None):
        # Barcode.__init__ aufrufen (setzt self.text = text.upper())
        super(DatamatrixEncoder, self).__init__(text)
        self.daten = [ord(ch) + 1 for ch in self.text]
        self.n = n if n is not None else self._waehle_groesse()
        self._validiere()

        k = self._RS_BLOECKE[self.n]
        d, e = self.SYMBOL_TABLE[self.n]
        gepaddet = self._padden()

        if k == 1:
            # Kleines Symbol: ECC aus Elternklasse, direkt verwendbar
            self.codewords = gepaddet + self._reed_solomon_ecc()
        else:
            # Großes Symbol: Interleaving
            ecc_pro_block = e // k
            daten_bloecke = teile_in_bloecke(gepaddet, k)
            bloecke_mit_ecc = reed_solomon_pro_block(daten_bloecke, ecc_pro_block)
            self.codewords = verschachtle_bloecke(bloecke_mit_ecc)

    def rs_bloecke(self):
        """Anzahl der RS-Blöcke für dieses Symbol."""
        return self._RS_BLOECKE[self.n]

    def bitmap(self):
        """Bit-Matrix — nur für kleine Symbole (1 RS-Block)."""
        if self.rs_bloecke() == 1:
            return super().bitmap()
        raise NotImplementedError(
            f"{self.n}×{self.n} hat {self.rs_bloecke()} RS-Blöcke — "
            "bitte save_png() verwenden"
        )

    def save_png(self, dateiname, modulgroesse=None, quietzone_module=None):
        """Speichert das Symbol als PNG — funktioniert für alle Größen.

        Kleine Symbole (1 Block): eigener Renderer aus Etappe 15.
        Große Symbole (k>1 Blöcke): pylibdmtx übernimmt Rendering
        und Platzierung."""
        if self.rs_bloecke() == 1:
            kw = {}
            if modulgroesse is not None:
                kw["modulgroesse"] = modulgroesse
            if quietzone_module is not None:
                kw["quietzone_module"] = quietzone_module
            self.save(dateiname, **kw)
            return
        # Großes Symbol: pylibdmtx.encode()
        from pylibdmtx.pylibdmtx import encode as dmtx_encode
        from PIL import Image
        result = dmtx_encode(
            self.text.encode("ascii"),
            size=f"{self.n}x{self.n}",
        )
        img = Image.frombytes("RGB", (result.width, result.height), result.pixels)
        img.save(dateiname)

    def __repr__(self):
        d, e = self.SYMBOL_TABLE[self.n]
        k = self.rs_bloecke()
        return (
            f"DatamatrixEncoderGross(text={self.text!r}, "
            f"{self.n}×{self.n}, {d}+{e} CW, {k} RS-Block{'e' if k>1 else ''})"
        )
# endregion


# region demo
if __name__ == "__main__":
    from pylibdmtx.pylibdmtx import decode as dmtx_decode
    from PIL import Image

    # Kleines Symbol (1 Block): wie in Etappe 15
    e_klein = DatamatrixEncoderGross("GRETA")
    e_klein.save_png("greta_klein.png")
    img = Image.open("greta_klein.png")
    scan = dmtx_decode(img)
    print(f"{e_klein!r}")
    print(f"  Scan: {scan[0].data.decode() if scan else 'KEIN SCAN'}")

    # Großes Symbol (2 Blöcke): 36×36 mit einem langen Text
    langer_text = "INTERLEAVING VERTEILT SCHAEDEN AUF MEHRERE RS-BLOECKE"
    e_gross = DatamatrixEncoderGross(langer_text, n=36)
    e_gross.save_png("interleaving_36x36.png")
    img = Image.open("interleaving_36x36.png")
    scan = dmtx_decode(img)
    print(f"\n{e_gross!r}")
    print(f"  Scan: {scan[0].data.decode() if scan else 'KEIN SCAN'}")
    print(f"  Codewords (erste 10): {e_gross.codewords[:10]}")
# endregion
