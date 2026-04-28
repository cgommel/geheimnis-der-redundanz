# Work in Progress

> Aktueller Arbeitsstand auf `feature/latex-native`. Kurzer Schnappschuss,
> damit die Arbeit nach einer Pause wieder schnell aufgenommen werden kann.

## Stand

Branch: `feature/latex-native`

| Phase | Schritt | Status |
|-------|---------|--------|
| Phase 0 | Build-Reparatur, GitHub-Repo, Layout-Briefing | ✅ |
| Phase 1, M1 | LaTeX-Skelett & Layout (scrbook, tcolorbox) | ✅ |
| Phase 1, M2 | Python-Snippet-Infrastruktur (minted, Region-Marker) | ✅ |
| Phase 1, M3 | Tag 3 migriert | ✅ |
| Phase 1, M4 | Tag 1, 2, 4 migriert | ✅ |
| Phase 1, M5 | Lösungen herauslösen, `\autoref` | ⬜ |
| Phase 1, M6 | Glossar & Index | ⬜ |
| Phase 1, M7 | Front-/Back-Matter | ⬜ |
| Phase 1, M8 | Aufräumen, Merge nach `main` | ⬜ |
| Phase 2 | Container-Migration | ⬜ |
| Phase 3 | CI/Release | ⬜ |

## Aktueller Stand des Buchs

- 59 Seiten Gesamtbuch (`pdf/latex/buch.pdf`)
- Alle vier vorhandenen Tage inhaltlich migriert
- Lösungen vorerst noch innerhalb der jeweiligen Kapitel (M5 lagert sie aus)
- Layout, Marginalien, Code-Highlighting, Region-basierte Snippets, Recto/Verso-Spiegelung — alles funktioniert

## Nächster Schritt: Tag 5 importieren

`import/files.zip` (unversioniert!) enthält das Tag-5-Material. Vorgehen:
1. Entpacken nach `import/tag5/` o.\ä.
2. Sichten — Markdown? LaTeX-Vorentwurf? Andere Form?
3. Inhalt migrieren: `latex/kapitel/tag5.tex` neu, Code-Snippets nach `latex/code/tag5/`
4. `buch.tex` um `\include{kapitel/tag5}` erweitern
5. `doku/inhaltsplan.md` aktualisieren, falls nötig
6. Build testen, A/B-Vergleich nicht mehr möglich (kein altes PDF), aber Plausibilitätscheck

## Stolperfallen für Folgemigrationen

- **Anführungszeichen:** `babel[ngerman]` macht aus `"u` ein `ü`. Vor jedem Build:
  `grep '"' latex/kapitel/tagN.tex` und ASCII-`"` durch Unicode-`"` ersetzen.
  ABER: in `\begin{verbatim}`-Blöcken (Code-Beispiele wie `print("Hallo Greta")`)
  müssen die Quotes ASCII bleiben, sonst tippt Greta etwas Falsches ab.
  → Nach `replace_all` immer Verbatim-Stellen kontrollieren.
- **Tabellen:** Standardmäßig `lll`-Spalten brechen aus dem Aufgabenblock heraus,
  wenn Inhalt zu lang. Bei textlastiger letzter Spalte: `p{Xcm}` verwenden.
- **`\checkmark`** braucht `amssymb` (in Präambel geladen).
- **`\write18`-Snippets** brauchen das Verzeichnis `latex/.snippets/`, das das
  Makefile-Target `buch` per `mkdir -p` anlegt.

## Lokale Voraussetzungen

```bash
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   collection-latexextra
brew install --cask font-dejavu
brew install pygments
```

Im Container-Schritt (Phase 2) wandert das alles ins Dockerfile.
