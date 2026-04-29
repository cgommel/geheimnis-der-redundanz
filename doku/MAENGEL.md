# Mängel- und Vorschlagsliste

> Sammlung aller Punkte, die im Polish- und Review-Sprint abzuarbeiten
> sind. Pro Punkt: kurze ID, Kategorie, Schweregrad, Verortung,
> Beschreibung, ggf. Lösungsidee. Erst sammeln, dann systematisch
> umsetzen — keine spontanen Hotfixes ohne Eintrag.

## Status

- 🟥 offen
- 🟧 in Arbeit
- 🟩 erledigt (kann nach erledigtem Polish-Sprint archiviert werden)

## Layout

### LY-01 — Marginalie verwaist nach Page-Break 🟩
- **Schwere**: hoch (User: „sowas geht gar nicht")
- **Stelle**: Tag 6, Bleistiftübung 1 („Polynome rechnen.") — Übergang
  in der Nähe von Seite 52 → 53. Vermutlich auch an anderen Stellen
  möglich, wenn knapp.
- **Befund**: die Marginalie „Bleistift-Übung 1" landet im
  Marginalbereich der \emph{vorigen} Seite, während der zugehörige
  Aufgaben-Block (Titel „Polynome rechnen." plus farbiger Strich) erst
  auf der nächsten Seite anfängt. Optisch zerrissen.
- **Ursache (Vermutung)**: in der `aufgabe`-Umgebung wird `\marginpar`
  vor `\begin{aufgabebox}` emittiert; LaTeX bricht zwischen
  Marginalie und Box auf eine neue Seite um.
- **Lösungsidee**: entweder die `\marginpar`-Ausgabe an den ersten
  Inhalt der tcolorbox koppeln (zum Beispiel via `before upper` oder
  `attach boxed title`), oder `\nopagebreak[4]` zwischen Marginpar
  und Boxbeginn, oder den ganzen Aufgaben-Header per `\samepage` oder
  `\needspace{...}` zusammenhalten.

### LY-02 — ASCII-Diagramm EAN-13 sollte TikZ werden 🟥
- **Schwere**: mittel
- **Stelle**: Tag 1, Block „EAN-13 — Prüfziffern aus dem echten Leben"
- **Befund**: das Diagramm
  ```
  4 0 0 6 3 8 1 3 3 3 9 3 1
  └────── 12 Datenziffern ──────┘ │
                                  Prüfziffer
  ```
  liegt als `verbatim`-Block. Die Box-Drawing-Glyphen (`└─┘│`) und
  der ASCII-Pipe `│` alignen visuell nicht zuverlässig; das `│` für
  die Prüfziffer steht nicht bündig unter der 13. Ziffer.
- **Lösungsidee**: TikZ-Diagramm mit echter geschweifter Klammer
  unter den 12 Datenziffern und einem Pfeil zur Prüfziffer.

### LY-03 — Quote-vor-Konsonant: Leerzeichen wirkt verschluckt 🟥
- **Schwere**: niedrig (Polish)
- **Stelle**: Vorwort (eine Stelle bereits umformuliert: „wie
  installiere ich Thonny?" hängst → „beim Installieren von Thonny
  stecken bleibst"). Verdacht auf weitere Stellen.
- **Befund**: nach Unicode-`"` (U+201D, schließendes deutsches
  Anführungszeichen) wirkt das Leerzeichen optisch zu klein, manchmal
  verschwindet es ganz. Liegt an DejaVu-Serif-Glyph-Kerning oder
  Microtype-Interaktion.
- **Lösungsidee**: bei Bedarf `\,` (kleines Leerzeichen) einsetzen
  oder umformulieren. Generelle Sweep über alle Quote-Vorkommen.

### LY-05 — Tabelle ragt aus Aufgabenblock heraus 🟥
- **Schwere**: hoch (sichtbar im PDF, Strich-Block wird verletzt)
- **Stelle**: `tag2.tex`, Bleistiftübung 7 („Anwenden"), Tabelle
  „Code | Mindestdistanz | Fehler erkennbar | Fehler korrigierbar"
- **Befund**: aus dem Build-Log: `Overfull \hbox (72.71155pt too
  wide) in paragraph at lines 456--466`. Die Tabellen-Überschriften
  sind zu lang für die schmalere Aufgabenblock-Spalte; eine ganze
  Tabelle ragt 7\,cm rechts in den Marginalbereich.
- **Lösungsidee**: Spaltenüberschriften abkürzen („Mindestdist.",
  „Erkennbar", „Korrigierbar") oder Tabelle drehen (Codes als
  Spalten, Eigenschaften als Zeilen).

### LY-06 — hyperref kann Mathe in Section-Titeln nicht ⌬ 🟥
- **Schwere**: kosmetisch beim Build (102 Warnungen), bei
  PDF-Bookmarks sichtbar
- **Stelle**: alle Tag-Kapitel; Section-Titel der Form
  `\section{... ($\approx$ N min)}`
- **Befund**: 102×
  `Package hyperref Warning: Token not allowed in a PDF string
  (Unicode): removing 'math shift' / '\approx'`. PDF-Bookmarks zeigen
  „X.Y Titel ( N min)" ohne `≈`-Symbol.
- **Lösungsidee**: `\texorpdfstring{$\approx$}{≈}` für Bookmarks,
  oder eigener Befehl `\sectionmitzeit{Titel}{Zeitangabe}`, der das
  Bookmark sauber setzt (deckt LY-04 mit ab).

### LY-07 — Underfull \vbox while output active (6×) 🟥
- **Schwere**: niedrig
- **Befund**: 6 Stellen im Log mit
  `Underfull \vbox (badness 10000) has occurred while \output is
  active`. Page-Break setzt mit unsauberem Vertikal-Spacing.
- **Verwandt mit**: LY-01 (Marginalie verwaist nach Break) — gleiche
  Wurzel: knappe Aufgabenblöcke nahe Page-Bottom.

### LY-08 — Underfull \hbox, badness > 1000 (12×) 🟥
- **Schwere**: niedrig (Microtype-Polish)
- **Befund**: 12 Zeilen mit suboptimaler Wortverteilung, höchste
  Badness 4024 (`tag6.tex` lines 70--72) und 10000 (lines 203--205).
- **Lösungsidee**: gezielte `\hyphenation{...}`-Einträge oder
  Umformulierung der jeweiligen Sätze. Erst nach Ende der inhaltlichen
  Migration angehen, weil sich Zeilenfälle bei jeder Textänderung
  verschieben.

### LY-09 — Glossar: Overfull bei „Einzelfehler-Korrektur" 🟥
- **Schwere**: niedrig (4,11 pt zu breit)
- **Stelle**: Glossar-Eintrag „Hamming-Schranke", String
  „Einzelfehler-Korrektur" wird nicht getrennt
- **Lösungsidee**: `\hyphenation{Ein-zel-feh-ler-Kor-rek-tur}` oder
  expliziter Bindestrich-Bruch.

### LY-10 — glossaries: tracklang-Warnung für ngerman 🟥
- **Schwere**: kosmetisch, möglicherweise Sortier-Effekt
- **Befund**: `Package tracklang Warning: No 'datatool' support for
  dialect 'ngerman'`. glossaries-extra fällt auf Default-Sortierung
  zurück; deutsche Umlaut-Sortierung könnte abweichen.
- **Lösungsidee**: `\usepackage[ngerman]{glossaries-extra-bib2gls}`
  oder `sort=de` Option auf einzelne Einträge mit Umlauten
  (z.\,B.\ Auslöschung, Bündelfehler, Übertragung).

### LY-11 — Unused option `headings` 🟥
- **Schwere**: kosmetisch
- **Stelle**: `buch.tex` `\documentclass[…, headings=normalsize, …]`
- **Befund**: `LaTeX Warning: Unused global option(s): [headings]`.
  scrbook erwartet `headings=` zur Klassen-Zeit, das war unsere
  Schreibweise; aber KOMA übernimmt scheinbar die Form anders.
- **Lösungsidee**: in `\KOMAoptions{headings=…}` übersetzen oder
  einfach entfernen.

### LY-12 — DejaVu Serif hat keine echten Kapitälchen 🟥
- **Schwere**: kosmetisch (unsichtbar bisher, weil Fallback brauchbar
  aussieht)
- **Befund**: `LaTeX Font Warning: Font shape 'TU/DejaVuSerif(0)/m/sc'
  undefined ... using 'TU/DejaVuSerif(0)/m/n' instead` (4×). Wir
  nutzen `\textsc{...}` in den Marginalien-Bezeichnungen
  („Bleistift-Übung 1" usw.); LaTeX fällt auf den Standardschnitt
  zurück — also keine echten Kapitälchen.
- **Lösungsidee**: entweder andere Schrift mit `\setmainfont[…SmallCaps…]`
  per fontspec, oder einen eigenen Befehl `\fakesmallcaps{...}`, der
  via `\MakeUppercase` plus reduzierter Schriftgröße simuliert. Dritte
  Option: für die Marginalie auf `\textsc` ganz verzichten und stattdessen
  „Bleistift-Übung 1" einfach in `\textit` oder `\sffamily` setzen.

### LY-13 — Detail-Lokalisierung der Underfull-/Overfull-Stellen 🟥
- **Schwere**: Polish (Sammelpunkt für LY-08 und LY-09)
- **Befund**: Log-Liste mit relativen Zeilennummern, aber ohne klaren
  Datei-Verweis (außer für die zwei bekannten Overfulls). Höchste
  Badness 10000 in einer Underfull-Box (lines 203--205 — Datei zur
  Zeit unklar) und 4024 (lines 70--72).
- **Lösungsidee**: bei der Microtype-Polish-Phase pro Eintrag über
  die `[N]`-Page-Marker im Log auf die Datei zurückrechnen, dann
  vor Ort umformulieren oder `\hyphenation`-Hilfe einsetzen.

### LY-04 — Section-Titel mit `\normalfont`-Zeitangabe 🟥
- **Schwere**: kosmetisch
- **Stelle**: alle Tag-Kapitel, z. B. „1.3 Das Paritätsbit — die
  einfachste Erkennung (≈ 45 min)"
- **Befund**: aktuell als
  `\section{... \normalfont(\textit{$\approx$ 45 min})}` gesetzt. Sieht
  funktional aus, aber typografisch eher Werkstatt-Zustand.
- **Lösungsidee**: eigener Befehl `\sectionmitzeit{Titel}{Zeitangabe}`,
  der die Zeitangabe konsistent rendert (z. B. kleiner, eingerückt,
  oder als Marginalie).

## Inhalt

*(noch leer — wird beim minutiösen Buch-Review gefüllt)*

## Code

*(noch leer)*

## Toolchain / Build

*(noch leer)*

## Doku

*(noch leer)*
