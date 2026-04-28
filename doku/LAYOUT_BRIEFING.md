# Layout-Experiment: Was wir am Ende wollen

> Briefing-Dokument für Claude Code. Beschreibt das **finale Layout-Konzept**, das in einer mehrstufigen Iteration in Claude Chat erarbeitet wurde. Enthält alle Entscheidungen, ihre Begründung und die LaTeX-Bausteine, die das Konzept umsetzen. Soll als Referenz dienen, wenn das aktuelle einseitige Layout (`vorlage_koma.tex`) nach LaTeX migriert und auf doppelseitig umgestellt wird.

## Status

- **Aktuell** (Tag 1–4 als PDF): einseitig, Marginalien rechts, ohne farbige Striche. Funktioniert, ist aber nicht das Zielbild.
- **Ziel:** doppelseitig, Marginalien und farbige Aufgaben-Striche immer **außen** (auf Recto rechts, auf Verso links), Pastellfarben pro Aufgabentyp.

## Demo-PDF

Die finale Variante ist als Demo-PDF im Repo:
`layout-konzepte/marginalien_doppelseitig.pdf`

Beim Öffnen sieht man auf Seite 1 die Recto-Variante (Marginalie und Strich rechts), auf Seite 2 die Verso-Variante (beides links spiegelverkehrt). Die zwei Seiten zusammen entsprechen einem aufgeschlagenen Heft.

---

## Iterationsverlauf (verkürzt)

Damit Kontext klar ist, hier die Zwischenstände – jeder hat etwas zum finalen Konzept beigetragen:

1. **Marginalien als Konzept** wurde eingeführt, weil das Heft zu viele identisch aussehende Aufgaben-Überschriften hatte. Die Aufgabentypen (Bleistift/Python/Werkzeug) sollen am Rand erkennbar sein, nicht im Text-Fluss.
2. **Erster Versuch:** Marginalien rechts, kein Strich am Aufgabentext. Problem: die Marginalie war vertikal nicht mit dem Aufgabenblock bündig (saß zu hoch).
3. **Vier Block-Markierungs-Varianten** wurden verglichen: dünner grauer Rahmen, farbiger Rahmen, Pastell-Hintergrund, dünner farbiger Strich am linken Rand. Gewählt wurde die **Strich-Variante**, weil sie dezent ist, aber den Aufgabenblock klar abgrenzt.
4. **Drei Farb-Sets** wurden gegenübergestellt (kräftig, gedämpft, hell). Gewählt wurde **Farbset 3 (hell/pastell)**, weil es im Vergleich zu „rostig" und „dumpf" am freundlichsten wirkt.
5. **Strich auf Außenseite:** Erst stand der Strich links, das wirkte unausgewogen. Mit Strich rechts und Marginalie auf derselben Seite entstand eine klare „Seitenrand-Einheit". 
6. **Doppelseitiges Layout:** Damit Strich und Marginalie *immer* außen liegen (auch im gedruckten Heft), wurde auf `twoside` umgestellt. Auf Recto-Seiten (ungerade): außen = rechts. Auf Verso-Seiten (gerade): außen = links.
7. **Vertikales Alignment** war über alle Iterationen ein wiederkehrender Reibungspunkt – das Symbol stand zu hoch oder zu tief verglichen mit der ersten Zeile der Aufgabenbox. Finale Lösung: `\vspace*{12pt}` als manuelle Korrektur am Anfang der Marginalie.
8. **Marginalie näher an den Strich:** `marginparsep` reduziert von 0,5 cm auf 0,15 cm, sodass Marginalie und Strich praktisch eine Einheit bilden.

## Designentscheidungen im Überblick

### Layout-Geometrie

```
Klasse:                scrartcl (oder später scrbook)
Optionen:              11pt, a4paper, twoside

Geometrie:
  inner=2.5cm
  outer=4.5cm
  top=2.0cm
  bottom=2.5cm
  marginparwidth=2.7cm   (etwas schmaler als beim aktuellen 3.0cm)
  marginparsep=0.15cm    (sehr eng, Marginalie nahe am Strich)
```

**Konsequenz:** Die Hauptspalte ist enger als beim aktuellen Layout, was die Lesbarkeit verbessert (klassische Faustregel: 60-70 Zeichen pro Zeile). Auf der Außenseite entsteht eine breite Marginalspalte mit Strich + Symbol + Bezeichnung.

### Schriften (unverändert vs. aktuell)

```
Haupt:    DejaVu Serif, Scale=0.95
Sans:     DejaVu Sans,  Scale=0.95
Mono:     DejaVu Sans Mono, Scale=0.85
Marker:   DejaVu Sans (für Symbole ✏ ⌨ ⚙)
microtype für Laufweiten
```

### Aufgabentypen und ihre Farben (Farbset 3)

```latex
\definecolor{cBleistift}{RGB}{235, 160, 80}     % helles Orange
\definecolor{cPython}   {RGB}{ 95, 140, 180}    % sanftes Blau
\definecolor{cWerkzeug} {RGB}{185, 200, 110}    % helles Lindgrün
```

Diese drei Farben werden konsequent verwendet:
- für den **Strich** am Aufgabenblock (`borderline east` oder `borderline west`)
- für das **Symbol** in der Marginalie
- für die **Kapitälchen-Bezeichnung** unter dem Symbol

### Marginalien-Inhalt

Drei Zeilen, vertikal angeordnet:

```
✏              ← großes Symbol (24pt), in der Aufgaben-Farbe
Bleistift-     ← Bezeichnung Zeile 1 in Kapitälchen
Übung 3        ← Bezeichnung Zeile 2 in Kapitälchen, mit Nummer
```

Das Symbol kommt aus DejaVu Sans, das die Unicode-Codepoints U+270F (✏), U+2328 (⌨) und U+2699 (⚙) nativ rendert. Keine Color-Emoji-Fonts nötig.

### Aufgaben-Strich

Ein einzelner farbiger Strich am Außenrand des Aufgabentextblocks, 2,5 pt stark, vertikal über die Höhe des Blocks.

Auf **Recto-Seiten** (ungerade Seitenzahl): Strich auf der rechten Seite des Blocks.
Auf **Verso-Seiten** (gerade Seitenzahl): Strich auf der linken Seite des Blocks.

Innenabstände im Block: 4 pt zur Strich-Seite, 12 pt zur Innenseite (sodass der Aufgabentext etwas Luft zwischen sich und dem Strich hat).

---

## LaTeX-Bausteine (vollständig)

Diese Bausteine sind in mehreren Iterationen entstanden und in einem Demo-Dokument getestet. Sie sollen als Vorlage für die LaTeX-Migration dienen.

### Präambel-Pakete

```latex
\documentclass[11pt, a4paper, twoside]{scrartcl}

\usepackage[a4paper,
            inner=2.5cm, outer=4.5cm,
            top=2.0cm, bottom=2.5cm,
            marginparwidth=2.7cm, marginparsep=0.15cm]{geometry}

\usepackage{fontspec}
\setmainfont{DejaVu Serif}[Scale=0.95]
\setsansfont{DejaVu Sans}[Scale=0.95]
\setmonofont{DejaVu Sans Mono}[Scale=0.85]
\newfontfamily\markerfont{DejaVu Sans}

\usepackage[ngerman]{babel}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{changepage}
```

### Farb-Definitionen

```latex
\definecolor{cBleistift}{RGB}{235, 160, 80}
\definecolor{cPython}   {RGB}{ 95, 140, 180}
\definecolor{cWerkzeug} {RGB}{185, 200, 110}
```

### Zwei tcolorbox-Varianten (Strich rechts vs. links)

```latex
\newtcolorbox{aufgabeRecto}[1]{%
  enhanced, breakable,
  colback=white, colframe=white,
  boxrule=0pt, arc=0pt, outer arc=0pt,
  left=4pt, right=12pt, top=4pt, bottom=4pt,
  boxsep=0pt,
  borderline east={2.5pt}{0pt}{#1},
  before skip=0.6em, after skip=0.6em,
}

\newtcolorbox{aufgabeVerso}[1]{%
  enhanced, breakable,
  colback=white, colframe=white,
  boxrule=0pt, arc=0pt, outer arc=0pt,
  left=12pt, right=4pt, top=4pt, bottom=4pt,
  boxsep=0pt,
  borderline west={2.5pt}{0pt}{#1},
  before skip=0.6em, after skip=0.6em,
}
```

### Marginalien-Inhalte für Recto und Verso

Wichtig: auf Verso-Seiten ist der Inhalt rechtsbündig (bündig zum Strich, der dann links sitzt), auf Recto-Seiten linksbündig. Das `\vspace*{12pt}` ist die manuelle vertikale Korrektur, damit das Symbol mit der ersten Zeile der Aufgabenbox horizontal fluchtet (kompensiert das `before skip` und `top` der tcolorbox).

```latex
\newcommand{\markercontentVerso}[4]{%
  \vspace*{12pt}\raggedleft\color{#4}%
  {\markerfont\fontsize{24}{26}\selectfont #1}\\[0.05em]
  {\small\textsc{#2}}\\
  {\small\textsc{#3}}%
}

\newcommand{\markercontentRecto}[4]{%
  \vspace*{12pt}\raggedright\color{#4}%
  {\markerfont\fontsize{24}{26}\selectfont #1}\\[0.05em]
  {\small\textsc{#2}}\\
  {\small\textsc{#3}}%
}
```

### Page-aware Aufgaben-Umgebung

Diese Umgebung wählt anhand der Seitenparität automatisch die richtige Box-Variante und gibt für `\marginpar` *beide* Inhaltsvarianten an, sodass LaTeX selbst die richtige Seite wählen kann.

```latex
\makeatletter
\newenvironment{aufgabe}[4]%
  {% #1=symbol, #2=label1, #3=label2, #4=farbe
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
  }
  {%
   \expandafter\end\expandafter{\@aktbox}%
  }
\makeatother
```

### Komfort-Wrapper für die drei Aufgabentypen

Diese drei Befehle sind das, was im Markup tatsächlich verwendet wird. Sie kapseln die `aufgabe`-Umgebung mit den passenden Symbolen, Bezeichnungen und Farben.

```latex
\newenvironment{bleistiftuebung}[2]%
  {\begin{aufgabe}{✏}{Bleistift-}{Übung #1}{cBleistift}\textbf{#2.\par}}
  {\end{aufgabe}}

\newenvironment{pythoneinheit}[2]%
  {\begin{aufgabe}{⌨}{Python-}{Einheit #1}{cPython}\textbf{#2.\par}}
  {\end{aufgabe}}

\newenvironment{werkzeugcheck}[1]%
  {\begin{aufgabe}{⚙}{Werkzeug-}{Check}{cWerkzeug}\textbf{#1.\par}}
  {\end{aufgabe}}
```

(Die `\textbf{...}` für den Aufgabentitel ist eine Konvention: der erste Satz der Aufgabe wird fett gesetzt, dann normaler Text.)

### Verwendung im Dokument

```latex
\begin{bleistiftuebung}{1}{Wiederholung als Code}
Welche der folgenden empfangenen Dreierblöcke werden korrekt zu 0 oder 1
zurückübersetzt? \texttt{111}, \texttt{010}, \texttt{001}, \texttt{110},
\texttt{000}, \texttt{101}.

Wie viele Bitfehler pro Dreierblock kann das Verfahren korrigieren?
\end{bleistiftuebung}

\begin{pythoneinheit}{1}{Paritätsprüfer bauen}
Lege in Thonny eine neue Datei an und tippe diesen Code ab:

\begin{verbatim}
def paritaetsbit(daten):
    return sum(daten) % 2
\end{verbatim}
\end{pythoneinheit}

\begin{werkzeugcheck}{Thonny einrichten}
Lade Thonny von thonny.org herunter und installiere es.
\end{werkzeugcheck}
```

---

## Was beim Migrieren zu beachten ist

### Kompatibilität mit der aktuellen Markdown-Quelle

Der aktuelle Postprozessor `marginalien_postprocess.py` macht aus

```markdown
### ✏️ Bleistiftübung 1 – Wiederholung als Code
```

dann

```latex
\bleistiftuebung{1}{Wiederholung als Code}
```

Das ist ein **einfacher Befehl**, keine Umgebung. In der LaTeX-Migration wird es eine **Umgebung** (`\begin{bleistiftuebung}{1}{Titel} ... \end{bleistiftuebung}`), damit der Aufgabentext im Strich-Block steht.

Der Postprozessor müsste also angepasst werden, oder – besser – die Markdown-Quelle wird Schritt für Schritt zu LaTeX migriert.

### Reihenfolge der Migration

Empfohlen:

1. Layout-Bausteine in eine **neue** Vorlage `vorlage_koma_v2.tex` einbauen (alte Vorlage bleibt liegen).
2. Mit *einem* Tag testen (z. B. Tag 3, weil er das Venn-Diagramm hat und damit ein nicht-trivialer Testfall ist).
3. Vertikales Alignment final justieren – der Wert `\vspace*{12pt}` ist empirisch ermittelt und kann je nach Schriftgröße/Box-Padding nachjustiert werden müssen.
4. Vergleich mit dem Demo-PDF aus `layout-konzepte/`.
5. Wenn ok: alle vier Tage migrieren.
6. Erst danach in den Hauptkörper-Migrationsschritt (`scrbook`-Klasse, `\chapter` pro Tag, Anhang für Lösungen) übergehen.

### Was *nicht* übernommen werden soll

- Die Idee aus einer früheren Iteration, die Marginalie mit einem Trennstrich oben oder einem Kasten zu versehen (Varianten 1–3 aus der Iteration vor dem Strich-Konzept). Die wurden explizit verworfen.
- Kräftige Farben (Farbset 1) – wirken zu „rostig", besonders das Orange.
- Volle farbige Rahmen um die Aufgabe – wirken zu schwer.
- Pastell-Hintergrund – wird zu bunt, wenn mehrere Aufgaben kurz hintereinander stehen.

### Bekannte Stolperfallen

- `\marginpar` und `tcolorbox` zusammen: das `\marginpar` muss *vor* der tcolorbox-Umgebung stehen, sonst funktioniert die vertikale Anker-Logik nicht. Genau das macht die `aufgabe`-Umgebung oben.
- `\reversemarginpar` plus `marginnote` ist fragil. Stattdessen `\marginpar[verso]{recto}` mit zwei Inhalten – das ist robust und gut dokumentiert.
- `changepage`'s `\checkoddpage` muss vor jedem `\ifoddpage` neu aufgerufen werden, sonst ist die Information stale.

---

## Test-Szenarien

Wenn das neue Layout fertig ist, sollten folgende Fälle funktionieren:

1. **Eine Aufgabe pro Aufgabentyp** auf einer Seite, alle drei Symbole sichtbar.
2. **Aufgabe geht über Seitenumbruch** (`breakable` in tcolorbox), Strich setzt sich fort, Marginalie nur am Anfang.
3. **Aufgabe enthält Code-Block** mit `\begin{verbatim}`. Der Block muss im Strich-Block bleiben und die Strich-Linie muss durchgehend sein.
4. **Recto-/Verso-Wechsel mitten im Tag**: nach einem `\clearpage` muss die nächste Aufgabe automatisch die Spiegelvariante bekommen.
5. **Erste Aufgabe ganz oben auf der Seite**: vertikales Alignment darf nicht durch das fehlende vorhergehende Element gestört werden.

Punkt 5 ist erfahrungsgemäß der Schwierigste – beim Vorgehen empirisch testen.
