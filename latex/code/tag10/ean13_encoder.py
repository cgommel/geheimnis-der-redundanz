# EAN-13-Encoder mit Pillow.
#
# Greta hat in Etappe 9 das Encoding von Hand verstanden. Hier
# übersetzen wir es in Python — in drei Stufen vom „dummen" bis
# zum kompakten Code.

# region tabellen
# Drei Codetabellen pro Ziffer 0..9 (genau wie auf dem Werkstatt-
# Spickzettel) plus die Pattern-Tabelle für die Erstziffer.

L_CODES = {
    "0": "0001101", "1": "0011001", "2": "0010011", "3": "0111101",
    "4": "0100011", "5": "0110001", "6": "0101111", "7": "0111011",
    "8": "0110111", "9": "0001011",
}
G_CODES = {
    "0": "0100111", "1": "0110011", "2": "0011011", "3": "0100001",
    "4": "0011101", "5": "0111001", "6": "0000101", "7": "0010001",
    "8": "0001001", "9": "0010111",
}
R_CODES = {
    "0": "1110010", "1": "1100110", "2": "1101100", "3": "1000010",
    "4": "1011100", "5": "1001110", "6": "1010000", "7": "1000100",
    "8": "1001000", "9": "1110100",
}
PATTERNS = {
    "0": "LLLLLL", "1": "LLGLGG", "2": "LLGGLG", "3": "LLGGGL",
    "4": "LGLLGG", "5": "LGGLLG", "6": "LGGGLL", "7": "LGLGLG",
    "8": "LGLGGL", "9": "LGGLGL",
}
# endregion


# region stufe1_dumm
# Stufe 1 — sehr explizit, jeder Schritt einzeln. Funktioniert,
# ist aber lang. Pro Position eine if-Abfrage und eine Anweisung.
# (Hier nur die linken sechs Ziffern; die rechten gehen analog.)

ean = "4270004371635"
erste_ziffer = ean[0]                    # "4"
pattern = PATTERNS[erste_ziffer]         # "LGLLGG"

bits = "101"                             # Start-Guard

# Position 2 (Index 1 im EAN):
if pattern[0] == "L":
    bits = bits + L_CODES[ean[1]]
else:
    bits = bits + G_CODES[ean[1]]

# Position 3:
if pattern[1] == "L":
    bits = bits + L_CODES[ean[2]]
else:
    bits = bits + G_CODES[ean[2]]

# Position 4:
if pattern[2] == "L":
    bits = bits + L_CODES[ean[3]]
else:
    bits = bits + G_CODES[ean[3]]

# Position 5:
if pattern[3] == "L":
    bits = bits + L_CODES[ean[4]]
else:
    bits = bits + G_CODES[ean[4]]

# Position 6:
if pattern[4] == "L":
    bits = bits + L_CODES[ean[5]]
else:
    bits = bits + G_CODES[ean[5]]

# Position 7:
if pattern[5] == "L":
    bits = bits + L_CODES[ean[6]]
else:
    bits = bits + G_CODES[ean[6]]

bits = bits + "01010"                    # Mittel-Guard
# (rechte Hälfte und End-Guard genauso ausgeschrieben — wir
# sparen uns den Platz)

print(len(bits), "Bits bis hierher.")
# endregion


# region stufe2_loop
# Stufe 2 — alle sechs Positionen in einer for-Schleife. Statt
# der Indexangabe pattern[0], pattern[1], ... nutzen wir die
# Schleifenvariable i.

ean = "4270004371635"
erste_ziffer = ean[0]
pattern = PATTERNS[erste_ziffer]

bits = "101"
for i in range(6):
    if pattern[i] == "L":
        bits = bits + L_CODES[ean[i + 1]]
    else:
        bits = bits + G_CODES[ean[i + 1]]
bits = bits + "01010"
for i in range(6):
    bits = bits + R_CODES[ean[i + 7]]
bits = bits + "101"

print(len(bits), "Bits — Stufe 2.")
# endregion


# region stufe3_enumerate
# Stufe 3 — mit enumerate werden Index UND Wert gleichzeitig
# über die Schleife geliefert. Statt ean[i+1] schreiben wir
# direkt ziffer.

ean = "4270004371635"
erste_ziffer = ean[0]
pattern = PATTERNS[erste_ziffer]

bits = "101"
for i, ziffer in enumerate(ean[1:7]):
    if pattern[i] == "L":
        bits += L_CODES[ziffer]
    else:
        bits += G_CODES[ziffer]
bits += "01010"
for ziffer in ean[7:13]:
    bits += R_CODES[ziffer]
bits += "101"

print(len(bits), "Bits — Stufe 3.")
# endregion


# region funktion
# Stufe 3 als wiederverwendbare Funktion verpackt. Eingabe: ein
# 13-stelliger EAN. Ausgabe: die 95-Bit-Folge.

def bits_for_ean(ean):
    erste_ziffer = ean[0]
    pattern = PATTERNS[erste_ziffer]
    bits = "101"
    for i, ziffer in enumerate(ean[1:7]):
        if pattern[i] == "L":
            bits += L_CODES[ziffer]
        else:
            bits += G_CODES[ziffer]
    bits += "01010"
    for ziffer in ean[7:13]:
        bits += R_CODES[ziffer]
    bits += "101"
    return bits
# endregion


# region drawer
# Pro 1-Bit ein modulbreites schwarzes Rechteck. Hellzonen ergeben
# sich aus dem Offset hellzone_links.

from PIL import Image, ImageDraw

def draw_barcode(ean, modulbreite=4, hoehe=120, dateiname="barcode.png"):
    bits = bits_for_ean(ean)
    hellzone_links = 11 * modulbreite
    hellzone_rechts = 7 * modulbreite
    breite = hellzone_links + len(bits) * modulbreite + hellzone_rechts
    bild = Image.new("1", (breite, hoehe), 1)
    zeichner = ImageDraw.Draw(bild)
    for i, bit in enumerate(bits):
        if bit == "1":
            x0 = hellzone_links + i * modulbreite
            x1 = x0 + modulbreite - 1
            zeichner.rectangle([(x0, 0), (x1, hoehe - 1)], fill=0)
    bild.save(dateiname)
    print("Strichcode gespeichert:", dateiname)
# endregion


# region demo
if __name__ == "__main__":
    draw_barcode("4270004371635", dateiname="honig.png")
    draw_barcode("4006381333931", dateiname="schokolade.png")  # Tag 1
    draw_barcode("9783446435001", dateiname="buch.png")        # ISBN-13
# endregion
