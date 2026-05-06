# Etappe 15, Stufe 1: Klassen verstehen anhand geometrischer Formen.
#
# Bevor wir den Datamatrix-Encoder zu einer Klasse umbauen, lernen
# wir das Konzept "Klasse" an einem Beispiel kennen, das nichts mit
# Barcodes zu tun hat: geometrische Formen.
#
# Eine Klasse ist ein Bauplan. Aus ihm entstehen "Instanzen" —
# konkrete Objekte mit eigenen Daten. Methoden sind Funktionen, die
# zur Klasse gehören und auf diesen Daten arbeiten.

# region basisklasse
class Form:
    """Basisklasse für alle geometrischen Formen.

    Beschreibt das, was alle Formen gemeinsam haben:
      - sie haben einen Namen
      - sie kennen ihre Fläche
      - sie können sich beschreiben
    """

    def __init__(self, name):
        # __init__ ist der Konstruktor. Er wird automatisch aufgerufen,
        # sobald jemand eine Instanz erzeugt: f = Form("Quadrat").
        # self ist die gerade erzeugte Instanz — ähnlich wie "ich"
        # in einem Personenpronom.
        self.name = name

    def flaeche(self):
        # Diese Methode wird von Unterklassen überschrieben.
        # Die Basisklasse selbst weiß keine Formel.
        raise NotImplementedError(
            f"{self.name} muss eine eigene flaeche()-Methode mitbringen"
        )

    def beschreibe(self):
        return f"{self.name}: Fläche = {self.flaeche():.2f}"
# endregion


# region unterklassen
class Kreis(Form):
    """Ein Kreis erbt von Form — er IST eine Form, mit zusätzlichem
    Radius und einer eigenen Flächenformel."""

    def __init__(self, radius):
        super().__init__("Kreis")  # Konstruktor der Elternklasse aufrufen
        self.radius = radius

    def flaeche(self):
        return 3.14159 * self.radius ** 2


class Rechteck(Form):
    def __init__(self, breite, hoehe):
        super().__init__("Rechteck")
        self.breite = breite
        self.hoehe = hoehe

    def flaeche(self):
        return self.breite * self.hoehe


class Dreieck(Form):
    def __init__(self, basis, hoehe):
        super().__init__("Dreieck")
        self.basis = basis
        self.hoehe = hoehe

    def flaeche(self):
        return 0.5 * self.basis * self.hoehe
# endregion


# region weitervererbung
class Quadrat(Rechteck):
    """Ein Quadrat IST ein spezielles Rechteck — Breite gleich Höhe.

    Wir erben von Rechteck statt von Form, weil ein Quadrat alle
    Eigenschaften eines Rechtecks hat. Die flaeche()-Methode bekommen
    wir geschenkt; nur den Konstruktor passen wir an."""

    def __init__(self, seite):
        super().__init__(seite, seite)
        self.name = "Quadrat"  # Namen überschreiben (war "Rechteck")
# endregion


# region demo
if __name__ == "__main__":
    formen = [
        Kreis(radius=3),
        Rechteck(breite=4, hoehe=5),
        Quadrat(seite=6),
        Dreieck(basis=8, hoehe=3),
    ]

    # Jede Instanz weiß selbst, wie sie ihre Fläche berechnet —
    # obwohl wir sie alle gleich behandeln (Polymorphismus).
    for f in formen:
        print(f.beschreibe())

    summe = sum(f.flaeche() for f in formen)
    print(f"Gesamtfläche: {summe:.2f}")
# endregion
