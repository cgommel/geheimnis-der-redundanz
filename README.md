# Das Geheimnis der Redundanz

## Von der Prüfziffer zum Datamatrix

Ein Buchprojekt, das aus einem zweiwöchigen Schülerpraktikum hervorgeht.
Die Hauptperson ist **Greta** (10. Klasse Gymnasium); jedes Tageskapitel
führt einen Schritt weiter — Fehlererkennung, Fehlerkorrektur, endliche
Körper, Reed-Solomon, Datamatrix. Bleistift-Übungen auf Karopapier
wechseln sich mit Python-Einheiten in Thonny ab.

## Aktueller Stand

| Tag | Thema                                              | Status        | Greta |
|-----|----------------------------------------------------|---------------|-------|
| 1   | Prüfziffern: Parität, EAN-13                       | ✅ migriert   | ✅ ≈ 2 h |
| 2   | ISBN-10, Luhn, Hamming-Distanz                     | ✅ migriert   | ✅      |
| 3   | Hamming-Code (7,4)                                 | ✅ migriert   | offen   |
| 4   | SECDED, Bündelfehler, Interleaving, CRC            | ✅ migriert   | ✅ ≈ 75 min |
| 5   | Endliche Körper GF(2^n) — die neue Mathematik      | ✅ migriert   | offen   |
| 6   | Polynome über GF(2^n), Reed-Solomon-Idee           | offen         |         |
| 7   | Reed-Solomon: Encoder                              | offen         |         |
| 8   | Reed-Solomon: Decoder                              | offen         |         |
| 9   | Datamatrix-Symbol: Layout, Module, ECC-200         | offen         |         |
| 10  | Datamatrix selbst zeichnen / decodieren            | offen         |         |

Lösungen liegen im Anhang A. Aktueller Buchumfang: 72 Seiten.

## Verzeichnisstruktur

```text
.
├── README.md                       ← diese Datei
├── Makefile                        ← Build-Targets (make / make test-code / make clean)
├── latex/                          ← Single Source of Truth (LaTeX-native)
│   ├── buch.tex                    Master, scrbook twoside
│   ├── praeambel.tex               Pakete, Geometrie, Schriften, Header
│   ├── farben.tex                  CMYK-Farbset für die Aufgabentypen
│   ├── befehle.tex                 Aufgaben-Umgebungen, Code-Snippet-Wrapper
│   ├── kapitel/tagN.tex            Kapitel pro Tag (Aufgaben + Erklärtext)
│   ├── loesungen/tagN.tex          Lösungen pro Tag (eingebunden in den Anhang)
│   ├── anhang_loesungen.tex        Anhang-Master, bündelt loesungen/*.tex
│   ├── code/tagN/*.py              Eigenständig lauffähige Python-Snippets
│   │                               mit Region-Markern (# region NAME / # endregion)
│   ├── scripts/extract_region.py   Schneidet Regionen zur Build-Zeit aus
│   └── .latexmkrc                  XeLaTeX + shell-escape, Output nach ../pdf/latex/
├── doku/                           ← Redaktionelle Dokumentation
│   ├── zielpublikum.md             Wer ist Greta
│   ├── schreibstil.md              Tonalität, Konventionen
│   ├── inhaltsplan.md              Roter Faden Tag 1–10
│   ├── feedback-greta.md           Greta-Feedback je Tag
│   ├── LAYOUT_BRIEFING.md          Designentscheidungen für das doppelseitige Layout
│   └── WIP.md                      Aktueller Arbeitsstand
├── layout-konzepte/                ← Demo-PDF zum Layout-Briefing
└── pdf/                            ← Build-Output (gitignored)
    └── latex/buch.pdf
```

## Bauen

```bash
make           # baut das Buch nach pdf/latex/buch.pdf
make test-code # prüft die Python-Snippets syntaktisch
make clean     # entfernt Build-Artefakte
```

### Voraussetzungen lokal

```bash
# TeX-Pakete (TeX Live):
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   collection-latexextra
# Schriften:
brew install --cask font-dejavu        # macOS / Homebrew
# minted-Backend:
brew install pygments                  # macOS / Homebrew
```

Der Container-Build (kommt als nächste Phase) löst das ab und kapselt
die ganze Toolchain.

## Layout-Eigenschaften

- `scrbook` zweiseitig, A4, 11 pt, KOMA-Headings
- DejaVu Serif/Sans/Sans Mono
- Aufgaben-Umgebungen mit farbigem Strich auf der jeweils äußeren
  Seite (CMYK-Pastellfarben: Bleistift-Orange, Python-Blau,
  Werkzeug-Grün), page-aware (wechselt korrekt mit der
  Seitenparität, auch bei Aufgaben über Page-Breaks)
- Marginalie spiegelt mit, Symbol + Kapitälchen-Bezeichnung in der
  Aufgaben-Farbe
- Code-Highlighting via `minted` mit Tango-Style
- TikZ für Diagramme (z. B. das Hamming-Venn-Diagramm in Tag 3)

Begründungen und alle Designentscheidungen stehen in
`doku/LAYOUT_BRIEFING.md`.

## Wer entscheidet was?

- **Inhaltliche Stoffauswahl:** Onkel/Nutzer entscheidet, Claude
  schlägt vor.
- **Didaktische Reihenfolge und Tempo:** Claude schlägt vor, Onkel
  korrigiert anhand von Greta-Feedback.
- **Schreibstil und Wortwahl:** Claude schreibt, Onkel redigiert.
- **Layout und Build:** Claude implementiert, Onkel entscheidet das
  große Bild.
- **Greta-Feedback** wandert in `doku/feedback-greta.md` und wird vor
  jeder neuen Tagesplanung konsultiert.
