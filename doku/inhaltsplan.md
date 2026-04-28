# Inhaltsplan – Tage 5 bis 10

> Tag 1 bis 4 sind als Markdown-Hefte fertig. Hier ist der **rote Faden** der noch ausstehenden Tage 5–10. Der Plan ist eine *Skizze* — feinjustiert wird basierend auf Greta-Feedback und je nach Tempo.

## Roter Faden des Gesamtwerks

```
Tag 1: Parität, EAN-13      ← einfache Prüfziffern, Erkennung
Tag 2: ISBN-10, Luhn,        ← elegantere Prüfziffern, Hamming-Distanz
       Hamming-Distanz       ← zentraler Begriff für Codes
Tag 3: Hamming-Code (7,4)    ← erstes echtes Korrigieren von Bitfehlern
Tag 4: SECDED, CRC,          ← Brücke zur Praxis (Bündelfehler!)
       Interleaving
─── HARTE GRENZE: ab hier müssen wir vom Bit zum Byte umsteigen ───
Tag 5: Endliche Körper       ← die Mathematik, die Reed-Solomon erst möglich macht
Tag 6: Polynome über GF(2^n) ← Ergänzung der Mathematik, RS-Idee
Tag 7: Reed-Solomon-Encoder
Tag 8: Reed-Solomon-Decoder
Tag 9: Datamatrix-Symbol     ← Format spec, Layout, ECC-200
Tag 10: Datamatrix selbst
        zeichnen / decodieren ← die finale Synthese
```

## Tag 5 – Endliche Körper GF(2^n)

**Ziel:** Greta versteht, was ein endlicher Körper ist und kann in GF(2^3) oder GF(2^4) addieren und multiplizieren.

**Anker zum Vortag:** Tag 4 endete mit der Frage „Wie überträgt man Modulo auf Bytes?" Die Antwort: Polynom­arithmetik modulo eines irreduziblen Polynoms.

**Bausteine:**
- Wiederholung: Modulo bei Zahlen (Tag 1), Polynome modulo bei CRC (Tag 4)
- Was ist ein Körper? (Konkrete Definition: man kann +, −, ·, ÷ und es bleibt im Körper)
- GF(2) als kleinster Körper – Bits mit XOR und AND
- GF(2^3) konkret aufbauen: Polynome vom Grad < 3 über GF(2), modulo z. B. `x³ + x + 1`
- Multiplikationstafel von GF(2^3) zu Fuß ausrechnen (Bleistiftübung)
- Inverse finden — im Gegensatz zu Modulo 256 funktioniert hier wirklich alles
- Python-Einheit: GF(2^3)-Klasse mit add, mul, inv

**Erwarteter Schwierigkeitsgrad:** Höchster Tag bisher. Möglicherweise lohnt es sich, GF(2^3) statt GF(2^8) zu wählen (8 statt 256 Elemente — alles geht noch von Hand).

## Tag 6 – Polynome über GF(2^n) und die Reed-Solomon-Idee

**Ziel:** Greta versteht, warum man bei Reed-Solomon mit Polynomen über GF(2^n) arbeitet, und kann das Grundprinzip des „Lagrange-Interpolation"-Tricks erklären.

**Bausteine:**
- Polynome über GF(2^n) addieren, multiplizieren
- Schöne Eigenschaft: ein Polynom vom Grad k-1 ist eindeutig durch k Stützstellen bestimmt (Lagrange-Interpolation)
- Daraus die RS-Idee: k Datensymbole → Polynom vom Grad k-1 → an n Stellen ausgewertet → n Codesymbole
- Wenn n - k > 2t Symbole, kann man bis zu t Symbolfehler korrigieren
- Bleistift: kleines konkretes Beispiel mit GF(2^3), k=3, n=5 (3 Datensymbole, 2 Prüfsymbole)
- Python: Polynom-Klasse über GF, Auswertung an Stützstellen

## Tag 7 – Reed-Solomon-Encoder

**Ziel:** Greta kann einen vollständigen RS-Encoder für ein konkretes Beispiel bauen (z. B. RS(7,3) über GF(2^3)).

**Bausteine:**
- Generator-Polynom (oft als Produkt von Linearfaktoren)
- Systematischer Encoder: Daten + Prüfsymbole, sodass das Codepolynom durch das Generator-Polynom teilbar ist (analog zu CRC, Tag 4!)
- Bleistift: ein RS(7,3)-Codewort von Hand encoden
- Python: vollständiger Encoder

## Tag 8 – Reed-Solomon-Decoder

**Ziel:** Greta versteht den Decoder zumindest für den Fall „bekannte Auslöschungen" (das ist deutlich einfacher als der allgemeine Berlekamp-Massey). Idealerweise auch das einfachere Verfahren für bis zu t Fehler.

**Bausteine:**
- Syndromberechnung
- Auslöschungs-Decoder (wenn Position bekannt) — das ist konzeptionell wie ISBN-10 mit fehlender Ziffer (Tag 2)!
- Vollständiger Decoder als Skizze, evtl. nicht vollständig in Python (zu komplex)
- Stattdessen: vorhandene RS-Bibliothek nutzen und mit ihr spielen

**Pragmatische Alternative:** Wenn das zu schwer wird, kann Tag 8 auch sein „RS in der Praxis" — vorhandene Library `reedsolo` für Python nutzen, an QR-Codes ausprobieren, dann zu Datamatrix.

## Tag 9 – Datamatrix-Symbol

**Ziel:** Greta versteht den Aufbau eines Datamatrix-Codes (ECC-200, der heutige Standard).

**Bausteine:**
- Symbol-Layout: L-Pattern, Zeitsignal, Daten- und ECC-Bereich
- Wie viele Daten- vs. ECC-Symbole bei verschiedenen Symbolgrößen
- Encodierungsschemata (ASCII, C40, Text, Base 256)
- Datenplatzierungs-Algorithmus (das berühmte „Treppenmuster")
- Bleistift: ein kleinstes Datamatrix (10×10 mit 3 ECC-Bytes) selbst zeichnen
- Python: Encoder für kleine Datamatrix

## Tag 10 – Datamatrix selbst zeichnen / decodieren

**Ziel:** Synthese. Greta hat einen funktionierenden Encoder UND Decoder für einen kleinen Datamatrix.

**Bausteine:**
- Vollständige Encoder-Pipeline: Text → ASCII-Encoding → ECC-Bytes → Symbol-Platzierung → SVG / PNG
- Decoder: Bild → Module-Erkennung (Hand-Eingabe?) → ECC-Korrektur → Text
- Anwendung: einen Datamatrix mit ihrem Namen drauf erzeugen
- Demo: Datamatrix bewusst beschädigen und Decoder zeigt, dass er trotzdem funktioniert
- Reflexion über die zwei Wochen: Was hat sie gelernt? Wo wurde es schwer?

## Bonus-Themen, falls Zeit übrig bleibt

- **QR-Codes:** strukturell ähnlich, andere Codierungs-Tricks
- **Satellitenkommunikation:** verkettete Codes, Faltungscodes
- **Modernere Verfahren:** LDPC-Codes (kurz), Turbo-Codes
- **Sicherheit vs. Integrität:** kryptographische Hashes, digitale Signaturen — als Kontrast zu Reed-Solomon

## Tempo-Vorbehalt

Wenn Greta in den ersten Tagen langsamer ist als erwartet (z. B. weil der Mathe-Hintergrund schwächer ist), kann der Plan nach hinten skaliert werden:
- Tag 5 + 6 können in 3 Tage gestreckt werden, wenn endliche Körper schwer fallen
- Tag 7 + 8 sind die schwierigsten — hier ist Vorsicht angesagt
- Tag 9 + 10 können auch entfallen, wenn die Zeit knapp wird; dann ist das „Buch" eben „bis Reed-Solomon" und Datamatrix ist Ausblick

## Was Claude Code mit dem Plan macht

Der Plan ist **bewusst grob**. Er soll als Orientierung dienen, nicht als Drehbuch. Vor jedem neuen Tag:
1. Greta-Feedback aus `feedback-greta.md` konsultieren
2. Tempo des Vortags prüfen
3. Einen Vorschlag für den nächsten Tag erstellen (im Stil der bisherigen Skizzen, siehe z. B. die Skizze für Tag 2/3 in der Konversation, falls sie noch da ist)
4. Den Vorschlag mit dem Onkel abstimmen
5. Erst dann das Heft ausschreiben.
