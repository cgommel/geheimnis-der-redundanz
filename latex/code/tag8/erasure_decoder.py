# Reed-Solomon-Auslöschungs-Decoder.
# Korrigiert bis zu t Auslöschungen (Fehler an bekannten Positionen).
# Voraussetzung: gf256.py, rs_encoder.py, syndrome.py im selben Ordner.

from gf256 import GF256, gf256_inverse
from rs_encoder import rs_encode
from syndrome import berechne_syndrome


# region funktion
def auslosung_korrigieren(empfangen, auslosch_positionen, anzahl_pruefsymbole):
    """Korrigiert Auslöschungen an bekannten Positionen.

    empfangen:           Codewort als Liste von GF256-Elementen,
                         mit 0 an den Auslösch-Positionen.
    auslosch_positionen: Liste der Indizes, an denen Symbole ausgelöscht
                         (verloren) sind.
    anzahl_pruefsymbole: t (so wie beim Encoder).

    Rückgabe: korrigiertes Codewort.

    Verfahren: jedes Syndrom S_i ist eine Linearkombination der
    Fehlerwerte e_j mit Koeffizienten alpha^(i*j). Wenn wir die
    Positionen j kennen (Auslöschungen!), bleibt ein lineares
    Gleichungssystem in den Unbekannten e_j — eine Vandermonde-Matrix.
    Das lösen wir mit Gauß-Elimination in GF(2^8).
    """
    alpha = GF256(2)
    v = len(auslosch_positionen)
    if v > anzahl_pruefsymbole:
        raise ValueError(
            f"Zu viele Auslöschungen ({v}) für {anzahl_pruefsymbole} Prüfsymbole"
        )

    syn = berechne_syndrome(empfangen, anzahl_pruefsymbole)

    # Vandermonde-Matrix A: A[i][k] = alpha^((i+1) * j_k)
    # Wir nehmen die ersten v Syndrome — dann ist A genau v x v.
    A = []
    for i in range(1, v + 1):
        zeile = [alpha ** (i * j) for j in auslosch_positionen]
        A.append(zeile)

    rhs = list(syn[:v])

    # Gauß-Elimination, in-place
    for col in range(v):
        # Pivot suchen
        pivot = col
        for row in range(col, v):
            if A[row][col] != GF256(0):
                pivot = row
                break
        A[col], A[pivot] = A[pivot], A[col]
        rhs[col], rhs[pivot] = rhs[pivot], rhs[col]

        # Pivot-Zeile auf 1 normieren
        inv = gf256_inverse(A[col][col])
        for k in range(col, v):
            A[col][k] = A[col][k] * inv
        rhs[col] = rhs[col] * inv

        # andere Zeilen eliminieren
        for row in range(v):
            if row != col and A[row][col] != GF256(0):
                faktor = A[row][col]
                for k in range(col, v):
                    A[row][k] = A[row][k] + faktor * A[col][k]
                rhs[row] = rhs[row] + faktor * rhs[col]

    # rhs enthält jetzt die Fehlerwerte e_j; korrigiere damit empfangen
    korrigiert = list(empfangen)
    for k, j in enumerate(auslosch_positionen):
        korrigiert[j] = empfangen[j] + rhs[k]
    return korrigiert
# endregion


# region test
# Test: zwei Auslöschungen in einem RS(255-Buchstabe-codewort)
daten = [GF256(c) for c in b"GRETA"]
codewort = rs_encode(daten, 4)

# Auslöschungen an Position 2 und 6 simulieren
auslosch = [2, 6]
empfangen = list(codewort)
verlorene_werte = [empfangen[j].wert for j in auslosch]
for j in auslosch:
    empfangen[j] = GF256(0)
print(f"Empfangen: {[c.wert for c in empfangen]}")
print(f"           (mit Auslöschungen an Position {auslosch})")

korrigiert = auslosung_korrigieren(empfangen, auslosch, 4)
print(f"Korrigiert: {[c.wert for c in korrigiert]}")
print(f"Original:   {[c.wert for c in codewort]}")

# Plausibilitätsprüfung
ok = all(k.wert == c.wert for k, c in zip(korrigiert, codewort))
print(f"Korrektur erfolgreich: {ok}")
# endregion
