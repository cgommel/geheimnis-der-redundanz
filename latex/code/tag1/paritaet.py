# region pruefer
def paritaetsbit(daten):
    """Liefert 0 oder 1, so dass die Gesamtanzahl der Einsen gerade ist."""
    return sum(daten) % 2


def ist_gueltig(wort):
    """Prüft, ob ein Wort gerade Parität hat."""
    return sum(wort) % 2 == 0


# Test:
daten = [1, 0, 1, 1, 0, 1, 0]
p = paritaetsbit(daten)
gesendet = daten + [p]
print("Gesendet:", gesendet, "  gültig?", ist_gueltig(gesendet))

# Jetzt einen Fehler einbauen:
empfangen = gesendet.copy()
empfangen[3] = 1 - empfangen[3]   # Bit an Position 3 kippen
print("Empfangen:", empfangen, "  gültig?", ist_gueltig(empfangen))
# endregion


# region kippe-bit
def kippe_bit(wort, position):
    neu = wort.copy()
    neu[position] = 1 - neu[position]
    return neu
# endregion


# region test-einzel
import itertools


richtig = 0
gesamt = 0
for daten in itertools.product([0, 1], repeat=7):
    daten = list(daten)
    p = paritaetsbit(daten)
    gesendet = daten + [p]
    for pos in range(8):
        empfangen = kippe_bit(gesendet, pos)
        gesamt += 1
        if not ist_gueltig(empfangen):
            richtig += 1
print(f"{richtig}/{gesamt} Einzelfehler erkannt")
# endregion


# region test-doppel
richtig, gesamt = 0, 0
for daten in itertools.product([0, 1], repeat=7):
    daten = list(daten)
    gesendet = daten + [paritaetsbit(daten)]
    for p1, p2 in itertools.combinations(range(8), 2):
        empfangen = kippe_bit(kippe_bit(gesendet, p1), p2)
        gesamt += 1
        if not ist_gueltig(empfangen):
            richtig += 1
print(f"{richtig}/{gesamt} Doppelfehler erkannt")
# endregion
