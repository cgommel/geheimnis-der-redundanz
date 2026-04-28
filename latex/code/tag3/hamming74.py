# region encoder
def hamming74_encode(daten):
    """Codiert 4 Datenbits in 7 Bits Hamming-Code.
    daten ist eine Liste [d1, d2, d3, d4].
    Rückgabe: Liste [bit1, bit2, ..., bit7]."""
    d1, d2, d3, d4 = daten

    # Prüfbits berechnen (gerade Parität in jeder Gruppe)
    p1 = (d1 + d2 + d4) % 2   # überwacht Positionen 3, 5, 7 (= d1, d2, d4)
    p2 = (d1 + d3 + d4) % 2   # überwacht Positionen 3, 6, 7 (= d1, d3, d4)
    p3 = (d2 + d3 + d4) % 2   # überwacht Positionen 5, 6, 7 (= d2, d3, d4)

    # In die richtige Reihenfolge einsetzen:
    # Position:  1   2   3   4   5   6   7
    return [p1, p2, d1, p3, d2, d3, d4]


# Test mit Datenwort 1011
print(hamming74_encode([1, 0, 1, 1]))
# Erwartet: [0, 1, 1, 0, 0, 1, 1]   (das ist der Wert aus Bleistiftübung 2)
# endregion


# region decoder
def hamming74_decode(empfangen):
    """Dekodiert 7 Bits Hamming-Code, korrigiert ggf. einen Einzelfehler.
    empfangen ist eine Liste [bit1, ..., bit7].
    Rückgabe: (daten, fehlerposition)
      daten = Liste der 4 Datenbits
      fehlerposition = 0 (kein Fehler) oder 1..7 (Position des Fehlers)"""
    b = empfangen.copy()

    # Prüfsummen berechnen
    s1 = (b[0] + b[2] + b[4] + b[6]) % 2   # Positionen 1, 3, 5, 7
    s2 = (b[1] + b[2] + b[5] + b[6]) % 2   # Positionen 2, 3, 6, 7
    s3 = (b[3] + b[4] + b[5] + b[6]) % 2   # Positionen 4, 5, 6, 7

    # s3 s2 s1 binär lesen → Fehlerposition (1..7) oder 0
    fehlerposition = s3 * 4 + s2 * 2 + s1

    # Fehler korrigieren falls nötig
    if fehlerposition != 0:
        b[fehlerposition - 1] = 1 - b[fehlerposition - 1]

    # Datenbits an den Positionen 3, 5, 6, 7 extrahieren
    daten = [b[2], b[4], b[5], b[6]]
    return daten, fehlerposition


# Test ohne Fehler:
codewort = hamming74_encode([1, 0, 1, 1])
print(hamming74_decode(codewort))
# Erwartet: ([1, 0, 1, 1], 0)

# Test mit Fehler an Position 5:
gestoert = codewort.copy()
gestoert[4] = 1 - gestoert[4]   # Bit 5 (Index 4) kippen
print(hamming74_decode(gestoert))
# Erwartet: ([1, 0, 1, 1], 5)
# endregion


# region test-einzel
import itertools


def teste_alle_einzelfehler():
    """Testet alle 16 Datenwörter und alle 7 möglichen Einzelfehler."""
    erfolg = 0
    gesamt = 0
    for daten in itertools.product([0, 1], repeat=4):
        daten = list(daten)
        codewort = hamming74_encode(daten)
        for fehlerpos in range(7):
            gestoert = codewort.copy()
            gestoert[fehlerpos] = 1 - gestoert[fehlerpos]
            rekonstruiert, erkannte_pos = hamming74_decode(gestoert)
            gesamt += 1
            if rekonstruiert == daten:
                erfolg += 1
            else:
                print(f"FEHLER bei daten={daten}, fehlerpos={fehlerpos+1}: "
                      f"rekonstruiert {rekonstruiert}, erkannt {erkannte_pos}")
    print(f"{erfolg}/{gesamt} Einzelfehler korrekt korrigiert")


teste_alle_einzelfehler()
# Erwartet: 112/112 (16 Datenwörter × 7 Fehlerpositionen)
# endregion


# region test-doppel
def teste_alle_doppelfehler():
    erfolg = 0
    falsch = 0
    gesamt = 0
    for daten in itertools.product([0, 1], repeat=4):
        daten = list(daten)
        codewort = hamming74_encode(daten)
        for pos1, pos2 in itertools.combinations(range(7), 2):
            gestoert = codewort.copy()
            gestoert[pos1] = 1 - gestoert[pos1]
            gestoert[pos2] = 1 - gestoert[pos2]
            rekonstruiert, _ = hamming74_decode(gestoert)
            gesamt += 1
            if rekonstruiert == daten:
                erfolg += 1
            else:
                falsch += 1
    print(f"Doppelfehler: {erfolg}/{gesamt} zufällig richtig, "
          f"{falsch}/{gesamt} falsch")


teste_alle_doppelfehler()
# endregion
