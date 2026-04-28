# region interleave
def interleave(codewoerter):
    """Nimmt eine Liste von gleich langen Codewörtern und liefert
    die spaltenweise interleaved Bitfolge."""
    n = len(codewoerter[0])
    ergebnis = []
    for spalte in range(n):
        for codewort in codewoerter:
            ergebnis.append(codewort[spalte])
    return ergebnis


def deinterleave(bitfolge, anzahl_codewoerter):
    """Kehrt das Interleaving um."""
    n = len(bitfolge) // anzahl_codewoerter
    codewoerter = [[] for _ in range(anzahl_codewoerter)]
    idx = 0
    for spalte in range(n):
        for i in range(anzahl_codewoerter):
            codewoerter[i].append(bitfolge[idx])
            idx += 1
    return codewoerter


# Test:
codes = [[1, 0, 1, 0], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 1, 1]]
print("Codes:", codes)
verschachtelt = interleave(codes)
print("Interleaved:", verschachtelt)
zurueck = deinterleave(verschachtelt, 4)
print("Deinterleaved:", zurueck)
print("Identisch?", zurueck == codes)
# endregion
