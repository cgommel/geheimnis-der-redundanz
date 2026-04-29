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
─── Intermezzo: EAN-13 zweimal zeichnen ───
Tag  9: EAN-13 berechnen und      ← Anwendungsetappe: eigenen 12-Ziffer-       ⬜
        von Hand zeichnen (NEU)     Code wählen, Prüfziffer berechnen,
                                    Encoding-Tabellen L/G/R lernen,
                                    Strichcode mit der Zeichenvorlage
                                    Modul für Modul ausfüllen, scannen
Tag 10: EAN-13 mit Python         ← gleicher Code, jetzt automatisiert:       ⬜
        zeichnen (NEU)              Pillow, schwarz-weiße Pixel, Encoder
                                    in 30 Zeilen, beliebig viele Codes
                                    auf Knopfdruck — Aha „Python sparrrt"
─── Synthese: Datamatrix ───
Tag 11: Datamatrix-Symbol         ← Format, Layout, ECC-200, Daten-           ⬜
        (Theorie + Layout)          platzierungsalgorithmus
Tag 12: Datamatrix selbst         ← Encoder + Decoder, eigenes Symbol         ⬜
        zeichnen und decodieren     mit dem eigenen Namen drauf

─── Bonus, falls Greta noch Hunger hat ───
Tag 13: QR-Codes im Vergleich     ← gleiche Mathe, anderes Layout             (opt.)
Tag 14: Verkettete Codes          ← Voyager, CD-Audio, „warum Spotify nicht   (opt.)
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

## Tag 9 – EAN-13 von Hand zeichnen (Intermezzo)

**Ziel:** Greta beweist sich selbst, dass sie einen scannbaren
Strichcode \emph{vollständig von Hand} hinbekommt — mit Bleistift und
Lineal aus zwölf selbstgewählten Ziffern einen EAN-13, der vom
Handy-Scanner anstandslos gelesen wird. Der Erkenntnisgewinn („das
geht wirklich") ist der Kern dieses Intermezzos, nicht das
Werkzeug-Lernen.

**Warum dieser Tag:** Datamatrix-Code zu zeichnen ist konzeptionell
und handwerklich anspruchsvoll. Vorher wird eingeübt, wie man
überhaupt einen druckbaren, scannbaren Code zeichnet — an einem
1D-Format, das Greta aus Tag 1 schon kennt (Prüfziffer, Verifikation).

**Bausteine:**

- Block 1: Eigenen 12-Ziffer-Code wählen (z.\,B. Geburtsdatum
  \texttt{ttmmjjjjxxxx}), Prüfziffer wie an Tag 1 berechnen. Im
  Lösungsteil ausführlich vorgerechnet, damit der Zeichen-Code
  garantiert korrekt ist.
- Block 2: Encoding-Tabellen — L-, G- und R-Codes für die zehn
  Ziffern, plus Paritätsmuster der Erstziffer (steuert L/G-Verteilung
  in der linken Hälfte). Das ist neu gegenüber Tag 1.
- Block 3: Aufbau eines EAN-13 — Hellzonen, Start-/Mittel-/Endguards,
  95 Datenmodule, 6+6-Aufteilung, Klarschrift unter dem Code.
- Block 4: Zeichenvorlage als separates Standalone-PDF (A4 quer): vier
  Felder zum Probieren, eines davon mit einem fertig gezeichneten
  Beispiel-EAN als Vorlage (andere Ziffern als Gretas Code, damit
  nicht nur abgemalt wird). Modul-Hilfsraster, Klarschriftkästchen,
  L/G/R-Markierung pro Position.
- Block 5: Ausdrucken, scannen, debuggen — was passiert, wenn ein
  einzelner Strich zu schmal/zu breit ist? Mindestmodulbreite,
  Quiet-Zone, Druckqualität.
- Block 6: Reflexion — EAN-13 hat (außer der Prüfziffer) keine
  Fehlerkorrektur. Datamatrix-Vorschau: das Quadrat-Format hat
  Reed-Solomon eingebaut, deshalb übersteht es Beschädigung.

## Tag 10 – EAN-13 mit Python zeichnen (Intermezzo, Teil 2)

**Ziel:** Nachdem Greta von Hand einen scannbaren EAN-13 hinbekommen
hat, automatisiert sie denselben Vorgang in Python. Erkenntnisgewinn:
„dasselbe, was eine Stunde Bleistift gekostet hat, sind in Python 30
Zeilen und beliebig oft wiederholbar." Brücke zu Datamatrix, das wir
sowieso nur noch programmatisch bauen können.

**Warum direkt nach Tag 9:** Hand-Zeichnung gibt das Verständnis,
Python-Zeichnung den praktischen Hebel. Greta hat alle Encoding-Tabellen
schon im Kopf (Tag 9), Pillow kommt nur als Werkzeug dazu.

**Bausteine:**

- Block 1: Pillow installieren (`pip install Pillow`), erste
  schwarz-weiße Pixel-Bilder, Rechteck zeichnen, als PNG speichern.
- Block 2: L-/G-/R-Tabellen aus Tag 9 als Python-Dictionaries.
- Block 3: EAN-13-Encoder schreiben — 13 Ziffern → Bitstrom →
  PNG-Bild mit konfigurierbarer Modulbreite. Quiet-Zonen, Klarschrift
  unter dem Code (optional via PIL.ImageDraw + Font).
- Block 4: Verifikation — den Greta-Code aus Tag 9 erzeugen, Hand-
  und Python-Zeichnung überlagern (oder einfach beide scannen).
- Block 5: Variation — eine Mini-Galerie scannbarer Strichcodes für
  Familienmitglieder erzeugen (jeweils Geburtsdatum + Initialen).
- Block 6: Reflexion — Skalierung. Was kostet ein Datamatrix mit
  derselben Methode? (Spoiler: deutlich mehr als 30 Zeilen, deshalb
  in den nächsten Tagen mit Bibliothek arbeiten.)

## Tag 11 – Datamatrix-Symbol: Theorie & Layout

**Ziel:** Greta versteht den Aufbau eines Datamatrix-Codes (ECC-200)
soweit, dass sie an Tag 12 einen vollständigen Encoder bauen kann.

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

## Tag 12 – Datamatrix selbst zeichnen und decodieren

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

### Tag 13 – QR-Codes im Vergleich
Strukturell sehr ähnlich zu Datamatrix, aber mit eigenen
Codierungs-Tricks (vier ECC-Level: L, M, Q, H; Reed-Solomon ebenfalls
über GF(2⁸); Maskierungs-Patterns). Kompakter Tag, weil die meiste
Mathematik schon da ist.

### Tag 14 – Verkettete Codes und Praxis-Geschichten
Voyager-Sonden mit verkettetem Faltungscode + Reed-Solomon.
Audio-CDs mit CIRC. Modernere Verfahren: LDPC-Codes (kurz),
Turbo-Codes. Sicherheit vs. Integrität: kryptographische Hashes,
digitale Signaturen — als Kontrast zu Reed-Solomon.

## Tempo-Vorbehalt

Greta hat Tag 1 in 2 h, Tag 4 in 75 min durchgearbeitet — sie wird
schneller. Plan rechnet trotzdem mit der 2 h pro Tag-Faustregel; bei
zu schnellem Tempo ist Tag 13/14 die natürliche Reserve.

## Wie der Plan benutzt wird

Der Plan ist **bewusst grob** — Orientierung, kein Drehbuch. Vor
jedem neuen Tag:

1. Greta-Feedback aus `feedback-greta.md` konsultieren
2. Tempo des Vortags prüfen
3. Skizze für den nächsten Tag erstellen, mit dem Onkel abstimmen
4. Erst dann das Kapitel ausschreiben (`latex/kapitel/tagN.tex`,
   plus Code-Snippets in `latex/code/tagN/`, plus Lösungen in
   `latex/loesungen/tagN.tex`).
