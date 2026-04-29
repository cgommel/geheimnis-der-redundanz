# Work in Progress

> Aktueller Arbeitsstand und nächste Schritte. Letzter Update vor
> drohender Conversation-Kompaktierung — soll als persistenter Anker
> dienen, wenn die Chat-Historie verkürzt wird.

## Stand: 2026-04-29 (nach Tag 7 + Tag 8)

### Was im Buch ist (`main`-Branch)

`main` hatte bis gerade Tag 1–6 plus Polish (Glossar, Index-Header,
Vorwort, Titelseite). Der Polish-Sprint ist gemergt; Release
`v2026.04.29.1` ist live.

### Was auf `feature/tag7-8` liegt (noch nicht gemergt)

- **Tag 7** — Reed-Solomon-Encoder mit Generator-Polynom, Wechsel auf
  GF($2^8$), systematische Codierung. `latex/kapitel/tag7.tex` plus
  `latex/code/tag7/{gf256.py, rs_encoder.py}` mit Region-Markern.
  Lösung in `latex/loesungen/tag7.tex`.
- **Tag 8** — Reed-Solomon-Decoder, Auslöschungs-Decoder vollständig
  von Hand und in Python (Vandermonde + Gauß in GF($2^8$)),
  Berlekamp-Massey nur als Skizze, `reedsolo`-Library für die
  Praxis. Code in `latex/code/tag8/{syndrome.py, erasure_decoder.py,
  with_reedsolo.py}`. Lösung in `latex/loesungen/tag8.tex`.
- **Standalone-Master** für Vorab-PDFs ohne Mergen:
  `latex/buch_tag7.tex`, `latex/buch_tag8.tex`,
  `latex/buch_tag7_8.tex`. Targets: `make buch_tag7`,
  `make buch_tag8`, `make buch_tag7_8`.
- **Hauptbuch** umfasst auf dem Branch jetzt 110 Seiten (Tag 1–8 +
  Anhang).

### Branch-Status

- `feature/tag7-8` ist gepusht, Commits: M5/M8 → Polish → Tag 7 → Tag 8 + Standalones.
- Noch nicht gemergt nach `main`. Vor Merge ist (a) Tag 7-Review
  durch Onkel offen, (b) Tag 8-Review noch gar nicht erfolgt.
- CI auf `feature/tag7-8` lief beim letzten Stand grün (Build mit dem
  erweiterten Container-Image: trixie + texlive-plain-generic +
  texlive-extra-utils).

### Mängelliste (`doku/MAENGEL.md`)

13 Layout-Punkte zur Abarbeitung. Stand: alle offen, keiner in
Arbeit. LY-01 (Marginalie verwaist nach Page-Break) ist bereits
durch `\needspace{5\baselineskip}` gefixt — Eintrag aktualisieren,
falls nochmal angefasst.

### Standalone-PDFs für Greta (alle aktuell)

- `pdf/latex/buch_tag7.pdf` — 13 Seiten
- `pdf/latex/buch_tag8.pdf` — 15 Seiten
- `pdf/latex/buch_tag7_8.pdf` — 28 Seiten (kompaktes Reed-Solomon-Heft)

## Nächste Schritte (priorisiert)

1. **Onkel reviewt Tag 7 + 8** inhaltlich. Korrekturen kommen als
   Hotfix-Commits auf `feature/tag7-8`.
2. **Merge `feature/tag7-8` → `main`**, neuer Tag (z.\,B.\
   `v2026.04.30`) → Release-PDF auf GitHub.
3. **Tag 9** (Intermezzo „1D-Strichcode mit Pillow zeichnen", Code
   39) als nächster Branch `feature/tag9`. Greta soll am eigenen
   Strichcode mit Handy scannen.
4. **Tag 10/11**: Datamatrix Theorie & Praxis.
5. **Mängellisten-Sprint**: gesammelte LY-XX-Punkte aus
   `doku/MAENGEL.md` durcharbeiten.
6. **Bonus-Tage** 12/13 (QR-Codes, Voyager) bei Greta-Tempo.

## Konventionen, die wir uns gesetzt haben

- Erst sammeln in `doku/MAENGEL.md`, dann systematisch fixen — keine
  Hotfixes ohne Eintrag.
- Nach jedem Push: `gh run list` schauen, ob CI grün ist (lokale und
  Container-Welt können driften).
- Commit-Messages ohne Claude-Spuren, auf Deutsch.
- Farben in CMYK, Anführungszeichen Unicode (Babel-`"`-Shorthand ist
  global abgeschaltet).
- Standalone-Master für Vorab-PDFs einzelner Tage — Pattern
  `latex/buch_tagN.tex` plus Makefile-Target `make buch_tagN`.
- Latexmk-Cold-Start-Glossar-Quirk: Standalone-Targets nutzen `-f`
  und ignorierten Exit-Code, mit `test -f` als finaler Check.
- Tag in Branch-Name: `feature/tagN` für ein einzelnes Kapitel,
  `feature/tagN-M` für mehrere.

## Lokale Voraussetzungen

```bash
sudo tlmgr install fvextra framed newunicodechar latexmk \
                   tcolorbox changepage tikzfill pdfcol \
                   needspace collection-latexextra
brew install --cask font-dejavu
brew install pygments
pip install reedsolo  # für Tag 8 Python-Einheit 3
```

Im Container ist alles drin (`build/Dockerfile` mit Debian Trixie +
`texlive-plain-generic` + `texlive-extra-utils`); `reedsolo` müsste
für Container-Builds noch ergänzt werden — bisher nicht eingebaut,
weil `make test-code` nur Syntax prüft (`py_compile` braucht keine
Imports zu auflösen).
