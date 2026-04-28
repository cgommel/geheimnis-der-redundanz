# region berechnung
def crc_berechnen(daten_bits, generator_bits):
    """Berechnet das CRC für eine Liste von Datenbits.
    daten_bits:     Liste der Daten (z.B. [1,0,1,1,0])
    generator_bits: Liste der Generator-Bits (z.B. [1,0,1,1] für G(x) = x^3+x+1)
    Rückgabe: Liste der CRC-Bits (Länge = len(generator_bits) - 1)"""
    grad = len(generator_bits) - 1
    # Daten plus Nullen anhängen
    arbeit = list(daten_bits) + [0] * grad

    # Polynomdivision modulo 2
    for i in range(len(daten_bits)):
        if arbeit[i] == 1:   # nur teilen, wenn führendes Bit 1 ist
            for j in range(len(generator_bits)):
                arbeit[i + j] ^= generator_bits[j]   # XOR

    # Die letzten 'grad' Bits sind der Rest = CRC
    return arbeit[len(daten_bits):]


def crc_pruefen(empfangen_bits, generator_bits):
    """Prüft, ob die empfangene Folge (Daten + CRC) durch G teilbar ist.
    Rückgabe: True wenn CRC stimmt, False sonst."""
    grad = len(generator_bits) - 1
    daten = empfangen_bits[:-grad]
    erwartet = crc_berechnen(daten, generator_bits)
    return erwartet == empfangen_bits[-grad:]


# Test:
generator = [1, 0, 1, 1]   # G(x) = x^3 + x + 1
daten = [1, 0, 1, 1, 0]
crc = crc_berechnen(daten, generator)
print("CRC:", crc)

gesendet = daten + crc
print("Gesendet:", gesendet)
print("Empfangen ok?", crc_pruefen(gesendet, generator))

# Mit Fehler:
gestoert = gesendet.copy()
gestoert[2] = 1 - gestoert[2]
print("Empfangen ok (mit Fehler)?", crc_pruefen(gestoert, generator))
# endregion


# region brute-force
import itertools


def teste_alle_fehler(gesendet, generator):
    n = len(gesendet)
    erkannt = 0
    nicht_erkannt = 0
    nicht_erkannte_muster = []
    # Alle möglichen Fehler-Muster (außer dem Null-Muster, das ist ja kein Fehler)
    for fehler_muster in itertools.product([0, 1], repeat=n):
        if all(b == 0 for b in fehler_muster):
            continue   # Null-Muster überspringen
        # Fehler einbauen
        gestoert = [g ^ f for g, f in zip(gesendet, fehler_muster)]
        if crc_pruefen(gestoert, generator):
            nicht_erkannt += 1
            nicht_erkannte_muster.append(fehler_muster)
        else:
            erkannt += 1
    return erkannt, nicht_erkannt, nicht_erkannte_muster


erkannt, nicht_erkannt, muster = teste_alle_fehler(gesendet, generator)
print(f"{erkannt} erkannt, {nicht_erkannt} nicht erkannt")
print(f"Nicht erkannte Muster (Anzahl): {len(muster)}")
# endregion
