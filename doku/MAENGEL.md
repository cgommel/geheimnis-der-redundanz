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

### LY-01 — Marginalie verwaist nach Page-Break 🟥
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
