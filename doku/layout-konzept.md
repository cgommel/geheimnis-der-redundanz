# Layout-Konzept

> Stand des aktuellen Layouts und Plan für die Weiterentwicklung im Rahmen der LaTeX-Migration.

## Aktuelles Layout (Tag 1–4)

- **LaTeX-Klasse:** `scrartcl` (KOMA-Script Article)
- **Einseitig**, A4
- **Geometrie:** inner=2.0 cm, outer=4.5 cm, marginpar 3 cm, marginparsep 0.5 cm
- **Schriften:** DejaVu Serif (Haupt), DejaVu Sans (Marginalien-Symbole), DejaVu Sans Mono (Code)
- **Microtype** für Laufweiten-Optimierung
- **Marginalien** rechts: dezent grau, drei Symbole (✏ Bleistift, ⌨ Tastatur, ⚙ Zahnrad) plus zweizeilige Bezeichnung in Kapitälchen
- **Codeblöcke** mit hellgrauem Hintergrund (Pandoc-Highlighting im Tango-Stil)

Siehe `vorlage/vorlage_koma.tex`.

## Aktuelle Toolchain

```
Markdown
   │
   ▼ pandoc
LaTeX-Body (body.tex)
   │
   ▼ marginalien_postprocess.py
LaTeX-Body mit \bleistiftuebung{}{}, \pythoneinheit{}{} etc.
   │
   ▼ \input{} via main.tex
xelatex
   │
   ▼ (zweimal für Querverweise)
PDF
```

## Geplante Weiterentwicklung (im Rahmen LaTeX-Migration)

### 1. Doppelseitiges Layout mit Marginalien-Strich-Einheit außen

Im Verlauf der Diskussion wurde das **Zielbild** entwickelt und in `layout-konzepte/marginalien_doppelseitig.pdf` festgehalten. Eckdaten:

- `\documentclass[twoside]{scrbook}` (oder weiterhin `scrartcl` mit `twoside`)
- Auf Recto (ungerade Seiten): Marginalie und farbiger Strich der Aufgabenbox **rechts**
- Auf Verso (geraden Seiten): Marginalie und Strich **links**
- Strich- und Marginalien-Position spiegeln sich, sodass beide stets auf der **äußeren** Seite des aufgeschlagenen Hefts sitzen
- Marginalie rückt sehr nah an den Strich (`marginparsep ≈ 0.15 cm`)
- Aufgabenblock wird durch einen 2,5-pt-Strich am Rand (`tcolorbox` mit `borderline east` bzw. `borderline west`) markiert
- Strich-/Marginalien-Farben (Pastell aus Farbset 3 in der Demo):
  - Bleistift: RGB(235, 160, 80) — helles Orange
  - Python: RGB(95, 140, 180) — sanftes Blau
  - Werkzeug: RGB(185, 200, 110) — Lindgrün
- Vertikale Korrektur per `\vspace*{12pt}` am Anfang der `\marginpar`, damit das Symbol bündig mit der ersten Zeile der Aufgabenbox sitzt.

Siehe Demo-PDF und die LaTeX-Quelle aus dem letzten Iterationsschritt (in der Konversationshistorie). Die wichtigen Code-Bausteine:

```latex
\usepackage{changepage}   % für \checkoddpage und \ifoddpage
\usepackage[most]{tcolorbox}

\newtcolorbox{aufgabeRecto}[1]{%
  enhanced, breakable,
  colback=white, colframe=white,
  boxrule=0pt, arc=0pt, outer arc=0pt,
  left=4pt, right=12pt, top=4pt, bottom=4pt,
  borderline east={2.5pt}{0pt}{#1},
  before skip=0.6em, after skip=0.6em,
}
\newtcolorbox{aufgabeVerso}[1]{%
  ...spiegelverkehrt mit borderline west...
}

\newenvironment{aufgabe}[4]{%
  \checkoddpage
  \ifoddpage
    \def\@aktbox{aufgabeRecto}%
  \else
    \def\@aktbox{aufgabeVerso}%
  \fi
  \marginpar[\markercontentVerso{#1}{#2}{#3}{#4}]%
             {\markercontentRecto{#1}{#2}{#3}{#4}}%
  \expandafter\begin\expandafter{\@aktbox}{#4}%
  \ignorespaces
}{%
  \expandafter\end\expandafter{\@aktbox}%
}
```

### 2. Neue Befehlsstruktur (LaTeX statt Markdown-Marker)

Die heute über den Postprozessor injizierten Marginalien-Marker werden zu echten LaTeX-Befehlen:

```latex
\bleistiftuebung{1}{Wiederholung als Code}
   ...Aufgabentext...
\endaufgabe   % oder \end{aufgabe}, je nach Implementierung

\pythoneinheit{1}{Paritätsprüfer bauen}
   ...Aufgabentext, ggf. mit listings/minted-Code...
\endaufgabe

\werkzeugcheck{Thonny einrichten}
   ...Werkzeug-Setup...
\endaufgabe
```

Die Befehle setzen automatisch die Marginalie und die Aufgabenbox.

### 3. Buchstruktur

- `\documentclass[11pt, a4paper, twoside]{scrbook}`
- Ein Master-File `buch.tex` mit Front-Matter (Titel, Inhaltsverzeichnis), Main-Matter (Tag 1 ff.), Back-Matter (Lösungen, Glossar, Index)
- Jeder Tag wird ein **Kapitel** (`\chapter{Tag 1 — Prüfziffern und Fehlererkennung}`)
- Lösungen aus den einzelnen Tagen werden herausgelöst und in den Anhang verschoben (`\appendix` und ein Kapitel `\chapter{Lösungen}`)
- Jede Aufgabe bekommt ein `\label{ueb:tagN:thema}`, der Lösungsanhang verweist mit `\autoref{ueb:tagN:thema}` darauf

### 4. Index, Glossar

- **Glossar** mit `glossaries`-Paket: Begriffe wie *endlicher Körper*, *Bündelfehler*, *Generatorpolynom* werden erstmalig im Text mit `\gls{begriff}` referenziert und im Glossar definiert.
- **Index** mit `imakeidx`: wichtige Konzepte werden mit `\index{Hamming-Distanz}` markiert. Der Index landet im Back-Matter.

### 5. Querverweise

- Wann immer auf einen früheren Inhalt Bezug genommen wird (z. B. „siehe Tag 1, Block 4"), kommt ein klickbarer Querverweis: `\autoref{block:tag1:naive-idee}`.
- Die Lösungen verweisen auf die Aufgabe und umgekehrt: „Lösung zu Aufgabe \ref{ueb:tag3:venn}".

## Was *nicht* geändert werden soll

- **Tonalität und didaktischer Aufbau** der Hefte bleiben unverändert (siehe `schreibstil.md`).
- **Bildmaterial:** Das TikZ-Venn-Diagramm aus Tag 3 ist bereits ein Beispiel, wie wir Diagramme nativ einbinden. Mehr davon, wenn sinnvoll.
- **Codeblöcke:** Pandoc-Style des Code-Highlightings hat sich bewährt.
