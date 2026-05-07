# Erzeugt Vergleichsbilder für das Buch:
#   ascii-*  →  Plain-ASCII-Encoder
#   smart-*  →  DatamatrixEncoderModi (Digit-Paar + C40)
#
# Aufruf: python3 demo_modi.py   (im Verzeichnis latex/code/tag18/)
# Ausgabe: Bilder werden in latex/abbildungen/tag18/ geschrieben.

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tag15"))
from encoder_klasse import DatamatrixEncoder  # noqa: E402

from encoder_modi import DatamatrixEncoderModi  # noqa: E402

ZIEL = os.path.join(os.path.dirname(__file__), "..", "..", "abbildungen", "tag18")
os.makedirs(ZIEL, exist_ok=True)


def speichere(encoder, name):
    pfad = os.path.join(ZIEL, name)
    encoder.save(pfad, modulgroesse=18)
    n = encoder.n
    daten_cw = len(encoder.daten)
    print(f"  {name}: {n}×{n}, {daten_cw} Daten-CW → {pfad}")


print("--- Ziffernfolge: '12345678' ---")
speichere(DatamatrixEncoder("12345678"),        "ziffern_ascii.png")
speichere(DatamatrixEncoderModi("12345678"),     "ziffern_smart.png")

print("--- Langer Text: 'PRAKTIKUMSWOCHE' ---")
speichere(DatamatrixEncoder("PRAKTIKUMSWOCHE"),     "text_ascii.png")
speichere(DatamatrixEncoderModi("PRAKTIKUMSWOCHE"),  "text_smart.png")

print("--- Gemischt: 'BESTELLNR12345678' ---")
speichere(DatamatrixEncoder("BESTELLNR12345678"),     "gemischt_ascii.png")
speichere(DatamatrixEncoderModi("BESTELLNR12345678"),  "gemischt_smart.png")
