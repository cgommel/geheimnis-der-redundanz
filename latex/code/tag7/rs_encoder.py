# Reed-Solomon-Encoder mit Generator-Polynom-Sicht.
# Voraussetzung: gf256.py liegt im selben Ordner.

from gf256 import GF256

# region generator
def generator_polynom(anzahl_pruefsymbole):
    """Erzeugt das Generator-Polynom
    g(x) = (x - alpha^1)(x - alpha^2) ... (x - alpha^t)
    für t Prüfsymbole, mit alpha = GF256(2) als primitivem Element.
    (Datamatrix-Konvention: Wurzeln starten bei alpha^1, nicht alpha^0.)
    Rückgabe: Liste der Koeffizienten, niedrigster Grad zuerst.
    In GF gilt minus = plus, also (x - a) wird zu (x + a)."""
    alpha = GF256(2)
    g = [GF256(1)]   # konstantes Polynom 1

    for i in range(1, anzahl_pruefsymbole + 1):
        wurzel = alpha ** i
        # Multipliziere g(x) mit (x + wurzel):
        # neuer Koeffizient bei x^k = alter Koeff. bei x^(k-1) (für k > 0)
        # plus alter Koeff. bei x^k mal wurzel.
        neu = [GF256(0)] * (len(g) + 1)
        for j, koeff in enumerate(g):
            neu[j] = neu[j] + koeff * wurzel   # konstanter Anteil
            neu[j + 1] = neu[j + 1] + koeff    # x-Anteil
        g = neu
    return g


# Beispiel: 4 Prüfsymbole für RS(255, 251) — korrigiert 2 Fehler
g = generator_polynom(4)
print("Generatorpolynom für RS(255, 251):")
for i, koeff in enumerate(g):
    print(f"  x^{i}: {koeff}")
# endregion


# region encoder
def rs_encode(daten, anzahl_pruefsymbole):
    """Systematischer Reed-Solomon-Encoder.

    daten:                Liste von GF256-Elementen (Datensymbole).
    anzahl_pruefsymbole:  wie viele Prüfsymbole hinten dran.

    Codewort-Form: [d_0, d_1, ..., d_(k-1), p_0, p_1, ..., p_(t-1)]
    mit d_i = Datensymbole, p_j = Prüfsymbole.
    Die Codewort-Polynom ist durch das Generator-Polynom teilbar —
    genau wie beim CRC, nur mit GF(256)-Arithmetik in den Koeffizienten."""
    g = generator_polynom(anzahl_pruefsymbole)

    # Daten plus angehängte Nullen
    arbeit = list(daten) + [GF256(0)] * anzahl_pruefsymbole

    # Polynomdivision modulo g(x) mit XOR-artigem Verfahren.
    grad_g = len(g) - 1
    for i in range(len(daten)):
        koeff = arbeit[i]
        if koeff != GF256(0):
            for j in range(grad_g + 1):
                # g[grad_g - j] ist der Koeffizient von x^(grad_g - j),
                # passt zur aktuellen Position i+j.
                arbeit[i + j] = arbeit[i + j] + koeff * g[grad_g - j]

    # Letzte t Symbole sind die Prüfsymbole
    return list(daten) + arbeit[-anzahl_pruefsymbole:]


# Test mit einer kurzen Nachricht
daten = [GF256(c) for c in b"GRETA"]
codewort = rs_encode(daten, 4)
print("\nCodewort:", [c.wert for c in codewort])
print("Daten:    ", [c.wert for c in codewort[:-4]])
print("Prüfsymbole:", [c.wert for c in codewort[-4:]])
# endregion


# region check
def ist_durch_g_teilbar(codewort, anzahl_pruefsymbole):
    """Verifikation: ein gültiges Codewort hat an alpha^1, alpha^2, ...,
    alpha^t jeweils den Wert 0 (denn die Wurzeln des Generator-
    Polynoms sind genau diese Stellen — Datamatrix-Konvention)."""
    alpha = GF256(2)
    for i in range(1, anzahl_pruefsymbole + 1):
        # Wert des Codepolynoms an Stelle alpha^i (Horner-Schema)
        x = alpha ** i
        wert = GF256(0)
        for koeff in reversed(codewort):
            wert = wert * x + koeff
        if wert != GF256(0):
            return False, i, wert
    return True, None, None


ok, idx, wert = ist_durch_g_teilbar(codewort, 4)
print(f"\nCodewort ist gültig: {ok}")
# endregion
