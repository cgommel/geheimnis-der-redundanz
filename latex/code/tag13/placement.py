# Datamatrix ECC-200 Datenplatzierung.
#
# Eingabe: 12 Codewort-Bytes (5 Daten + 7 ECC für 12×12).
# Ausgabe: 12×12-Bit-Matrix (0 = weiß, 1 = schwarz). Der Daten-
#          bereich (alle inneren Module ohne L-Pattern und
#          Zeitsignal) ist gefüllt; die Frame-Module bleiben auf
#          None und werden in Etappe 14 als Rahmen drumgelegt.
#
# Algorithmus aus ISO/IEC 16022 Annex F (ECC-200 placement).
# Jedes 8-Bit-Codeword wird als "Utah"-L-Form ins Symbol gesetzt;
# ein Cursor wandert diagonal durch die Datenfläche. An den
# Symbol-Ecken gibt es vier Sonder-Wrap-Patterns (Corner1..4).
#
# Wichtig für 12×12: das Annex-F-Layout läuft auf einer
# 10×10-Mappingmatrix (Symbol-Innenfläche), nicht auf den vollen
# 12×12 Modulen. Die 100 Innenmodule fassen 12 Codewords á 8 Bit
# = 96 plus 4 fest definierte Padding-Bits unten rechts.

# region utah
def _place_one(layout, n, row, col, chr_, bit):
    """Setze einen Codeword/Bit-Slot, mit Wrap-around am Symbol-Rand."""
    if row < 0:
        row += n
        col += 4 - ((n + 4) % 8)
    if col < 0:
        col += n
        row += 4 - ((n + 4) % 8)
    layout[row][col] = (chr_, bit)


def _place_utah(layout, n, row, col, chr_):
    """Setzt die 8 Bits eines Codeworts als Utah-L-Form.
    Bit 1 = MSB an Position (row-2, col-2), Bit 8 = LSB an (row, col)."""
    _place_one(layout, n, row - 2, col - 2, chr_, 1)
    _place_one(layout, n, row - 2, col - 1, chr_, 2)
    _place_one(layout, n, row - 1, col - 2, chr_, 3)
    _place_one(layout, n, row - 1, col - 1, chr_, 4)
    _place_one(layout, n, row - 1, col,     chr_, 5)
    _place_one(layout, n, row,     col - 2, chr_, 6)
    _place_one(layout, n, row,     col - 1, chr_, 7)
    _place_one(layout, n, row,     col,     chr_, 8)
# endregion


# region corners
def _place_corner1(layout, n, chr_):
    _place_one(layout, n, n - 1, 0,     chr_, 1)
    _place_one(layout, n, n - 1, 1,     chr_, 2)
    _place_one(layout, n, n - 1, 2,     chr_, 3)
    _place_one(layout, n, 0,     n - 2, chr_, 4)
    _place_one(layout, n, 0,     n - 1, chr_, 5)
    _place_one(layout, n, 1,     n - 1, chr_, 6)
    _place_one(layout, n, 2,     n - 1, chr_, 7)
    _place_one(layout, n, 3,     n - 1, chr_, 8)


def _place_corner2(layout, n, chr_):
    _place_one(layout, n, n - 3, 0,     chr_, 1)
    _place_one(layout, n, n - 2, 0,     chr_, 2)
    _place_one(layout, n, n - 1, 0,     chr_, 3)
    _place_one(layout, n, 0,     n - 4, chr_, 4)
    _place_one(layout, n, 0,     n - 3, chr_, 5)
    _place_one(layout, n, 0,     n - 2, chr_, 6)
    _place_one(layout, n, 0,     n - 1, chr_, 7)
    _place_one(layout, n, 1,     n - 1, chr_, 8)


def _place_corner3(layout, n, chr_):
    _place_one(layout, n, n - 3, 0,     chr_, 1)
    _place_one(layout, n, n - 2, 0,     chr_, 2)
    _place_one(layout, n, n - 1, 0,     chr_, 3)
    _place_one(layout, n, 0,     n - 2, chr_, 4)
    _place_one(layout, n, 0,     n - 1, chr_, 5)
    _place_one(layout, n, 1,     n - 1, chr_, 6)
    _place_one(layout, n, 2,     n - 1, chr_, 7)
    _place_one(layout, n, 3,     n - 1, chr_, 8)


def _place_corner4(layout, n, chr_):
    _place_one(layout, n, n - 1, 0,     chr_, 1)
    _place_one(layout, n, n - 1, n - 1, chr_, 2)
    _place_one(layout, n, 0,     n - 3, chr_, 3)
    _place_one(layout, n, 0,     n - 2, chr_, 4)
    _place_one(layout, n, 0,     n - 1, chr_, 5)
    _place_one(layout, n, 1,     n - 3, chr_, 6)
    _place_one(layout, n, 1,     n - 2, chr_, 7)
    _place_one(layout, n, 1,     n - 1, chr_, 8)
# endregion


# region main
def _build_layout(n_inner):
    """Annex-F-Layout für eine n_inner × n_inner Mappingmatrix.
    Liefert eine Matrix aus (codeword_index, bit_index) oder None."""
    layout = [[None] * n_inner for _ in range(n_inner)]
    chr_ = 1
    row, col = 4, 0
    while True:
        # Vier Sonder-Eckfälle
        if row == n_inner and col == 0:
            _place_corner1(layout, n_inner, chr_); chr_ += 1
        if row == n_inner - 2 and col == 0 and (n_inner % 4) != 0:
            _place_corner2(layout, n_inner, chr_); chr_ += 1
        if row == n_inner - 2 and col == 0 and (n_inner % 8) == 4:
            _place_corner3(layout, n_inner, chr_); chr_ += 1
        if row == n_inner + 4 and col == 2 and (n_inner % 8) == 0:
            _place_corner4(layout, n_inner, chr_); chr_ += 1
        # Diagonale nach oben-rechts
        while True:
            if row < n_inner and col >= 0 and layout[row][col] is None:
                _place_utah(layout, n_inner, row, col, chr_); chr_ += 1
            row -= 2
            col += 2
            if not (row >= 0 and col < n_inner):
                break
        row += 1
        col += 3
        # Diagonale nach unten-links
        while True:
            if row >= 0 and col < n_inner and layout[row][col] is None:
                _place_utah(layout, n_inner, row, col, chr_); chr_ += 1
            row += 2
            col -= 2
            if not (row < n_inner and col >= 0):
                break
        row += 3
        col += 1
        if not (row < n_inner or col < n_inner):
            break
    return layout


def place_codewords(codewords, n=12):
    """Datenbereich-Platzierung für ein n×n ECC-200-Symbol.

    Eingabe: Liste von Codewort-Bytes (für n=12 sind das 12 Stück).
    Ausgabe: n×n-Matrix. Datenmodule sind auf 0/1 gesetzt, Frame-
    Module (L-Pattern + Zeitsignal) bleiben None und werden in
    Etappe 14 als Rahmen drumgelegt.

    Konvention: Bit 1 jedes Codeworts ist das MSB (Wert 128),
    Bit 8 das LSB (Wert 1). Diese Reihenfolge passt zu pylibdmtx
    und zur ISO-Spec.
    """
    inner = n - 2  # Innenfläche ohne L-Pattern und Zeitsignal
    layout = _build_layout(inner)
    matrix = [[None] * n for _ in range(n)]

    for r in range(inner):
        for c in range(inner):
            cell = layout[r][c]
            if cell is None:
                # Padding: festes Schachbrett-Pattern
                bit = 1 if ((r + c) % 2 == 0) else 0
                matrix[r + 1][c + 1] = bit
                continue
            chr_, bit_no = cell
            if 1 <= chr_ <= len(codewords):
                cw = codewords[chr_ - 1]
                # Bit 1 = MSB (Wert 128)
                bit = (cw >> (8 - bit_no)) & 1
                matrix[r + 1][c + 1] = bit
            else:
                # Sollte für n=12 nicht eintreten (alle Slots belegt
                # entweder durch Codewords oder Padding)
                bit = 1 if (((r + 1) + (c + 1)) % 2 == 0) else 0
                matrix[r + 1][c + 1] = bit

    return matrix
# endregion


# region demo
def _render(matrix, n=12):
    """Liefert die Matrix als String mit █ / · / ? für Anzeige."""
    lines = []
    for row in matrix:
        lines.append("".join(
            "█" if v == 1 else ("·" if v == 0 else "?") for v in row
        ))
    return "\n".join(lines)


def _reference_matrix(payload):
    """Erzeugt die pylibdmtx-Referenzmatrix für eine 12×12-Nutzlast."""
    from pylibdmtx.pylibdmtx import encode
    from PIL import Image
    encoded = encode(payload, size="12x12")
    img = Image.frombytes(
        "RGB", (encoded.width, encoded.height), encoded.pixels
    ).convert("L")
    # 80×80 Bild, 12×12 Module à 5 Pixel, 10 Pixel Quietzone
    return [
        [1 if img.getpixel((10 + c * 5 + 2, 10 + r * 5 + 2)) < 128 else 0
         for c in range(12)]
        for r in range(12)
    ]


def _is_frame(r, c, n=12):
    return c == 0 or c == n - 1 or r == 0 or r == n - 1


def verify_against_reference():
    """Vergleicht die generierten Matrizen für HONIG und GRETA mit
    der pylibdmtx-Referenz."""
    cases = [
        ("HONIG", b"HONIG",
         [73, 80, 79, 74, 72, 70, 186, 97, 167, 44, 40, 243]),
        ("GRETA", b"GRETA",
         [72, 83, 70, 85, 66, 64, 90, 71, 128, 186, 106, 125]),
    ]
    for name, payload, codewords in cases:
        generated = place_codewords(codewords, n=12)
        reference = _reference_matrix(payload)
        mismatches = []
        for r in range(12):
            for c in range(12):
                if _is_frame(r, c):
                    continue
                if generated[r][c] != reference[r][c]:
                    mismatches.append((r, c, generated[r][c], reference[r][c]))
        if not mismatches:
            print(f"\u2713 {name} matches")
        else:
            print(f"\u2717 {name}: {len(mismatches)} mismatches")
            for r, c, g, ref in mismatches[:10]:
                print(f"    ({r},{c}) generated={g} reference={ref}")


if __name__ == "__main__":
    cw = [73, 80, 79, 74, 72, 70, 186, 97, 167, 44, 40, 243]
    m = place_codewords(cw, 12)
    print("Datenbereich für HONIG (Frame = ?):")
    print(_render(m))
    print()
    verify_against_reference()
# endregion
