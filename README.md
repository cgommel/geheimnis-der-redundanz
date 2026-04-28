# Das Geheimnis der Redundanz
## Von der Prüfziffer zum Datamatrix

> **Wichtigstes Dokument für den Wechsel zu Claude Code.** Dieses README ist der vollständige Kontext, den ein neuer Claude (oder Mensch) braucht, um an dem Projekt sinnvoll weiterarbeiten zu können.

## Worum geht's?

Ein Buchprojekt, das aus einem zweiwöchigen Schülerpraktikum-Tutorial hervorgeht. Die Hauptperson ist **Greta** (10. Klasse Gymnasium); die Tagestouren werden **Schritt für Schritt** zu einem tiefen Verständnis von **Datamatrix-2D-Codes** geführt. Roter Faden: Fehlererkennung → Fehlerkorrektur → endliche Körper → Reed-Solomon → Datamatrix.

Das Buch wird in **Tageshefte** aufgeteilt (10 Tage geplant). Jedes Heft kombiniert **Bleistiftübungen** auf Karopapier mit **Python-Übungen** in Thonny.

Das Projekt wird vom Onkel/Mentor (= der Nutzer) in Iterationen mit Claude entwickelt; Greta arbeitet die Hefte durch und gibt Feedback.

## Aktueller Stand (Stand: Übergabe an Claude Code)

| Tag | Thema                                          | Markdown | PDF | Bemerkung                |
|-----|------------------------------------------------|:--------:|:---:|--------------------------|
| 1   | Prüfziffern: Parität, EAN-13                   | ✓        | ✓   | von Greta durchgearbeitet (≈ 2 h, „alles gefallen") |
| 2   | ISBN-10, Luhn, Hamming-Distanz                 | ✓        | ✓   | von Greta durchgearbeitet, kein Detail-Feedback |
| 3   | Hamming-Code (7,4)                             | ✓        | ✓   | noch nicht von Greta bearbeitet |
| 4   | SECDED, Bündelfehler, Interleaving, CRC        | ✓        | ✓   | von Greta durchgearbeitet (≈ 75 min) |
| 5   | Endliche Körper GF(2^n) – die neue Mathematik  | ✓        | ✓   | noch nicht von Greta bearbeitet |
| 6   | Polynome über GF(2^n), Reed-Solomon-Idee       | offen    |     |                          |
| 7   | Reed-Solomon: Encoder                          | offen    |     |                          |
| 8   | Reed-Solomon: Decoder                          | offen    |     |                          |
| 9   | Datamatrix-Symbol: Layout, Module, ECC-200     | offen    |     |                          |
| 10  | Datamatrix selbst zeichnen / decodieren        | offen    |     |                          |

## Verzeichnisstruktur

```
.
├── README.md                       ← diese Datei
├── markdown/                       ← Quellen der Tageshefte (Single Source of Truth)
│   ├── tag1_pruefziffern.md
│   ├── tag2_isbn_luhn_hamming.md
│   ├── tag3_hamming_code.md
│   └── tag4_secded_crc_interleaving.md
├── vorlage/                        ← LaTeX-Vorlage und Build-Hilfsskript
│   ├── vorlage_koma.tex            (KOMA-Script-basiertes Layout mit Marginalien)
│   └── marginalien_postprocess.py  (wandelt Aufgaben-Headings in Marginalien-Marker)
├── build/                          ← Build-Skripte
│   └── build.sh                    (baut ein einzelnes Heft oder alle)
├── doku/                           ← Redaktionelle Dokumentation
│   ├── schreibstil.md              (Tonalität, Sprache, didaktische Prinzipien)
│   ├── inhaltsplan.md              (Detailskizze Tag 5–10, Lernziele, Übergänge)
│   ├── zielpublikum.md             (Wer ist Greta, was kann sie, was nicht)
│   ├── layout-konzept.md           (aktuelles Layout, geplante Erweiterungen)
│   ├── feedback-greta.md           (gesammeltes Feedback, leer / wachsend)
│   └── claude-code-prompt.md       (Vorschlag, wie man Claude Code prompten kann)
├── layout-konzepte/                ← PDFs zu Layout-Iterationen (Diskussionsmaterial)
│   └── marginalien_doppelseitig.pdf
└── referenz-pdfs/                  ← Aktueller Output zu Vergleichszwecken
    ├── tag1_pruefziffern.pdf
    ├── tag2_isbn_luhn_hamming.pdf
    ├── tag3_hamming_code.pdf
    └── tag4_secded_crc_interleaving.pdf
```

## Der Wechsel zu Claude Code – warum

Das Projekt ist groß genug geworden, dass es ein **echtes Buchprojekt** werden soll. Das bedeutet:

- Versionskontrolle (Git) statt PDFs in einem Cloud-Ordner
- Inkrementelle Builds (Makefile)
- Mittelfristig: Wechsel von Markdown zu nativ LaTeX (für bessere Querverweise, Index, Glossar, automatische Nummerierung – wichtig spätestens ab Tag 5, wenn die Mathematik dichter wird)
- Möglichkeit, dass der Nutzer auch zwischen Sessions selbst Hand anlegt

## Geplante Migration nach LaTeX

Aktuell: **Markdown → pandoc → LaTeX-Body → Postprozessor → xelatex → PDF**

Geplant (in Claude Code):

1. Pandoc nutzen, um die vier vorhandenen Markdown-Dateien als Startpunkt nach LaTeX zu konvertieren
2. Buchstruktur einführen: `\documentclass{scrbook}`, `\chapter{...}` pro Tag, `\include{tag1}` etc.
3. Eigene Befehle in `befehle.tex` definieren: `\bleistiftuebung{nr}{titel}`, `\pythoneinheit{nr}{titel}`, `\werkzeugcheck{titel}` (ersetzen heutige Marginalien-Logik)
4. Lösungen aus den einzelnen Tagen herauslösen und in einen gemeinsamen Anhang (`anhang_loesungen.tex`) verschieben, mit Querverweisen
5. Index und Glossar hinzufügen (`makeindex`, `glossaries`-Paket)
6. Doppelseitiges Layout final umsetzen (siehe `layout-konzepte/marginalien_doppelseitig.pdf`)

## Schnelleinstieg für einen neuen Claude

1. Lies `doku/zielpublikum.md` (eine Seite, definiert Greta)
2. Lies `doku/schreibstil.md` (zwei Seiten, definiert die Tonalität)
3. Lies `doku/inhaltsplan.md` (definiert, was inhaltlich noch ansteht)
4. Schau in eines der Markdown-Dokumente (z. B. `markdown/tag3_hamming_code.md`), um den Stil zu sehen
5. Schau ins zugehörige PDF in `referenz-pdfs/`, um den Output zu sehen
6. Ab dann: legen wir los.

## Build (aktuell)

Im Verzeichnis `build/`:

```bash
./build.sh tag3   # baut nur Tag 3
./build.sh all    # baut alle vier Tage
```

Voraussetzungen: `pandoc`, `xelatex`, `python3`, DejaVu-Fonts. Siehe `build/build.sh`.

## Wer entscheidet was?

- **Inhaltliche Stoffauswahl** (was wird in welchem Tag behandelt): Onkel/Nutzer entscheidet, Claude schlägt vor.
- **Didaktische Reihenfolge und Tempo:** Claude schlägt vor, Onkel/Nutzer korrigiert anhand von Greta-Feedback.
- **Schreibstil und Wortwahl:** Claude schreibt, Onkel/Nutzer redigiert.
- **Layout und Build:** Claude implementiert, Onkel/Nutzer entscheidet das große Bild.
- **Greta-Feedback:** wandert in `doku/feedback-greta.md`, wird vor jeder neuen Tagesplanung konsultiert.
