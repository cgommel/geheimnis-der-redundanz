# Work in Progress

> Aktueller Arbeitsstand und nächste Schritte.

## Stand: Ende des Polish-Sprint-Anlaufs (2026-04-29)

`main` enthält Tag 1–6, Container-Build, GitHub-Actions, Glossar,
Index (leer), Vorwort, Titelseite plus den ersten Layout-Fix (LY-01,
Marginalie verwaist nach Page-Break per `\needspace`).

**Releases:**
- `v2026.04.29` — Tag 1–6, Polish noch offen.
- `v2026.04.29.1` — Polish-Infrastruktur (M6 + M7) + LY-01-Fix.
  Tag-Push war gepusht, Release-Workflow lief beim Schließen der
  Sitzung noch (Image-Bau mit erweitertem Dockerfile dauert).

## Nächste Schritte

1. **Release-Run abchecken**: `gh run list --workflow release.yml
   --limit 1` und ggf. `gh release view v2026.04.29.1`. Falls grün:
   PDF-Asset prüfen.
2. **Mängelliste abarbeiten** (`doku/MAENGEL.md`, 13 offene Layout-
   Punkte). Reihenfolge der Sichtbarkeit: LY-05 (Tag-2-Tabelle 72 pt
   zu breit), LY-02 (TikZ-Diagramm EAN-13), LY-04+LY-06 zusammen
   (`\sectionmitzeit`), LY-09 / LY-11 / LY-10 / LY-12, dann LY-08 +
   LY-13 + LY-03 ganz am Ende (Microtype-Mikropolish — verschiebt
   sich bei jeder Textänderung).
3. **Inhaltliches Review** durchs ganze Buch nach Polish — eigene
   Sektion in `MAENGEL.md` füllen.
4. **Tag 7** (Reed-Solomon-Encoder mit Generator-Polynom) als
   `feature/tag7`-Branch.

## Konventionen, die wir uns gesetzt haben

- Erst sammeln in `doku/MAENGEL.md`, dann systematisch fixen — keine
  Hotfixes ohne Eintrag.
- Nach jedem Push: `gh run list` schauen, ob CI grün ist (lokale
  und Container-Welt können driften).
- Commit-Messages ohne Claude-Spuren.
- Farben in CMYK, Anführungszeichen Unicode (Babel-`"`-Shorthand ist
  global abgeschaltet).

## Lokale Voraussetzungen

```bash
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   needspace collection-latexextra
brew install --cask font-dejavu
brew install pygments
```

Im Container ist alles drin (`build/Dockerfile` mit Debian Trixie).
