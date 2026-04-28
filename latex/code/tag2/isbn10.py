# region validator
def isbn10_pruefziffer(neun_ziffern):
    """Berechnet die ISBN-10-Prüfziffer für eine Liste von 9 Ziffern.
    Liefert eine Zahl zwischen 0 und 10 (10 bedeutet 'X')."""
    summe = 0
    for i, d in enumerate(neun_ziffern):
        gewicht = 10 - i
        summe += d * gewicht
    return (11 - summe % 11) % 11


def isbn10_ist_gueltig(isbn):
    """isbn ist ein String mit 10 Zeichen. Letztes Zeichen darf 'X' sein."""
    ziffern = []
    for c in isbn[:9]:
        ziffern.append(int(c))
    erwartet = isbn10_pruefziffer(ziffern)
    letztes = isbn[9]
    if letztes == "X":
        return erwartet == 10
    else:
        return erwartet == int(letztes)


# Tests:
print(isbn10_ist_gueltig("0306406152"))   # True
print(isbn10_ist_gueltig("344643500X"))   # True (Prüfziffer ist X!)
print(isbn10_ist_gueltig("0306406153"))   # False
# endregion


# region zifferndreher
def teste_alle_zifferndreher_isbn10(isbn):
    nicht_erkannt = []
    zeichen = list(isbn)
    for i in range(10):
        for j in range(i + 1, 10):
            # Pragmatisch: nur tauschen, wenn beide Ziffern sind
            if zeichen[i] == "X" or zeichen[j] == "X":
                continue
            if zeichen[i] == zeichen[j]:
                continue
            getauscht = zeichen.copy()
            getauscht[i], getauscht[j] = getauscht[j], getauscht[i]
            if isbn10_ist_gueltig("".join(getauscht)):
                nicht_erkannt.append((i, j, "".join(getauscht)))
    return nicht_erkannt


print(teste_alle_zifferndreher_isbn10("0306406152"))
# → []  (keine unentdeckten Vertauschungen!)
# endregion
