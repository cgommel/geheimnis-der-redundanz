# Work in Progress

> Aktueller Arbeitsstand auf `feature/latex-native`. Kurzer Schnappschuss,
> damit die Arbeit nach einer Pause wieder schnell aufgenommen werden kann.

## Wo wir sind (Stand: Pause)

Branch: `feature/latex-native`

| Phase | Schritt | Status |
|-------|---------|--------|
| Phase 0 | Build-Reparatur, GitHub-Repo, Layout-Briefing | ✅ |
| Phase 1, M1 | LaTeX-Skelett & Layout (scrbook, tcolorbox) | ✅ |
| Phase 1, M2 | Python-Snippet-Infrastruktur (minted) | ✅ |
| Phase 1, M3 | Tag 3 migrieren | 🟡 in Arbeit |
| Phase 1, M4 | Tag 1, 2, 4 migrieren | ⬜ |
| Phase 1, M5 | Lösungen herauslösen, `\autoref` | ⬜ |
| Phase 1, M6 | Glossar & Index | ⬜ |
| Phase 1, M7 | Front-/Back-Matter | ⬜ |
| Phase 1, M8 | Aufräumen, Merge nach `main` | ⬜ |
| Phase 2 | Container-Migration | ⬜ |
| Phase 3 | CI/Release | ⬜ |

## M3 — Stand im Detail

**Was geht:**
- Tag 3 inhaltlich vollständig nach `latex/kapitel/tag3.tex` migriert (alle fünf Blöcke + Lösungen).
- Code-Snippets in `latex/code/tag3/hamming74.py` mit Region-Markern (`encoder`, `decoder`, `test-einzel`, `test-doppel`).
- `\pythoncodeteil{file}{region}`-Befehl funktioniert via `latex/scripts/extract_region.py` und `\write18`-Aufruf zur Build-Zeit. Snippets landen in `latex/.snippets/`.
- `latexmk` ruft jetzt korrekt `xelatex -shell-escape` auf (vorher hatte `.latexmkrc` nur `$pdflatex` gesetzt; bei `$pdf_mode = 5` zählt aber `$xelatex`).
- Erste Build-Iteration mit Tag 3 lief grün (23 Seiten Buch, 167 KB).
- TikZ-Venn nutzt unsere CMYK-Aufgabenfarben (Bleistift/Python/Werkzeug) statt orange/blue/green.

**Was offen ist:**
- ⚠️ **Babel-Shorthand-Bug:** ASCII `"` in deutschen Texten wird von `babel[ngerman]` als Shorthand-Aktivator interpretiert (`„Platz" um` wurde im PDF zu `„Platzüm`). Ich habe alle 17 Vorkommen in `tag3.tex` durch Unicode-`"` (U+201C) ersetzt, **aber den Build danach nicht mehr verifiziert** — das ist der erste Schritt nach der Pause: `make` und Tag-3-Seiten anschauen.
- A/B-Vergleich gegen `pdf/tag3_hamming_code.pdf` (alt) noch nicht systematisch durchgeführt.
- Kleinere Layout-Fragen, die in M7 zu klären sind:
  - `\section*{Lernziele für heute}` ist absichtlich unnummeriert — soll das so bleiben?
  - „3.1 Wie viele Prüfbits …" als nummerierter Section-Titel mit Zeitangabe ist nicht gerade elegant; im alten PDF stand „Block 1 · …".
  - Anführungszeichen-Bug betrifft nur tag3 (Stubs haben keine Quotes); muss beim Migrieren von Tag 1/2/4 mitbedacht werden.

## Was als nächstes ansteht

1. **Build verifizieren** nach dem Quote-Fix: `make -C /Users/chg/git/redundancy-book` und Tag-3-Seiten 9–15 (oder so) prüfen.
2. **A/B-Vergleich** gegen das alte PDF: `make alt` baut die Markdown-Variante in `pdf/tag3_hamming_code.pdf` zum direkten Daneben-Legen.
3. **M3 abschließen** mit Commit „M3: Tag 3 migriert".
4. **Tag-5-Import:** Sobald M3 stabil committet ist, das in `import/files.zip` (unversioniert!) abgelegte Tag-5-Material entpacken, sichten und nach `latex/kapitel/tag5.tex` + `latex/code/tag5/` einsortieren.
5. **M4** (Tag 1, 2, 4 migrieren) folgt danach — ob vor oder nach Tag 5 ist Entscheidung des Onkels.

## Lokale Voraussetzungen, die wir auf dem Weg gesammelt haben

Damit der Build lokal läuft, müssen installiert sein:

```bash
# TeX-Pakete (Mac, MacTeX/TeX Live 2026):
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   collection-latexextra
# Schriften:
brew install --cask font-dejavu
# minted-Backend:
brew install pygments
```

Im Container-Schritt (Phase 2) wandert das alles ins Dockerfile.

## Bekannte Stolperfallen für die Migration weiterer Tage

- **Anführungszeichen:** vor Build immer `grep '"' latex/kapitel/tagN.tex` und alle Treffer durch Unicode-Quotes ersetzen.
- **`\checkmark`** braucht `amssymb` (in Präambel geladen).
- **`\write18`-Snippets** brauchen das Verzeichnis `latex/.snippets/`, das das Makefile-Target `buch` per `mkdir -p` anlegt.
- **`(7,4)`-Hamming-Code:** als Mathematik mit `(7,4)` (ohne Mathe-Mode) belassen, weil im Fließtext besser lesbar.
