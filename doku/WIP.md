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
|         | Page-aware Aufgaben-Strich (Fix nach M4) | ✅ |
| Phase 1, M4½ | Tag 5 importiert und migriert | ✅ |
| Phase 1, M5 | Lösungen herauslösen, `\autoref` | ⬜ |
| Phase 1, M6 | Glossar & Index | ⬜ |
| Phase 1, M7 | Front-/Back-Matter | ⬜ |
| Phase 1, M8 | Aufräumen, Merge nach `main` | ⬜ |
| Phase 2 | Container-Migration | ⬜ |
| Phase 3 | CI/Release | ⬜ |

## Aktueller Stand des Buchs

- 74 Seiten Gesamtbuch (`pdf/latex/buch.pdf`)
- Tag 1–5 inhaltlich migriert, alle Aufgaben-Umgebungen mit page-aware
  Strich (wechselt korrekt mit der Seitenparität, auch über Page-Breaks)
- Lösungen vorerst noch innerhalb der jeweiligen Kapitel (M5 lagert sie aus)
- Alte Markdown-Toolchain (`make alt`) baut Tag 1–5 weiterhin parallel
- `import/` ist geleert, `tag5_endliche_koerper.{md,pdf}` ist nach
  `markdown/` bzw. `referenz-pdfs/` einsortiert

## Nächste Schritte

1. **M5 — Lösungen in den Anhang.** Aktuell stehen die Lösungen am Ende
   jedes Kapitels (mit `\newpage` und `\section*{Lösungen}`). Idiomatischer
   wäre ein gemeinsamer `\appendix \chapter{Lösungen}` mit Sub-Sections
   pro Tag und `\autoref`-Querverweisen zwischen Aufgabe und Lösung.
2. **M6 — Glossar & Index.** Begriffe wie *Hamming-Distanz*,
   *Mindestdistanz*, *Bündelfehler*, *Generatorpolynom*, *Galois-Feld*,
   *irreduzibles Polynom* einsammeln, mit `glossaries` einbinden,
   Sachindex via `imakeidx`.
3. **M7 — Front-/Back-Matter.** Titelseite (jenseits des Default-`\maketitle`),
   Vorwort (Greta-als-Stilmittel-Erklärung), TOC-Tiefe justieren,
   Abbildungs-/Tabellenverzeichnis prüfen.
4. **M8 — Aufräumen.** Alte `vorlage/`, `markdown/`, `referenz-pdfs/`
   und `build/build.sh` archivieren oder entfernen, sobald sicher; Branch
   nach `main` mergen.

## Stolperfallen für Folgemigrationen

- **Anführungszeichen:** `babel[ngerman]` macht aus `"u` ein `ü`. Vor
  jedem Build: `grep '"' latex/kapitel/tagN.tex` und ASCII-`"` durch
  Unicode-`"` ersetzen. ABER: in `\begin{verbatim}`-Blöcken
  (Code-Beispiele wie `print("Hallo Greta")`) müssen die Quotes ASCII
  bleiben, sonst tippt Greta etwas Falsches ab.
- **Tabellen:** Standardmäßig `lll`-Spalten brechen aus dem
  Aufgabenblock heraus, wenn Inhalt zu lang. Bei textlastiger letzter
  Spalte: `p{Xcm}` verwenden.
- **`\checkmark`** braucht `amssymb` (in Präambel geladen).
- **`\write18`-Snippets** brauchen das Verzeichnis `latex/.snippets/`,
  das das Makefile-Target `buch` per `mkdir -p` anlegt.
- **Aufgaben-Strich nach Page-Break:** wird per `overlay` in der
  `aufgabebox` pro Page-Part neu gezeichnet (page-aware via
  `\strictpagecheck` + `\checkoddpage`/`\ifoddpage`); nicht zurück
  auf zwei separate Recto/Verso-Boxen umstellen.

## Lokale Voraussetzungen

```bash
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   collection-latexextra
brew install --cask font-dejavu
brew install pygments
```

Im Container-Schritt (Phase 2) wandert das alles ins Dockerfile.
