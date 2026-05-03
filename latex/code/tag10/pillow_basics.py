# Pillow-Grundlagen — die fünf Befehle, die du heute brauchst.
#
# Pillow ist nicht in der Standardbibliothek. Einmalig in Thonny:
#   Tools → Manage Packages → "Pillow" suchen → Install.

# region installprobe
from PIL import Image

print(Image.__name__, "läuft.")
# endregion


# region erstes_bild
# Ein 50 Pixel breites, 30 Pixel hohes Bild im Modus "1" (1 Bit pro
# Pixel = monochrom: nur schwarz oder weiß). Dritter Parameter ist
# die Hintergrundfarbe — im Modus "1" bedeutet 1 = weiß und 0 = schwarz.

from PIL import Image, ImageDraw

bild = Image.new("1", (50, 30), 1)        # weißes 50×30-Bild
zeichner = ImageDraw.Draw(bild)
zeichner.rectangle([(10, 5), (13, 24)], fill=0)   # ein Strich, 4 Pixel breit
bild.save("erster_strich.png")
print("Bild gespeichert.")
# endregion
