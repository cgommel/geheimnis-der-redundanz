# region validator
def ean13_pruefziffer(zwoelf_ziffern):
    """Berechnet die EAN-13-Prüfziffer für eine Liste von 12 Ziffern."""
    summe = 0
    for i, d in enumerate(zwoelf_ziffern):
        gewicht = 1 if i % 2 == 0 else 3
        summe += d * gewicht
    return (10 - summe % 10) % 10


def ean13_ist_gueltig(ean):
    """ean ist ein String mit 13 Ziffern."""
    ziffern = [int(c) for c in ean]
    erwartet = ean13_pruefziffer(ziffern[:12])
    return erwartet == ziffern[12]


# Tests:
print(ean13_ist_gueltig("4006381333931"))   # True
print(ean13_ist_gueltig("4006381333932"))   # False (letzte Ziffer falsch)
# endregion


# region zifferndreher
def teste_alle_zifferndreher(ean):
    nicht_erkannt = []
    ziffern = list(ean)
    for i in range(12):
        if ziffern[i] == ziffern[i + 1]:
            continue   # gleiche Ziffern → kein echter Dreher
        getauscht = ziffern.copy()
        getauscht[i], getauscht[i + 1] = getauscht[i + 1], getauscht[i]
        kandidat = "".join(getauscht)
        if ean13_ist_gueltig(kandidat):
            nicht_erkannt.append((i, kandidat))
    return nicht_erkannt


print(teste_alle_zifferndreher("4006381333931"))
# endregion


# region einzelfehler
def teste_einzelfehler(ean):
    erkannt = 0
    gesamt = 0
    ziffern = list(ean)
    for pos in range(13):
        original = ziffern[pos]
        for neu in "0123456789":
            if neu == original:
                continue
            kandidat = ziffern.copy()
            kandidat[pos] = neu
            gesamt += 1
            if not ean13_ist_gueltig("".join(kandidat)):
                erkannt += 1
    return erkannt, gesamt


print(teste_einzelfehler("4006381333931"))
# → (117, 117)  – alle 117 Einzelfehler werden erkannt.
# endregion
