# Etappe 17, Stufe 1: Interleaving für große Datamatrix-Symbole.
#
# Kleine Symbole (bis 32×32) haben einen einzigen RS-Block — alle
# Codewords werden zusammen kodiert und korrigiert. Große Symbole
# (ab 36×36) haben mehrere RS-Blöcke: die Daten werden aufgeteilt,
# jeder Block bekommt seine eigene ECC, und am Ende werden alle
# Blöcke verschachtelt (interleaved) in die Matrix geschrieben.
#
# Das Ergebnis: ein Kratzer zerstört aus jedem Block nur wenige
# Codewords — und jeder Block kann sich separat erholen.

import reedsolo


# region tabelle
# Erweiterter Symbol-Table: äußere Größe → (Daten-CW, ECC-CW, RS-Blöcke).
# Werte für 10×10 bis 26×26 wie in Etappe 15; größere Symbole nach
# ISO/IEC 16022:2006. Jede Symbolgröße ab 36×36 hat 2×2 Datenbereiche
# und damit 2 unabhängige RS-Blöcke.
SYMBOL_TABLE = {
    10: (3,   5,  1),  12: (5,   7,  1),  14: (8,  10,  1),
    16: (12,  12, 1),  18: (18,  14, 1),  20: (22, 18,  1),
    22: (30,  20, 1),  24: (36,  24, 1),  26: (44, 28,  1),
    32: (62,  50, 1),  # noch 1 Datenbereich, größerer Innenraum
    36: (86,  42, 2),  # ab hier: 2×2 Datenbereiche → 2 RS-Blöcke
    40: (114, 46, 2),
    44: (144, 56, 2),
    48: (174, 66, 2),
    52: (204, 84, 2),
    64: (280, 168, 2),
}
# endregion


# region bloecke
def teile_in_bloecke(codewords, k):
    """Verteilt eine Liste von Codewords möglichst gleichmäßig auf k Blöcke.

    Ist len(codewords) nicht durch k teilbar, bekommen die ersten
    (len % k) Blöcke je ein Codeword mehr. Beispiel: 9 CW, k=2 →
    [5, 4]."""
    n = len(codewords)
    basis = n // k
    rest = n % k
    bloecke, pos = [], 0
    for i in range(k):
        groesse = basis + (1 if i < rest else 0)
        bloecke.append(list(codewords[pos: pos + groesse]))
        pos += groesse
    return bloecke


def reed_solomon_pro_block(daten_bloecke, ecc_pro_block):
    """Berechnet für jeden Datenblock separat die RS-Prüfbytes.

    Gibt eine Liste von (daten, ecc)-Paaren zurück — jeder Block
    als eigenes Paar."""
    rs = reedsolo.RSCodec(nsym=ecc_pro_block, fcr=1, generator=2, prim=0x12D)
    ergebnis = []
    for block in daten_bloecke:
        codiert = rs.encode(bytes(block))
        ecc = list(codiert[len(block):])
        ergebnis.append((block, ecc))
    return ergebnis


def verschachtle_bloecke(bloecke_mit_ecc):
    """Verschachtelt Daten- und ECC-Codewords aller Blöcke.

    Zuerst werden die Daten-CWs round-robin gemischt (D_B1[0],
    D_B2[0], ..., D_B1[1], D_B2[1], ...), danach die ECC-CWs
    (E_B1[0], E_B2[0], ...). Das Ergebnis ist die Codeword-Sequenz,
    die in die Matrix geschrieben wird."""
    daten = [list(d) for d, _ in bloecke_mit_ecc]
    eccs  = [list(e) for _, e in bloecke_mit_ecc]

    def round_robin(bloecke):
        max_len = max(len(b) for b in bloecke)
        out = []
        for i in range(max_len):
            for b in bloecke:
                if i < len(b):
                    out.append(b[i])
        return out

    return round_robin(daten) + round_robin(eccs)
# endregion


# region demo
if __name__ == "__main__":
    # Kleines Beispiel: 9 Datenbytes, k=2 Blöcke, je 4 ECC-Bytes
    daten = list(range(65, 74))     # A B C D E F G H I
    print(f"Daten           : {daten}  ({[chr(b) for b in daten]})")

    bloecke = teile_in_bloecke(daten, k=2)
    print(f"Block 1         : {bloecke[0]}")
    print(f"Block 2         : {bloecke[1]}")

    bloecke_mit_ecc = reed_solomon_pro_block(bloecke, ecc_pro_block=4)
    for i, (d, e) in enumerate(bloecke_mit_ecc, 1):
        print(f"Block {i} (d+ecc)  : {d} + {e}")

    sequenz = verschachtle_bloecke(bloecke_mit_ecc)
    print(f"Interleaved     : {sequenz}")
    print(f"Länge           : {len(sequenz)} "
          f"(= 2×{len(daten)//2 + len(daten)%2} Daten + 2×4 ECC)")
# endregion
