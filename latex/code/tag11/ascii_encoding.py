# Datamatrix-Encoding, Stufe 1: ASCII-Modus.
#
# Datamatrix kennt mehrere Encoding-Modi (ASCII, C40, Text, Base 256,
# X12, EDIFACT). Wir bauen den einfachsten: ASCII. Damit lässt sich
# jedes druckbare ASCII-Zeichen kodieren — perfekt für unsere
# Test-Wörter "HONIG", "GRETA" usw.
#
# Regel ASCII-Modus:
#   Buchstabe X (ASCII-Wert n)  →  Codewort-Byte (n + 1)
#   Ziffer 0..9                 →  Sonderform: Doppelziffern werden
#                                  in einem einzigen Byte verpackt
#                                  (130..229), Einzelziffer wie
#                                  Buchstabe.
#   Pad-Byte (für Padding)      →  129
#
# Wir implementieren nur den Buchstaben-Fall, weil wir mit reinen
# Wörtern arbeiten.

# region offset
def buchstabe_zu_byte(ch):
    """ASCII-Modus: Codewort-Byte für ein druckbares Zeichen."""
    return ord(ch) + 1


# Probe:
print("'H' →", buchstabe_zu_byte("H"))   # 72 + 1 = 73
print("'O' →", buchstabe_zu_byte("O"))   # 79 + 1 = 80
print("'N' →", buchstabe_zu_byte("N"))   # 78 + 1 = 79
print("'I' →", buchstabe_zu_byte("I"))   # 73 + 1 = 74
print("'G' →", buchstabe_zu_byte("G"))   # 71 + 1 = 72
# endregion


# region wort
def wort_zu_bytes(text):
    """Eine Liste von Codewort-Bytes für ein Wort aus Buchstaben."""
    return [buchstabe_zu_byte(ch) for ch in text]


print("HONIG →", wort_zu_bytes("HONIG"))
# → [73, 80, 79, 74, 72]
# endregion


# region padding
PAD = 129       # Datamatrix-Pad-Byte

def auf_kapazitaet_padden(daten, kapazitaet):
    """Hänge Pad-Bytes an, bis die Datenkapazität erreicht ist."""
    if len(daten) > kapazitaet:
        raise ValueError(f"Daten zu lang ({len(daten)} > {kapazitaet})")
    return daten + [PAD] * (kapazitaet - len(daten))


# Symbol 12×12 hat 5 Datenbytes Kapazität (plus 7 ECC, total 12 Codewords).
# (Achtung: für unser Wort "HONIG" mit 5 Buchstaben wäre 12×12 zu klein —
# das passt erst in 14×14. Wir wählen weiter unten ein Symbol, das
# zu unserem Text passt.)
print("HONIG, 5 Bytes, padden auf 5:",
      auf_kapazitaet_padden(wort_zu_bytes("HONIG"), 5))
# endregion
