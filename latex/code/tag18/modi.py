# Etappe 18: Kodierungs-Modi für Datamatrix
#
# Drei Modi im Überblick:
#   ASCII-Modus  (bisherig): 1 Zeichen → 1 Codeword  (Wert = ord(ch)+1)
#   Digit-Paar-Modus:        2 Ziffern  → 1 Codeword  (Wert 130–229)
#   C40-Modus:               3 Zeichen  → 2 Codewords (mit Latch 230 / Unlatch 254)

# region c40_tabelle
# Jedes C40-Zeichen hat einen Wert zwischen 0 und 39.
# Leerzeichen = 3, Ziffern 4–13, Großbuchstaben A–Z = 14–39.
C40_WERT = {" ": 3}
C40_WERT.update({str(d): 4 + d for d in range(10)})
C40_WERT.update({chr(ord("A") + i): 14 + i for i in range(26)})

LATCH_C40 = 230   # Codeword: "ab jetzt C40-Modus"
UNLATCH   = 254   # Codeword: "zurück zu ASCII"
# endregion


# region digit_paar
def kodiere_digit_paar(text):
    """Kodiert Text im Digit-Paar-Modus.

    Zwei aufeinanderfolgende Ziffern werden als EIN Codeword kodiert
    (Wert = 130 + erste_Ziffer × 10 + zweite_Ziffer).
    Alle anderen Zeichen landen wie gewohnt als ASCII+1 im Codeword.

    Beispiel: "12" → 130 + 1×10 + 2 = 142  (statt zwei Codewords 50 und 51)
    """
    codewords = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i].isdigit() and text[i + 1].isdigit():
            codewords.append(130 + int(text[i]) * 10 + int(text[i + 1]))
            i += 2
        else:
            codewords.append(ord(text[i]) + 1)
            i += 1
    return codewords
# endregion


# region c40
def kodiere_c40(zeichen):
    """Kodiert eine Liste von Zeichen im C40-Modus.

    Gibt eine vollständige Codeword-Sequenz zurück:
    Latch (230), Daten-Codewords, Unlatch (254).

    Drei Zeichen (V1, V2, V3) werden so zu zwei Codewords:
        tmp   = V1 × 1600 + V2 × 40 + V3 + 1
        CW[0] = tmp >> 8        (obere 8 Bit)
        CW[1] = tmp & 0xFF      (untere 8 Bit)

    Restzeichen (falls kein Vielfaches von 3) werden in ASCII angehängt.
    """
    volle = (len(zeichen) // 3) * 3   # Anzahl Zeichen für vollständige Triplets

    codewords = [LATCH_C40]
    for i in range(0, volle, 3):
        v1 = C40_WERT[zeichen[i]]
        v2 = C40_WERT[zeichen[i + 1]]
        v3 = C40_WERT[zeichen[i + 2]]
        tmp = v1 * 1600 + v2 * 40 + v3 + 1
        codewords.append(tmp >> 8)
        codewords.append(tmp & 0xFF)
    codewords.append(UNLATCH)

    # Restzeichen (0, 1 oder 2) in ASCII
    for ch in zeichen[volle:]:
        codewords.append(ord(ch) + 1)

    return codewords
# endregion


# region smart
def kodiere_smart(text):
    """Wählt pro Textsegment den effizientesten Kodierungs-Modus.

    Regeln (in dieser Priorität):
    1. Zwei aufeinanderfolgende Ziffern → Digit-Paar (1 CW statt 2)
    2. Mindestens 6 C40-Zeichen ohne Zifferpaare → C40-Modus
    3. Sonst: ASCII-Modus (ord(ch)+1)

    C40 lohnt sich erst ab ≈ 6 Zeichen im Segment, weil Latch und
    Unlatch je ein Codeword kosten.
    """
    codewords = []
    i = 0
    while i < len(text):
        # Priorität 1: Digit-Paar
        if i + 1 < len(text) and text[i].isdigit() and text[i + 1].isdigit():
            codewords.append(130 + int(text[i]) * 10 + int(text[i + 1]))
            i += 2
            continue

        # Priorität 2: C40-Lauf messen
        # Wir brechen ab, sobald wir auf ein Ziffernpaar stoßen —
        # das kodiert Digit-Paar effizienter als C40.
        j = i
        while j < len(text) and text[j] in C40_WERT:
            if text[j].isdigit() and j + 1 < len(text) and text[j + 1].isdigit():
                break
            j += 1
        c40_laenge = j - i
        if c40_laenge >= 6:
            codewords.extend(kodiere_c40(list(text[i:j])))
            i = j
            continue

        # Fallback: ASCII
        codewords.append(ord(text[i]) + 1)
        i += 1

    return codewords
# endregion


# region demo
if __name__ == "__main__":
    tests = [
        ("12345678",        "Ziffernfolge"),
        ("GRETA",           "5 Großbuchstaben"),
        ("PRAKTIKUMSWOCHE", "15 Großbuchstaben"),
        ("BESTELLNR12345678", "Buchstaben + Ziffern"),
    ]
    for text, beschreibung in tests:
        ascii_cw = [ord(ch) + 1 for ch in text]
        smart_cw = kodiere_smart(text)
        print(f"{beschreibung}: {text!r}")
        print(f"  ASCII  → {len(ascii_cw):2d} Codewords: {ascii_cw}")
        print(f"  Smart  → {len(smart_cw):2d} Codewords: {smart_cw}")
        print()
# endregion
