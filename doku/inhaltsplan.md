# Inhaltsplan – Tage 1 bis 12 (+ Bonus)

> Tag 1 bis 6 sind als LaTeX-Kapitel im Buch (`pdf/latex/buch.pdf`).
> Hier ist der **rote Faden** der noch ausstehenden Tage 7–12 plus
> ein paar Bonus-Themen. Der Plan ist eine *Skizze* — feinjustiert
> wird basierend auf Greta-Feedback und je nach Tempo.

## Roter Faden des Gesamtwerks

```
Tag 1: Parität, EAN-13          ← einfache Prüfziffern, Erkennung           [fertig]
Tag 2: ISBN-10, Luhn,            ← elegantere Prüfziffern, Hamming-Distanz   [fertig]
       Hamming-Distanz           ← zentraler Begriff für Codes
Tag 3: Hamming-Code (7,4)        ← erstes echtes Korrigieren von Bitfehlern  [fertig]
Tag 4: SECDED, CRC,              ← Brücke zur Praxis (Bündelfehler!)         [fertig]
       Interleaving
─── Wechsel vom Bit zum Byte ───
Tag 5: Endliche Körper GF(2^n)   ← die Mathematik, die Reed-Solomon möglich  [fertig]
                                    macht — konkret aufgebaut für GF(2³)
Tag 6: Polynome über GF, RS-Idee ← Daten als Polynom, Stützstellen,          [fertig]
                                    Reed-Solomon durch Auswertung
Tag 7: RS-Encoder + GF(2⁸)       ← Wechsel auf 256 Elemente, Generator-      ⬜
                                    Polynom, systematische Codierung
Tag 8: RS-Decoder                ← Auslöschungs-Decoder von Hand,            ⬜
                                    reedsolo-Library für die Praxis,
                                    Berlekamp-Massey nur als Skizze
─── Intermezzo: Wir lernen zeichnen ───
Tag 9: 1D-Strichcode selbst      ← Python-Grafik mit Pillow, Code 39         ⬜
       zeichnen (NEU)               selbst codieren und ausdrucken,
                                    mit dem Handy scannen
─── Synthese: Datamatrix ───
Tag 10: Datamatrix-Symbol        ← Format, Layout, ECC-200, Daten-           ⬜
        (Theorie + Layout)          platzierungsalgorithmus
Tag 11: Datamatrix selbst        ← Encoder + Decoder, eigenes Symbol         ⬜
        zeichnen und decodieren     mit dem eigenen Namen drauf

─── Bonus, falls Greta noch Hunger hat ───
Tag 12: QR-Codes im Vergleich    ← gleiche Mathe, anderes Layout             (opt.)
Tag 13: Verkettete Codes         ← Voyager, CD-Audio, „warum Spotify nicht   (opt.)
        und LDPC-Ausblick           knirscht"
```

## Tag 7 – Reed-Solomon-Encoder + Wechsel auf GF(2⁸)

**Ziel:** Greta kann einen vollständigen Reed-Solomon-Encoder in
GF(2⁸) bauen und versteht die zwei äquivalenten Sichten:
Auswertungs-Encoder (Tag 6) und Generator-Polynom-Encoder (heute,
analog zu CRC aus Tag 4).

**Bausteine:**
- Block 1: GF(2⁸)-Wechsel — vier Code-Zeilen aus der GF8-Klasse
  ändern, alle 256 Elemente da. Demo: das Standard-Datamatrix-Polynom
  $x^8 + x^4 + x^3 + x^2 + 1$.
- Block 2: Generator-Polynom als Produkt von Linearfaktoren
  $(x - \alpha^0)(x - \alpha^1) \dots (x - \alpha^{2t-1})$ mit
  $\alpha$ als primitivem Element von GF(2⁸).
- Block 3: Systematischer Encoder (analog CRC): Daten plus angehängte
  Nullen modulo Generatorpolynom; Rest ist die Prüfsymbol-Folge.
- Block 4: RS(255, 251) als Beispiel — 4 Prüfsymbole, korrigiert 2
  Symbolfehler. Bleistift: kleine Variante RS(15, 11) über GF(2⁴),
  weil GF(2⁸)-Bleistiftrechnungen unmenschlich werden.
- Block 5: Python-Encoder, am echten RS(255, 251)-Beispiel verifiziert.

## Tag 8 – Reed-Solomon-Decoder

**Ziel:** Greta versteht Auslöschungs-Decoder vollständig (analog zur
ISBN-10-Detektivarbeit aus Tag 2), kann ihn selbst implementieren,
und nutzt für den allgemeinen Fall (unbekannte Fehlerposition) die
`reedsolo`-Bibliothek.

**Bausteine:**
- Block 1: Syndrom-Berechnung — der erste Schritt jedes Decoders.
- Block 2: Auslöschungs-Decoder von Hand. Wenn man weiß, *welche*
  Symbole fehlen, sind das nur lineare Gleichungen über GF(2⁸).
  Bleistift: konkretes RS(7, 3)-Beispiel mit zwei Auslöschungen über
  GF(2³).
- Block 3: Allgemeiner Decoder — Berlekamp-Massey-Algorithmus als
  Skizze („Magie-Box", die das Fehlerlokator-Polynom liefert), dann
  Forney-Formel für die Fehlerwerte. Volle Implementierung wäre
  Hochschulstoff; wir verstehen das Prinzip und gehen weiter.
- Block 4: Praxis mit `reedsolo`-Library. Fehler in eine Nachricht
  einbauen, Library korrigieren lassen, Grenzen des Verfahrens
  ausloten.
- Block 5: Reflexion — wie viele Fehler wurden korrigiert, was
  passiert jenseits der Grenze.

## Tag 9 – Wir zeichnen einen 1D-Strichcode (Intermezzo)

**Ziel:** Greta kann mit Pillow Pixel-Bilder erzeugen, beherrscht das
Code-39-Encoding und produziert einen scannbaren Strichcode mit dem
eigenen Namen — ausgedruckt und mit dem Handy gelesen.

**Warum dieser Tag:** Datamatrix-Code zu zeichnen ist konzeptionell
und handwerklich anspruchsvoll. Bevor wir uns dort versuchen, üben
wir die Grafik-Werkzeuge an einem trivialen 1D-Code.

**Bausteine:**
- Block 1: Pillow installieren (`pip install Pillow`), erste
  schwarz-weiße Pixel-Bilder, Rechteck zeichnen, als PNG speichern.
- Block 2: Code-39-Tabellen — 9 Striche pro Zeichen, davon 3 breit;
  Start- und Endsymbol `*`. Alphabet: A–Z, 0–9, plus ein paar
  Sonderzeichen.
- Block 3: Encoder schreiben — Text → Bitstrom → Bild.
- Block 4: Drucken + mit dem Handy scannen. Welche
  Strich-zu-Lücken-Verhältnisse funktionieren am besten? Druckqualität,
  Mindestbreite, Quiet-Zone vorne/hinten.
- Block 5: Reflexion — Code 39 hat keine Fehlerkorrektur. Was wäre
  die einfachste Erweiterung? (Brücke zu Datamatrix, das genau das
  hat.)

**Bonus:** EAN-13 selbst zeichnen — Greta hat die Mathe schon (Tag 1),
nur die Encoding-Tabellen sind anders (Set A/B/C). Als Heimarbeit.

## Tag 10 – Datamatrix-Symbol: Theorie & Layout

**Ziel:** Greta versteht den Aufbau eines Datamatrix-Codes (ECC-200)
soweit, dass sie an Tag 11 einen vollständigen Encoder bauen kann.

**Bausteine:**
- Symbol-Layout: L-Pattern (zwei feste Kanten), Zeitsignal (zwei
  abwechselnde Kanten), Datenbereich.
- Symbolgrößen: 10×10, 12×12, …, 144×144. Beziehung zwischen
  Symbolgröße und Anzahl Daten-/ECC-Bytes (Tabelle der wichtigsten).
- ECC-200: Reed-Solomon über GF(2⁸) mit Generatorpolynom abhängig
  von der Symbolgröße.
- Datenkodierung: ASCII-Modus (das wichtigste). C40, Text, Base 256
  als Ausblick.
- Datenplatzierungs-Algorithmus: das berühmte „Treppenmuster", das
  Daten- und ECC-Bytes über das Symbol verteilt.

## Tag 11 – Datamatrix selbst zeichnen und decodieren

**Ziel:** Synthese. Greta hat einen funktionierenden Encoder UND
Decoder für einen kleinen Datamatrix-Code.

**Bausteine:**
- Vollständiger Encoder: Text → ASCII-Encoding → Daten-Bytes →
  ECC-Bytes über Reed-Solomon → Symbol-Platzierung → PNG via Pillow.
- Decoder: Bild → Module-Erkennung (Hand-Eingabe für Fortgeschrittene
  optional, sonst aus dem eigenen Encoder zurück) → ECC-Korrektur →
  ASCII-Decoding → Text.
- Robustheits-Demo: Datamatrix bewusst beschädigen (mit dem Pinsel
  schwarze Flächen drauf) und Decoder zeigt, dass er trotzdem
  funktioniert.
- Reflexion: zwei Wochen Mathematik zusammengefasst — was steckt
  alles in dem schwarz-weißen Quadrat auf dem Versandetikett?

## Bonus-Tage

### Tag 12 – QR-Codes im Vergleich
Strukturell sehr ähnlich zu Datamatrix, aber mit eigenen
Codierungs-Tricks (vier ECC-Level: L, M, Q, H; Reed-Solomon ebenfalls
über GF(2⁸); Maskierungs-Patterns). Kompakter Tag, weil die meiste
Mathematik schon da ist.

### Tag 13 – Verkettete Codes und Praxis-Geschichten
Voyager-Sonden mit verkettetem Faltungscode + Reed-Solomon.
Audio-CDs mit CIRC. Modernere Verfahren: LDPC-Codes (kurz),
Turbo-Codes. Sicherheit vs. Integrität: kryptographische Hashes,
digitale Signaturen — als Kontrast zu Reed-Solomon.

## Tempo-Vorbehalt

Greta hat Tag 1 in 2 h, Tag 4 in 75 min durchgearbeitet — sie wird
schneller. Plan rechnet trotzdem mit der 2 h pro Tag-Faustregel; bei
zu schnellem Tempo ist Tag 12/13 die natürliche Reserve.

## Wie der Plan benutzt wird

Der Plan ist **bewusst grob** — Orientierung, kein Drehbuch. Vor
jedem neuen Tag:

1. Greta-Feedback aus `feedback-greta.md` konsultieren
2. Tempo des Vortags prüfen
3. Skizze für den nächsten Tag erstellen, mit dem Onkel abstimmen
4. Erst dann das Kapitel ausschreiben (`latex/kapitel/tagN.tex`,
   plus Code-Snippets in `latex/code/tagN/`, plus Lösungen in
   `latex/loesungen/tagN.tex`).
