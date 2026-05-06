# Etappe 16, Stufe 1: Datamatrix-Decoder mit Fehler-Lokalisation.
#
# Wir verwenden reedsolo (aus Etappe 8) für die eigentliche Decode-
# Rechnung — Berlekamp-Massey + Forney sind zu umfangreich, um sie
# nochmal von Hand zu schreiben. Spannend ist, dass reedsolo die
# Positionen der Fehler in der Codewort-Sequenz mitliefert. Damit
# können wir die kaputten Module im Symbol farbig markieren und
# Greta sieht: "Da war der Schaden — und der Decoder hat ihn
# trotzdem repariert."

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag13"))
from placement import _build_layout  # noqa: E402

import reedsolo  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402


# region klasse
class DatamatrixDecoder:
    """Pendant zu DatamatrixEncoder: nimmt eine Modul-Matrix oder ein
    PNG, liest die Codewords aus, decodiert mit Fehler-Korrektur und
    sagt, welche Module im Symbol kaputt waren."""

    SYMBOL_TABLE = {
        10: (3, 5),  12: (5, 7),  14: (8, 10),  16: (12, 12),
        18: (18, 14), 20: (22, 18), 22: (30, 20), 24: (36, 24), 26: (44, 28),
    }

    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(matrix)
        if self.n not in self.SYMBOL_TABLE:
            raise ValueError(f"Symbolgröße {self.n}×{self.n} nicht unterstützt")
        self.daten_anzahl, self.ecc_anzahl = self.SYMBOL_TABLE[self.n]
        self.codewords = self._matrix_zu_codewords()
        self.daten_bytes, self.errata = self._rs_decodieren()

    # --- Bild-Laden: Module aus PNG sampeln ---
    @classmethod
    def from_png(cls, pfad, n=12, modulgroesse=25, quietzone_module=1):
        bild = Image.open(pfad).convert("L")
        rand = quietzone_module * modulgroesse
        mid = modulgroesse // 2
        matrix = [[0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                x = rand + c * modulgroesse + mid
                y = rand + r * modulgroesse + mid
                matrix[r][c] = 1 if bild.getpixel((x, y)) < 128 else 0
        return cls(matrix)

    # --- Matrix → Codewords (Inverse von Etappe 13) ---
    def _matrix_zu_codewords(self):
        n_inner = self.n - 2
        layout = _build_layout(n_inner)
        slots = {}  # codeword_idx → Liste von (r_inner, c_inner, bit_nr)
        for r in range(n_inner):
            for c in range(n_inner):
                cell = layout[r][c]
                if cell is None:
                    continue
                cw_idx, bit_nr = cell
                slots.setdefault(cw_idx, []).append((r, c, bit_nr))

        anzahl = self.daten_anzahl + self.ecc_anzahl
        codewords = []
        for cw_idx in range(1, anzahl + 1):
            wert = 0
            for r_inner, c_inner, bit_nr in slots[cw_idx]:
                bit = self.matrix[r_inner + 1][c_inner + 1]
                wert |= bit << (8 - bit_nr)  # Bit 1 = MSB (128)
            codewords.append(wert)
        return codewords

    # --- Reed-Solomon-Decode mit reedsolo ---
    def _rs_decodieren(self):
        rs = reedsolo.RSCodec(
            nsym=self.ecc_anzahl, fcr=1, generator=2, prim=0x12D
        )
        try:
            daten, _, errata = rs.decode(bytes(self.codewords))
            return bytes(daten), list(errata)
        except reedsolo.ReedSolomonError:
            return None, []

    # --- Schöne Ausgabe-Properties ---
    @property
    def erfolgreich(self):
        return self.daten_bytes is not None

    @property
    def klartext(self):
        if not self.erfolgreich:
            return None
        text = ""
        for b in self.daten_bytes:
            if b == 129:  # Pad-Sentinel: Ende der echten Daten
                break
            if 2 <= b <= 128:
                text += chr(b - 1)
        return text

    @property
    def anzahl_fehler(self):
        return len(self.errata)

    def fehler_codewords(self):
        """1-basierte Codeword-Indizes, die der RS-Decoder als
        beschädigt erkannt hat."""
        return sorted(idx + 1 for idx in self.errata)

    def fehler_module(self):
        """Symbol-(zeile, spalte) jedes Moduls, das zu einem kaputten
        Codeword gehört."""
        n_inner = self.n - 2
        layout = _build_layout(n_inner)
        positionen = []
        kaputte = set(self.errata)
        for r in range(n_inner):
            for c in range(n_inner):
                cell = layout[r][c]
                if cell is None:
                    continue
                cw_idx, _ = cell
                if (cw_idx - 1) in kaputte:
                    positionen.append((r + 1, c + 1))
        return positionen
# endregion


# region visualisierung
def fehler_markieren(decoder, original_pfad, ausgabe_pfad,
                     modulgroesse=25, quietzone_module=1):
    """Lädt ein Datamatrix-PNG und überlagert die Module der vom
    Decoder gefundenen kaputten Codewords mit einer halbtransparenten
    roten Markierung. Speichert das Ergebnis als RGB-PNG."""
    grund = Image.open(original_pfad).convert("RGB")
    overlay = Image.new("RGBA", grund.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    rand = quietzone_module * modulgroesse
    for (r, c) in decoder.fehler_module():
        x0 = rand + c * modulgroesse
        y0 = rand + r * modulgroesse
        draw.rectangle(
            [x0, y0, x0 + modulgroesse - 1, y0 + modulgroesse - 1],
            fill=(255, 0, 0, 110),
            outline=(180, 0, 0, 255),
            width=2,
        )
    ergebnis = Image.alpha_composite(grund.convert("RGBA"), overlay)
    ergebnis.convert("RGB").save(ausgabe_pfad)
# endregion


# region demo
if __name__ == "__main__":
    # Wir laden ein Test-PNG, dass von DatamatrixEncoder (Etappe 15)
    # erzeugt wurde, und zeigen den Decoder im sauberen Fall.
    test_png = os.path.join(
        os.path.dirname(__file__), "..", "tag15", "greta.png"
    )
    d = DatamatrixDecoder.from_png(test_png, n=12)
    print(f"Klartext        : {d.klartext}")
    print(f"Fehler erkannt  : {d.anzahl_fehler}")
    print(f"Erfolgreich     : {d.erfolgreich}")
# endregion
