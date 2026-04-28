# Work in Progress

> Aktueller Arbeitsstand und nächste Schritte.

## Phase 1 — LaTeX-native Migration: ✅ abgeschlossen

| Schritt | Inhalt | Status |
|---------|--------|--------|
| M1 | Skelett & Layout (scrbook, tcolorbox, page-aware Strich) | ✅ |
| M2 | Python-Snippet-Infrastruktur (minted, Region-Marker) | ✅ |
| M3 | Tag 3 migriert | ✅ |
| M4 | Tag 1, 2, 4 migriert | ✅ |
| M4½ | Tag 5 importiert und migriert | ✅ |
| M5 | Lösungen in den Anhang ausgelagert | ✅ |
| M8 | Aufräumen, Merge nach `main` | 🟡 |

Aktueller Stand: 72 Seiten, Tag 1–5 vollständig, Lösungen im Anhang A
(eine Datei pro Tag in `latex/loesungen/`, gebündelt durch
`latex/anhang_loesungen.tex`).

**Auf Eis (Polish-Sprint nach dem Buch-Review):**

- M6 — Glossar & Index
- M7 — Front-/Back-Matter

## Phase 2 — Container-Build lokal: 🟡 in Arbeit

`build/Dockerfile` (Debian Bookworm + TeX Live + DejaVu + Pygments)
und `build/in-container.sh` (Engine-Detection: Apple `container` →
Docker → Fehler) sind angelegt, `make container` baut das Buch.

**Getestet:** Apple `container` 0.11 baut grün durch. (Docker-Pfad
plausibel, weil OCI-Standard, aber noch nicht explizit getestet.)

**Konsistenz:** Container und lokal bauen beide 72 Seiten —
deckungsgleicher Output. Die Wahl Debian Trixie statt Bookworm
schließt den TeX-Live-Versionsabstand zur lokalen Installation
(beide jetzt nahe TL 2025/2026).

## Anstehende Phasen

| Phase | Inhalt | Branch |
|-------|--------|--------|
| 3 | CI/Release auf GitHub (PR-Builds, tag-getriebene Releases) | `feature/ci-release` |
| 4 | Tag 6 (Polynome über GF(2^n), Reed-Solomon-Idee) | `feature/tag6` |
| 5 (opt.) | Tag 7 (Reed-Solomon-Encoder) | `feature/tag7` |
| Review | Mängel- und Vorschlagsliste übers ganze Buch | gesondert |
| Polish | M6, M7, Review-Punkte abarbeiten | gesondert |

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

Phase 2 (Container) kapselt das in ein Dockerfile.
