# Zielpublikum: Greta

> Wer ist Greta, was bringt sie mit, was nicht – und was bedeutet das für den Stil und die Tiefe des Tutorials?

## Person

- Schülerin, **10. Klasse Gymnasium**
- macht ein **zweiwöchiges Schülerpraktikum** (vermutlich in einem technischen Umfeld – der Rahmen ist Informatik / Codierung).
- Mentor ist der Onkel (= der Nutzer dieses Projekts).

## Was Greta kann (soweit bekannt)

- **Schulmathematik bis 10. Klasse:** Bruchrechnen, lineare Gleichungen, ein bisschen Geometrie, einfache Wahrscheinlichkeit, Funktionen, möglicherweise erste Berührungen mit Logarithmen und Folgen.
- **Erste Python-Erfahrung:** Schleifen (`for`), Listen, Funktionen, einfache Bedingungen. Kann einen Pythonquellcode abtippen, in Thonny ausführen, Fehlermeldungen lesen.
- **Naturwissenschaftliche Neugier:** Sie hat sich für ein technisches Praktikum entschieden, das deutet auf Interesse hin.

## Was Greta vermutlich *noch nicht* kann

- **Modulo-Rechnung:** wurde an Tag 1 explizit eingeführt.
- **Beweise im engeren Sinn:** kann einer Argumentation folgen, aber selber einen Beweis aufbauen wäre noch Neuland. Die Übungen sollten daher **geführt** sein (Tipp 1, Tipp 2 … bis sie selbst draufkommt).
- **Mengen- und Strukturbegriffe** wie „endlicher Körper" oder „Restklasse" – aber sie kann durch konkretes Hantieren auf das Konzept geführt werden, ohne dass die abstrakte Definition zuerst kommt.
- **Vektor-/Matrixrechnung:** wahrscheinlich noch nicht. Falls ein Tutorial-Inhalt darauf zugreift, muss er die Werkzeuge mitbringen.
- **Polynome jenseits der Schul-Grundlagen:** Polynome als „Ausdrücke" sind ihr bekannt, Polynome als „Vektoren über einem Körper" oder als „Elemente einer Algebra" sind komplett neu.

## Was Greta laut Feedback mag

- Sie hat Tag 1 in **2 Stunden** durchgearbeitet und gesagt, dass „alles gefallen hat". Das deutet auf:
  - Tempo war angemessen (nicht zu langsam, nicht zu schnell)
  - Mischung aus Bleistift und Python hat funktioniert
  - Praxisbezug (EAN-13 auf der Schokolade) hat gezündet
- Bei Tag 2 hat sie kein Detail-Feedback gegeben.
- Tag 3 und 4 hat sie noch nicht bearbeitet.

## Implikationen für die Konzeption

### Schwierigkeitsgrad

- **Tag 1 (fertig)** ist der Maßstab: bei diesem Tempo sind ca. 2 h Bearbeitungszeit angemessen.
- Tag 2-4 (fertig) versuchen, dieses Tempo zu halten.
- Spätestens **Tag 5 (endliche Körper)** wird konzeptionell schwerer. Hier ist Behutsamkeit gefragt: kleine Beispiele mit GF(2^3) statt GF(2^8), viele konkrete Rechnungen.
- **Tag 7-8 (Reed-Solomon)** sind die größten Herausforderungen. Vermutlich kann der Decoder nicht in voller Tiefe behandelt werden – Auslöschungs-Decodierung ist machbar, Berlekamp-Massey wahrscheinlich nicht.

### Notation

- Mathematische Notation in Maßen. Wenn ein Begriff einmal eingeführt wurde, darf er verwendet werden, sollte aber bei wichtigen Stellen wieder ausgesprochen werden („Hamming-Distanz d, also die Anzahl der unterschiedlichen Stellen").
- **Variablen sprechend benennen:** in Python `paritaetsbit`, `daten`, `gesendet`, `empfangen` (deutsch) statt `p`, `d`, `s`, `r`.

### Bleistift-Aufgaben

- Sollen so dosiert sein, dass Greta sie **selbst lösen kann**, mit ein bisschen Hilfe an den richtigen Stellen.
- **Tipps gestaffelt anbieten:** Tipp 1 als kleiner Schubs, Tipp 2 nur wenn Tipp 1 nicht reicht.
- Lösungen ausführlich, mit Rechenweg.

### Python-Aufgaben

- **Rüstcode** wird mitgeliefert, Greta soll keine Boilerplate selbst schreiben müssen.
- Aufgaben sind **klein und klar abgegrenzt**: eine Funktion implementieren, einen Test schreiben, eine kleine Variation ausprobieren.
- Brute-Force-Tests sind ein Lieblingswerkzeug — Computer sind dafür perfekt, und Greta sieht sofort visuell, ob ihr Verfahren funktioniert.

## Soll das später als Buch wirklich für „Greta-Persönlich" bleiben?

Eine offene Frage für die Buchprojekt-Phase: Soll die Hauptperson Greta bleiben, oder soll für ein allgemeines Publikum zu „du" oder „der/die Lernende" abstrahiert werden?

**Empfehlung:** Greta beibehalten. Die direkte Ansprache an eine konkrete Person ist ein literarischer Trick, der dem Buch Charakter gibt (vergleichbar mit „Der kleine Hobbit" oder „Mein Onkel Albert"). Wenn Greta keine reale Person mehr ist, sondern ein Stilmittel, ist das in Ordnung — die Leserin identifiziert sich dann mit ihr.
