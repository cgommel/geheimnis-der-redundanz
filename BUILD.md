# Buch aus den Quellen bauen

Das Buch wird aus LaTeX-Quellen gebaut, mit `xelatex`,
`glossaries-extra`, `tcolorbox` und `minted` (Code-Highlighting via
Pygments).

## Schnellstart

```bash
make                    # Hauptbuch nach pdf/latex/geheimnis-der-redundanz.pdf
make redundanz-tag5     # Standalone „Buch bis Etappe 5" (Etappen 1..5 + Lösungen)
make standalones        # alle Standalones (redundanz-tag1.pdf .. redundanz-tag8.pdf)
make test-code          # prüft die Python-Snippets syntaktisch
make clean              # entfernt Build-Artefakte
```

## Container-Build (empfohlen)

Wenn die TeX-Live-Welt lokal nicht passt, baut der Container alles
reproduzierbar (Debian Trixie + TeX Live):

```bash
make container         # Engine-Auto-Detection: bevorzugt Apple `container`,
                       # Fallback `docker`. Erzwingbar mit ENGINE=docker
make container-clean
```

## Lokale Voraussetzungen (ohne Container)

```bash
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   needspace unicode-math collection-latexextra
brew install --cask font-dejavu        # macOS / Homebrew (für Marginalien-Symbole)
brew install pygments
pip install reedsolo                   # für Etappe 8
```

**Fonts** (Source Serif 4, Source Sans 3, Source Code Pro, STIX Two
Math) liegen vendored unter [`latex/fonts/`](latex/fonts/) und werden
über `fontspec`-`Path=` direkt aus dem Repo geladen — keine
System-Installation nötig. Provenance und Lizenzen siehe
[`latex/fonts/README.md`](latex/fonts/README.md).

## Standalones „Buch bis Etappe N"

Pro Etappe N (1..8) gibt es einen Master `latex/redundanz-tagN.tex`,
der das Buch im Stand bis Etappe N rendert — vollständig (Vorwort,
Inhaltsverzeichnis, Etappen 1..N, Lösungen 1..N, Glossar, Index),
nur ohne die Hauptbuch-Titelseite. Damit kann eine Lesende die Etappe
in Kontext der vorigen Etappen lesen, ohne das ganze Buch zu kennen.

```bash
make redundanz-tag1    # Buch bis Etappe 1
make redundanz-tag5    # Buch bis Etappe 5
make standalones       # alle Standalones der Reihe nach
```

Alle Standalones teilen sich den Body in `latex/buch-rumpf.tex`; der
Master setzt nur `\maxetappe` und (für das Hauptbuch) die Titelseite.
Eine neue Etappe hinzufügen heißt: `\maxetappe` im Hauptbuch
hochziehen plus eine kurze `latex/redundanz-tag(N+1).tex` anlegen.

## Verzeichnisstruktur

```text
.
├── Makefile                          ← Build-Targets (make, container, clean, …)
├── latex/                            ← Single Source of Truth (LaTeX-native)
│   ├── geheimnis-der-redundanz.tex   Hauptbuch-Master (Titelseite + alle Etappen)
│   ├── redundanz-tagN.tex            Standalone-Master „Buch bis Etappe N"
│   ├── buch-rumpf.tex                Gemeinsamer Body, parametrisiert über \maxetappe
│   ├── praeambel.tex                 Pakete, Geometrie, Schriften, Kopfzeile
│   ├── farben.tex                    CMYK-Farbset für die Aufgabentypen
│   ├── befehle.tex                   Aufgaben-Umgebungen, Code-Snippet-Wrapper
│   ├── glossar.tex                   Glossar-Einträge (glossaries-extra)
│   ├── vorwort.tex                   Frontmatter-Kapitel
│   ├── kapitel/tagN.tex              Etappen
│   ├── loesungen/tagN.tex            Lösungen pro Etappe
│   ├── code/tagN/*.py                Lauffähige Python-Snippets mit
│   │                                 Region-Markern (# region NAME / # endregion)
│   ├── scripts/extract_region.py     Schneidet Regionen zur Build-Zeit aus
│   ├── fonts/                        Vendored Source Pro + STIX Two Math (OFL)
│   └── .latexmkrc                    XeLaTeX + shell-escape, Output nach pdf/
├── build/                            ← Container-Build
│   ├── Dockerfile                    Debian Trixie + TeX Live
│   └── in-container.sh               Engine-Detection-Wrapper
├── .github/workflows/
│   ├── build.yml                     CI: jeder Push baut das Buch
│   └── release.yml                   Tag-getriggertes Release mit PDF-Asset
├── doku/                             ← Redaktionelle Dokumentation
│   ├── zielpublikum.md               Profil der Zielperson
│   ├── schreibstil.md                Tonalität, Konventionen
│   ├── inhaltsplan.md                Roter Faden über alle Etappen
│   ├── feedback-greta.md             Rückmeldungen je Etappe
│   ├── LAYOUT_BRIEFING.md            Designentscheidungen für das Layout
│   ├── MAENGEL.md                    Sammelliste für den Polish-Sprint
│   └── WIP.md                        Aktueller Arbeitsstand
└── pdf/latex/                        ← Build-Output (gitignored)
    ├── geheimnis-der-redundanz.pdf       Hauptbuch
    └── redundanz-tagN.pdf                Standalones bis Etappe N
```

## Layout

- `scrbook` zweiseitig, A4, 11 pt, KOMA-Headings
- Source Serif 4 (Fließtext), Source Sans 3 (Überschriften, Marginalien),
  Source Code Pro (Quelltexte); STIX Two Math für Formeln (alle vendored)
- Aufgaben-Umgebungen mit farbigem Strich auf der jeweils äußeren
  Seite (CMYK-Pastell: Bleistift-Orange, Python-Blau, Werkzeug-Grün);
  page-aware, wechselt korrekt mit der Seitenparität auch über
  Page-Breaks hinweg
- Marginalie spiegelt mit, Symbol + Bezeichnung in der Aufgaben-Farbe
- Code-Highlighting via `minted` mit Tango-Style
- TikZ für Diagramme

Begründungen und alle Designentscheidungen stehen in
[`doku/LAYOUT_BRIEFING.md`](doku/LAYOUT_BRIEFING.md).
