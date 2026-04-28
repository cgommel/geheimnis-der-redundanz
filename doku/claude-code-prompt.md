# Hinweis für den Wechsel zu Claude Code

Diese Datei beschreibt, wie du Claude Code einsetzen kannst, sobald du das Projekt importiert hast.

## Zuerst: das Repo aufsetzen

1. ZIP entpacken in einen Ordner deiner Wahl, z. B. `~/projekte/redundancy-book/`
2. Git-Repo initialisieren:
   ```bash
   cd ~/projekte/redundancy-book
   git init
   git add .
   git commit -m "Initial import: Tag 1-4 als Markdown, Vorlage, Doku"
   ```
3. Build einmal lokal laufen lassen, um zu prüfen, dass die Toolchain funktioniert:
   ```bash
   ./build/build.sh tag1
   ```
   Erwartet: `pdf/tag1_pruefziffern.pdf` wird erzeugt. Voraussetzung sind:
   - `pandoc`
   - eine TeX-Distribution mit `xelatex` (auf macOS: MacTeX; auf Linux: texlive-xetex, texlive-latex-extra, texlive-fonts-recommended, texlive-lang-german, texlive-pictures, texlive-science, ggf. cm-super)
   - Python 3
   - DejaVu-Fonts (auf den meisten Linux-Distributionen vorinstalliert; macOS: über Homebrew `brew install --cask font-dejavu` oder als TTF-Download)

4. Claude Code starten und den Workspace öffnen.

## Erster Prompt für Claude Code

Hier ist ein Vorschlag für einen ersten Prompt — du kannst ihn verwenden oder anpassen:

> ```
> Hallo Claude. Ich übergebe dir hier ein Buchprojekt namens
> "Das Geheimnis der Redundanz – Von der Prüfziffer zum Datamatrix".
> Es ist aus einer langen Konversation in Claude Chat hervorgegangen.
> Die didaktische Klammer: das Buch begleitet meine Nichte Greta (10.
> Klasse Gymnasium) in einem zweiwöchigen Praktikum von einfachen
> Prüfziffern bis zum Datamatrix-Code (Reed-Solomon).
>
> Bitte mach dich zuerst mit dem Projekt vertraut, indem du in dieser
> Reihenfolge liest:
>
> 1. README.md (Projektübersicht)
> 2. doku/zielpublikum.md (wer ist Greta)
> 3. doku/schreibstil.md (Tonalität)
> 4. doku/inhaltsplan.md (was kommt noch)
> 5. doku/layout-konzept.md (Layout-Stand und -Plan)
> 6. doku/feedback-greta.md (was wir bisher von ihr wissen)
> 7. eines der Markdown-Hefte als Beispiel, z.B. markdown/tag3_hamming_code.md
>
> Schau dir auch das zugehörige PDF in referenz-pdfs/ an, damit du
> den Output siehst.
>
> Wenn du das gelesen hast, gib mir bitte:
> 1. Eine Zusammenfassung in 5-10 Sätzen, was du verstanden hast.
> 2. Drei Fragen, die du an mich hast, bevor wir loslegen.
> 3. Einen Vorschlag, womit wir starten sollten — Optionen sind grob:
>    a) LaTeX-Migration der bestehenden vier Tage (vom Markdown weg)
>    b) Tag 5 (endliche Körper) konzipieren und schreiben
>    c) Layout-Migration zum doppelseitigen Setup mit Strich außen
>    d) etwas anderes, das du sinnvoll findest
> ```

## Folge-Prompts: typische Szenarien

### Szenario A: Greta hat Tag 3 durchgearbeitet

> ```
> Greta hat Tag 3 in 2.5 Stunden durchgearbeitet. Sie ist bei der
> Konstruktion des Hamming-Codes (Block 2) ins Stocken geraten,
> insbesondere bei der binären Position-zu-Prüfbit-Zuordnung. Den
> Decoder-Trick (s3 s2 s1 = Fehlerposition) fand sie cool.
>
> Bitte aktualisiere doku/feedback-greta.md entsprechend.
> Überleg dann, ob wir an markdown/tag3_hamming_code.md noch etwas
> anpassen sollten (z.B. mehr Tipps in der Bleistiftübung 2). Wenn
> ja, schlag konkrete Änderungen vor; ich review.
> ```

### Szenario B: Tag 5 schreiben

> ```
> Tag 4 ist soweit ok (Greta noch nicht durch). Lass uns Tag 5
> (endliche Körper) angehen.
>
> Schau in doku/inhaltsplan.md → Tag 5 für die Skizze. Schreib
> bitte zuerst eine Detailskizze (1 Seite, was ist die Dramaturgie,
> welche Aufgaben ungefähr) und stimm sie mit mir ab, BEVOR du das
> Heft komplett ausschreibst.
> ```

### Szenario C: Layout-Migration

> ```
> Lass uns das Layout auf doppelseitig mit Strich außen migrieren,
> wie in doku/layout-konzept.md (Abschnitt 1) beschrieben und in
> layout-konzepte/marginalien_doppelseitig.pdf gezeigt.
>
> Bau die neue Vorlage als vorlage/vorlage_koma_v2.tex auf, lass
> die alte Vorlage erstmal liegen. Bau Tag 3 mit der neuen Vorlage
> und zeig mir das Ergebnis. Wenn ich es freigebe, schalten wir um.
> ```

### Szenario D: LaTeX-Migration starten

> ```
> Wir wechseln jetzt von Markdown zu nativ LaTeX, wie in
> doku/layout-konzept.md (Abschnitt 2-5) beschrieben.
>
> Gehe in zwei Schritten vor:
>
> Schritt 1: Lege ein neues Verzeichnis latex/ an mit:
>   - buch.tex (Master)
>   - befehle.tex (eigene Befehle für Bleistift, Python, Werkzeug)
>   - tag1.tex bis tag4.tex (per pandoc als Startpunkt erzeugt,
>     dann redaktionell überarbeitet)
>   - anhang_loesungen.tex (alle Lösungen herausgelöst und
>     zusammengeführt)
>
> Schritt 2: Build-System anpassen (latexmk statt pandoc+xelatex)
>
> Lass uns mit Schritt 1 für Tag 1 anfangen. Mach einen Commit
> nach jedem sinnvollen Zwischenstand, damit ich mitschauen kann.
> ```

## Wichtige Konventionen für Claude Code

### Git

- Eine Änderung = ein Commit. Aussagekräftige Messages.
- Branchen für größere Umbauten: `feature/latex-migration`, `feature/twoside-layout`.
- Jedes neue Tag-Heft auf einem eigenen Branch entwickeln; erst nach Greta-Feedback in `main` mergen.

### Build vor Commit

- Vor jedem Commit `./build/build.sh all` laufen lassen, um sicherzustellen, dass alles weiterhin baut.
- Falls jemand das Layout ändert: Visual diff der PDFs ist Pflicht (z. B. mit `diff-pdf` oder einfach Augen drauf).

### Regelmäßiges Aufräumen

- `pdf/` ist nicht eingecheckt (siehe `.gitignore` unten); Build-Artefakte werden nie commited.
- Markdown-Dateien sind die Single Source of Truth, solange wir noch in der Markdown-Phase sind. Nach LaTeX-Migration sind die LaTeX-Dateien die Quelle.

### Empfohlene `.gitignore`

```gitignore
# Build-Artefakte
pdf/
*.aux
*.log
*.out
*.toc
*.idx
*.ilg
*.ind
*.glo
*.gls
*.glg
body.tex
main.tex
main.pdf

# OS-Krimskrams
.DS_Store
Thumbs.db
```

## Was Claude Code besser kann als Claude Chat

- **Persistenz:** der Workspace bleibt erhalten, niemand muss „alles neu erklären".
- **Inkrementelles Bauen:** `make tag3` ist deutlich schneller als der Pfad in Claude Chat.
- **Datei-Granularität:** Claude Code kann gezielt einzelne Dateien lesen/schreiben, ohne dass ein Riesen-Kontext nötig ist.
- **Git-Integration:** echte Versionskontrolle, mit Diffs und Rollbacks.
- **Eigene Hand:** du kannst zwischendurch selbst Änderungen machen und Claude Code fragen, was du gemacht hast.

## Was Claude Chat besser kann

- **Bilder anschauen:** Claude Code hat (Stand der Entwicklung) Einschränkungen bei der visuellen Inspektion von PDFs. Wenn du eine Layout-Frage hast, bei der du wirklich sehen musst, wie's aussieht, kann ein kurzer Wechsel zu Claude Chat hilfreich sein. Du kannst das PDF dort hochladen und um Beurteilung bitten.
- **Brainstorming:** Für „lass uns drei Inhaltsskizzen für Tag 6 machen" ist die freie Konversation in Claude Chat geeigneter.
- **Stil-Diskussionen:** Tonalitäts-Justierungen, lange Reflexionen über pädagogische Fragen.

Faustregel: **Engineering und Implementierung in Claude Code, kreative Arbeit und visuelle Beurteilung wahlweise auch in Claude Chat.**
