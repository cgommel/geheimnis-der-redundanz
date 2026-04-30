# Work in Progress

> Aktueller Arbeitsstand und nächste Schritte. Soll als persistenter
> Anker dienen, wenn die Chat-Historie verkürzt wird.

## Stand: 2026-04-30 (mitten in Etappe 9)

### Was auf `main` ist

- Etappen 1–8 vollständig (Reed-Solomon Encoder + Decoder)
- Hausschriften: Source Serif 4 / Source Sans 3 / Source Code Pro /
  STIX Two Math, vendored unter `latex/fonts/` (OFL-1.1)
- Output-Naming umgestellt:
  - Hauptbuch: `pdf/latex/geheimnis-der-redundanz.pdf` (110 Seiten)
  - Standalones: `pdf/latex/redundanz-tagN.pdf` (Buch bis Etappe N,
    18→108 Seiten, ohne Hauptbuch-Titelseite)
  - Helper `latex/buch-rumpf.tex` parametrisiert über `\maxetappe`
- Pagestyle: Frontmatter `plain`, Mainmatter `scrheadings`
- Lizenzen: CC BY-SA 4.0 fürs Buch, MIT für die Code-Snippets,
  OFL-1.1 für die Schriften
- README öffentlich-tauglich, technisches in `BUILD.md`
- CI: Action-Versionen Node-24-fähig
- Letztes Release: **`v2026.04.29.2`** + **`v2026.04.30`**

### Was auf `feature/tag9` liegt (in Arbeit, noch nicht gemergt)

**Etappe 9 — EAN-13 von Hand zeichnen** (Branch von `main`, nach
`v2026.04.30`).

Aktuell fertig:

- `latex/kapitel/tag9.tex`:
  - Lernziele + Material-Block
  - **Block 1** — Repetition Prüfziffer am Honig-EAN `4270004371635`
    (Glas „Sommer in Radebeul" von Gommels Bienen)
  - **Block 2** — Drei Codetabellen: Story UPC-A → EAN-13, Modul-Konzept,
    L/G/R-Tabellen kombiniert, Erstziffer-Paritätsmuster, Beispiel mit
    Honig-EAN
  - Bleistift-Übungen 1 (Prüfziffer) und 2 (Encoding-Folge ablesen)
- `latex/loesungen/tag9.tex`: Lösungen zu Übungen 1 und 2
- `latex/redundanz-tag9.tex`: Standalone-Master „Buch bis Etappe 9"
- `latex/ean13-tikz.tex`: TikZ-Renderer
  - `\eanbarcodebits{<95 Bits>}{<first>}{<left6>}{<right6>}` —
    rendert vorberechnete Bit-Liste
  - `\barcodehonig` — Convenience-Wrapper für den Honig-EAN
  - Wird via `praeambel.tex` automatisch geladen
- `Makefile`: `ETAPPEN := 1..9`, `redundanz-tag9` Target funktioniert

### Wo wir mitten drin sind: Barcode-Renderer „lebensecht"

Der EAN-13-Renderer läuft, wurde aber durch User-Feedback noch nicht
endgültig akzeptiert. Iterationsverlauf:

1. Erste Version: Striche gerendert, aber Guards gingen nach **oben**
   raus — falsch.
2. Korrigiert: Daten-Strich-Bottom y=3, Guard-Strich-Bottom y=0 (Guards
   ragen 3 Module nach unten).
3. User: „besser, aber noch nicht lebensecht."
4. Aktuelle Version (im letzten Commit): Daten y=0, Guards y=-3,
   Klarschrift bei y=-0.5 mit `\ttfamily\large`. Klarschrift-Strings
   ohne `\,`-Kerning (kompakter, mehr OCR-B-Look).

### Idee, die noch offen ist

- **Generalisieren** zu `\eanbarcode{<13-Ziffern>}` — der Renderer
  baut die Bit-Liste selbst aus L/G/R-Lookup + Pattern. xstring +
  csname-Tabellen. Aktuell ist nur `\barcodehonig` hartkodiert.
  Brauchen wir spätestens für die Zeichenvorlage (anderer Beispiel-EAN
  `4012345678901`).
- Alternative wäre das CTAN-Paket `ean` zu nutzen, hab aber noch nicht
  geprüft, ob es mit XeLaTeX + Source-Schriften gut zusammenspielt.

### Mängelliste (`doku/MAENGEL.md`)

16 Punkte gesammelt, alle offen außer LY-01 und LY-11 (erledigt).
Highlights:

- **LY-14** — Aufeinanderfolgende `aufgabe`-Boxen ohne Atemraum
  (sichtbar in Tag 1, hochpriorisiert für den Polish-Sprint)
- **LY-15** — Build-Provenance (Branch + Commit-ID) dezent ins PDF
- **LY-16** — Kolophon-Seite mit Lizenz-Hinweis und Repo-URL
- **TC-01** — Python-Snippets beim Build neben das PDF legen

## Nächste Schritte (priorisiert)

1. **Barcode-Renderer lebensecht** — User-Feedback abwarten zur
   aktuellen Version (Guards y=-3, Klarschrift `\large`). Falls
   weiterhin nicht passend: vermutlich Generalisierung zum
   parametrisierten `\eanbarcode{...}` mit weiteren Anpassungen.
2. **Block 3 schreiben** — EAN-13-Aufbau-Diagramm: Hellzonen, Guards,
   6+6-Aufteilung, Klarschrift. Mit visualisierten Längen, vermutlich
   ein zweiter TikZ-Block, der den Honig-EAN nochmal mit Annotationen
   zeigt.
3. **Block 4 schreiben** — Hand-Zeichnen-Werkstatt mit Verweis auf die
   Zeichenvorlage.
4. **Zeichenvorlage** als A4-quer Standalone-PDF: 4 Felder zum Probieren,
   eines mit dem Beispiel-EAN `4012345678901` vorausgefüllt.
5. **Block 5** — Drucken/Scannen/Debuggen.
6. **Block 6** — Reflexion + Brücke zu Etappe 10 (Pillow + EAN-13
   automatisiert).
7. **Hauptbuch** auf `\maxetappe=9` hochziehen.
8. **Merge nach `main`**, neuer Release-Tag.

## Konventionen, die wir uns gesetzt haben

- Erst sammeln in `doku/MAENGEL.md`, dann systematisch fixen — keine
  Hotfixes ohne Eintrag.
- Nach jedem Push: `gh run list` schauen, ob CI grün ist.
- Commit-Messages ohne Claude-Spuren, auf Deutsch.
- Farben in CMYK, Anführungszeichen Unicode (Babel-`"`-Shorthand ist
  global abgeschaltet — wenn doch ASCII-`"` reinrutscht, wird's mit
  dem Folge-Buchstaben zu Babel-Kuriositäten wie „Radebeulßum" statt
  „Radebeul" zum").
- Standalone-Master pro Etappe N: `latex/redundanz-tagN.tex` mit
  `\def\maxetappe{N}` plus `\input{buch-rumpf}`. Hauptbuch
  `latex/geheimnis-der-redundanz.tex` mit `\maxetappe=8` (ggf.
  hochzuziehen) und Titelseite.
- Tag in Branch-Name: `feature/tagN` für eine einzelne Etappe.
- Greta hat Praktikum mit Onkel (Imker, „Gommels Bienen", Honig
  „Sommer in Radebeul"). EAN dieses Glases: `4270004371635`.
  Persönlicher Anker für die Etappe.
- Iterativ vorgehen: pro Block Build → User schaut → korrigieren.
  Der User ist pingelig (mit Recht), und jede Iteration ist klein.

## Lokale Voraussetzungen

```bash
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   needspace unicode-math collection-latexextra
brew install --cask font-dejavu        # nur für Marginalien-Symbole
brew install pygments
pip install reedsolo                   # für Etappe 8
```

Schriften (Source Pro Familie, STIX Two Math) sind im Repo unter
`latex/fonts/` vendored — keine System-Installation nötig.
