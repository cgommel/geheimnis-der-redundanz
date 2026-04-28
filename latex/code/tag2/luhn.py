# region validator
def luhn_pruefen(nummer):
    """Prüft, ob 'nummer' (String aus Ziffern) Luhn-gültig ist."""
    summe = 0
    # Wir gehen von rechts nach links
    for i, c in enumerate(reversed(nummer)):
        d = int(c)
        if i % 2 == 1:
            # Jede zweite Ziffer von rechts (beginnend bei Index 1) verdoppeln
            d = d * 2
            if d >= 10:
                d = d - 9   # Trick: bei zweistelligem Ergebnis ist Quersumme = d - 9
        summe += d
    return summe % 10 == 0


# Tests:
print(luhn_pruefen("4539148803436467"))   # True
print(luhn_pruefen("4539148803436468"))   # False (letzte Ziffer falsch)
# endregion


# region zifferndreher
def teste_zifferndreher_luhn(nummer):
    nicht_erkannt = []
    zeichen = list(nummer)
    for i in range(len(zeichen) - 1):
        if zeichen[i] == zeichen[i + 1]:
            continue
        getauscht = zeichen.copy()
        getauscht[i], getauscht[i + 1] = getauscht[i + 1], getauscht[i]
        if luhn_pruefen("".join(getauscht)):
            nicht_erkannt.append((i, "".join(getauscht)))
    return nicht_erkannt


print(teste_zifferndreher_luhn("4539148803436467"))
# endregion
