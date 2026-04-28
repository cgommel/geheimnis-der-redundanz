# region distanz
def hamming_distanz(a, b):
    """Liefert die Hamming-Distanz zwischen zwei gleich langen Sequenzen."""
    if len(a) != len(b):
        raise ValueError("Wörter müssen gleich lang sein")
    distanz = 0
    for x, y in zip(a, b):
        if x != y:
            distanz += 1
    return distanz


# Tests:
print(hamming_distanz("KATZE", "KASSE"))      # 2
print(hamming_distanz([0, 0, 0], [1, 1, 1]))  # 3
print(hamming_distanz("1011010", "1001110"))  # 3
# endregion


# region mindestdistanz
import itertools


def mindestdistanz(codewoerter):
    minimum = float("inf")
    for a, b in itertools.combinations(codewoerter, 2):
        d = hamming_distanz(a, b)
        if d < minimum:
            minimum = d
    return minimum


# Test mit dem Paritätscode (3+1 Bit):
paritaet_code = [
    "0000", "0011", "0101", "0110",
    "1001", "1010", "1100", "1111",
]
print(mindestdistanz(paritaet_code))   # erwartet: 2

# Test mit dem Wiederholungscode (3,1):
wdh_code = ["000", "111"]
print(mindestdistanz(wdh_code))        # erwartet: 3
# endregion


# region korrektur
def naechstes_codewort(empfangen, codewoerter):
    """Findet das Codewort mit kleinster Distanz zum empfangenen Wort."""
    bestes = None
    beste_distanz = float("inf")
    for c in codewoerter:
        d = hamming_distanz(empfangen, c)
        if d < beste_distanz:
            beste_distanz = d
            bestes = c
    return bestes


# Wiederholungscode (3,1) auf 1-Bit-Fehlerkorrektur testen:
richtig = 0
gesamt = 0
for original in wdh_code:
    for pos in range(3):
        empfangen = list(original)
        empfangen[pos] = "1" if empfangen[pos] == "0" else "0"
        empfangen = "".join(empfangen)
        rekonstruiert = naechstes_codewort(empfangen, wdh_code)
        gesamt += 1
        if rekonstruiert == original:
            richtig += 1
print(f"{richtig}/{gesamt} Einzelfehler korrigiert")
# endregion


# region doppelfehler
richtig = 0
gesamt = 0
for original in wdh_code:
    for pos1, pos2 in itertools.combinations(range(3), 2):
        empfangen = list(original)
        for pos in (pos1, pos2):
            empfangen[pos] = "1" if empfangen[pos] == "0" else "0"
        empfangen = "".join(empfangen)
        rekonstruiert = naechstes_codewort(empfangen, wdh_code)
        gesamt += 1
        if rekonstruiert == original:
            richtig += 1
print(f"{richtig}/{gesamt} Doppelfehler korrigiert")
# endregion
