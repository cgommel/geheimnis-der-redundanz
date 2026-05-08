# Etappe 19: Hilfswerkzeug — generiert die log/antilog-Tabelle für GF(256)
# (Datamatrix ECC-200, primitives Polynom 0x12D, Generator α = 2) und alle
# Zwischenschritte, die für den Lösungsanhang von Tag 19 gebraucht werden.
#
# Ausgabe: ein Dump in stdout mit log-Tabelle, antilog-Tabelle und den
# vollständigen Encoder-Spuren für „MUT" (10×10) und „GESCHAFFT" (14×14).
#
# Greta benutzt nur die ersten beiden Abschnitte (die zwei Tabellen) als
# Werkstatt-Beilage. Den Rest gibt es ebenfalls zum Selbst-Vergleich, falls
# sich jemand verrechnet hat.

PRIM = 0x12D     # primitives Polynom für GF(256), ECC-200
ALPHA = 2        # Generator-Element


# region tabellen
def baue_tabellen():
    """log[v] = i so dass α^i = v   (für v in 1..255)
    antilog[i] = α^i mod prim       (für i in 0..254)
    Index 255..509 als Bequemlichkeitsverdoppelung, damit
    Multiplikation ohne extra mod 255 möglich ist."""
    antilog = [0] * 512
    log = [0] * 256
    x = 1
    for i in range(255):
        antilog[i] = x
        log[x] = i
        x <<= 1
        if x & 0x100:
            x ^= PRIM
    for i in range(255, 510):
        antilog[i] = antilog[i - 255]
    return log, antilog


def gf_mul(a, b, log, antilog):
    if a == 0 or b == 0:
        return 0
    return antilog[log[a] + log[b]]
# endregion


# region generator
def generator_polynom(n_ecc, log, antilog):
    """g(x) = ∏_{i=1..n_ecc} (x - α^i) im GF(256).

    Liefert eine Liste von Polynom-Zwischenständen (g_1, g_2, …, g_{n_ecc}),
    jedes Polynom als Koeffizienten-Liste [c₀, c₁, …, c_n] (aufsteigend
    nach Grad, c_n = 1)."""
    g = [1]
    schritte = []
    for i in range(1, n_ecc + 1):
        alpha_i = antilog[i]
        neu = [0] * (len(g) + 1)
        for j, c in enumerate(g):
            neu[j] ^= gf_mul(c, alpha_i, log, antilog)
            neu[j + 1] ^= c
        g = neu
        schritte.append(list(g))
    return g, schritte
# endregion


# region rs_encoding
def rs_encode_mit_spur(daten, n_ecc, log, antilog):
    """Reed-Solomon-Encoding mit voller Iterations-Spur."""
    g, _ = generator_polynom(n_ecc, log, antilog)
    rest = list(daten) + [0] * n_ecc
    iterationen = []
    for i in range(len(daten)):
        faktor = rest[i]
        spur = {
            "i": i + 1,
            "faktor": faktor,
            "rest_vor": list(rest),
            "mults": [],
        }
        if faktor != 0:
            for j in range(len(g)):
                koeff = g[len(g) - 1 - j]
                produkt = gf_mul(koeff, faktor, log, antilog)
                spur["mults"].append({
                    "j": j,
                    "g_koeff": koeff,
                    "faktor": faktor,
                    "produkt": produkt,
                    "rest_pos": i + j,
                    "rest_vor_pos": rest[i + j],
                    "rest_neu_pos": rest[i + j] ^ produkt,
                })
                rest[i + j] ^= produkt
        spur["rest_nach"] = list(rest)
        iterationen.append(spur)
    return rest[len(daten):], iterationen
# endregion


# region ascii_und_c40
def ascii_codewords(text):
    return [ord(ch) + 1 for ch in text]


C40_WERT = {" ": 3}
C40_WERT.update({str(d): 4 + d for d in range(10)})
C40_WERT.update({chr(ord("A") + i): 14 + i for i in range(26)})


def c40_codewords_mit_spur(text):
    """Volle C40-Sequenz inkl. Latch (230) und Unlatch (254).
    Liefert auch die Triplet-Zwischenrechnungen."""
    LATCH, UNLATCH = 230, 254
    triplets = []
    cws = [LATCH]
    for i in range(0, (len(text) // 3) * 3, 3):
        v1 = C40_WERT[text[i]]
        v2 = C40_WERT[text[i + 1]]
        v3 = C40_WERT[text[i + 2]]
        tmp = v1 * 1600 + v2 * 40 + v3 + 1
        b1, b2 = tmp >> 8, tmp & 0xFF
        cws.extend([b1, b2])
        triplets.append({
            "zeichen": (text[i], text[i + 1], text[i + 2]),
            "werte":   (v1, v2, v3),
            "tmp": tmp, "b1": b1, "b2": b2,
        })
    cws.append(UNLATCH)
    return cws, triplets
# endregion


# region drucken
def drucke_log_tabelle(log, antilog):
    print("=" * 78)
    print("LOG-TABELLE: log[v] für v in 1..255  (in 16 Spalten zu je 16 Werten)")
    print("=" * 78)
    print("       " + " ".join(f"{c:4d}" for c in range(16)))
    for r in range(16):
        zeile = []
        for c in range(16):
            v = r * 16 + c
            if v == 0:
                zeile.append("  --")
            else:
                zeile.append(f"{log[v]:4d}")
        print(f"{r * 16:3d}–{r * 16 + 15:3d} " + " ".join(zeile))
    print()
    print("=" * 78)
    print("ANTILOG-TABELLE: antilog[i] = α^i  für i in 0..254")
    print("=" * 78)
    print("       " + " ".join(f"{c:4d}" for c in range(16)))
    for r in range(16):
        zeile = []
        for c in range(16):
            i = r * 16 + c
            if i >= 255:
                zeile.append("    ")
            else:
                zeile.append(f"{antilog[i]:4d}")
        print(f"{r * 16:3d}–{r * 16 + 15:3d} " + " ".join(zeile))
    print()


def drucke_aufgabe(text, n_ecc, modus, log, antilog):
    print()
    print("#" * 78)
    print(f"#  AUFGABE: {text!r}  ({modus}, {len(text)} Zeichen, n_ecc = {n_ecc})")
    print("#" * 78)

    if modus == "ASCII":
        daten = ascii_codewords(text)
        print(f"\nDaten-Codewords (ASCII +1): {daten}")
    elif modus == "C40":
        daten, triplets = c40_codewords_mit_spur(text)
        print("\nC40-Triplets:")
        for t in triplets:
            z = "".join(t["zeichen"])
            v1, v2, v3 = t["werte"]
            print(f"  {z}: V1={v1}, V2={v2}, V3={v3}  →  "
                  f"tmp = {v1}*1600 + {v2}*40 + {v3} + 1 = {t['tmp']}  "
                  f"→  b1={t['b1']}, b2={t['b2']}")
        print(f"Daten-Codewords (mit Latch/Unlatch): {daten}")

    g, schritte = generator_polynom(n_ecc, log, antilog)
    print(f"\nGenerator-Polynom g_{n_ecc}(x), Aufbauschritte:")
    for i, koef in enumerate(schritte, start=1):
        print(f"  g_{i}(x): {koef}")
    print(f"Endgültig g_{n_ecc} (aufsteigend nach Grad): {g}")

    ecc, iterationen = rs_encode_mit_spur(daten, n_ecc, log, antilog)
    print(f"\nRS-Iterationen (insgesamt {len(iterationen)}):")
    for it in iterationen:
        print(f"\n  Iteration {it['i']}: Faktor f = {it['faktor']}")
        print(f"    Rest vorher: {it['rest_vor']}")
        for m in it["mults"]:
            if m["faktor"] != 0 and m["g_koeff"] != 0:
                la, lb = log[m["g_koeff"]], log[m["faktor"]]
                summe = (la + lb) % 255
                print(f"    j={m['j']}: g={m['g_koeff']:3d} × f={m['faktor']:3d}  "
                      f"=  α^{la} × α^{lb}  =  α^{summe}  =  {m['produkt']:3d}   "
                      f"rest[{m['rest_pos']}]: {m['rest_vor_pos']:3d} ⊕ "
                      f"{m['produkt']:3d} = {m['rest_neu_pos']:3d}")
        print(f"    Rest nachher: {it['rest_nach']}")

    print(f"\nFINALE ECC-Codewords ({n_ecc} Stück): {ecc}")
    print(f"FINALE Codeword-Sequenz (Daten + ECC): {list(daten) + list(ecc)}")
    print()
    print("Bit-Zerlegung:")
    for i, cw in enumerate(list(daten) + list(ecc), start=1):
        bits = format(cw, "08b")
        print(f"  CW {i:2d} = {cw:3d} = {bits}")
# endregion


if __name__ == "__main__":
    log, antilog = baue_tabellen()
    drucke_log_tabelle(log, antilog)
    drucke_aufgabe("MUT",       n_ecc=5, modus="ASCII", log=log, antilog=antilog)
    drucke_aufgabe("GESCHAFFT", n_ecc=10, modus="C40",  log=log, antilog=antilog)
