# Das Geheimnis der Redundanz

## Von der Prüfziffer zum Datamatrix

Hauptperson ist **Greta**, 10. Klasse Gymnasium, im zweiwöchigen
Schülerpraktikum bei einem Onkel, der ihr ein bisschen
Codierungstheorie beibringen möchte. Das Buch begleitet sie auf der
Reise von der unscheinbaren EAN-13-Prüfziffer hinten am Strichcode
über Hamming, CRC und endliche Körper bis zum Reed-Solomon-Code, der
auf einem Datamatrix-Symbol zwei Wochen später ihren eigenen Namen
trägt — auch wenn die Hälfte mit dem Filzstift überschmiert ist.

### Bewusst hybrid: Bleistift trifft Python

Dieses Buch ist weder ein reines Mathe-Heft noch ein Programmierkurs.
Jede Etappe hat einen **Bleistift-Block** auf Karopapier und eine
**Python-Einheit** in Thonny. Beide Wege liefern denselben
Erkenntnisgewinn aus zwei Richtungen:

- Wer Reed-Solomon einmal von Hand über $\mathrm{GF}(2^3)$ rechnet,
  versteht, was die `reedsolo`-Bibliothek in 30 Zeilen abstrahiert.
- Wer einen EAN-13-Strichcode mit Lineal und Stift Modul für Modul
  aufmalt und vom Handy anstandslos scannen lässt, weiß einen
  Pillow-Encoder ganz anders zu schätzen.

Der Wechsel zwischen analog und digital ist Programm. Was beim Rechnen
zäh ist, ist beim Coden trivial — und umgekehrt. Wer beides macht,
versteht das Verfahren, nicht nur die API.

## Etappen

Das Buch ist als Praktikumstagebuch organisiert; je eine Etappe
entspricht ungefähr einem Praktikumstag (≈ 2 Stunden Arbeit für die
Zielperson).

**Im aktuellen Release enthalten:**

- Etappe 1 — Prüfziffern: Parität, EAN-13
- Etappe 2 — ISBN-10, Luhn, Hamming-Distanz
- Etappe 3 — Hamming-Code (7,4): erstes echtes Korrigieren
- Etappe 4 — SECDED, Bündelfehler, Interleaving, CRC
- Etappe 5 — Endliche Körper $\mathrm{GF}(2^n)$, die neue Mathematik
- Etappe 6 — Polynome über $\mathrm{GF}(2^n)$, Reed-Solomon-Idee
- Etappe 7 — Reed-Solomon-Encoder + Wechsel auf $\mathrm{GF}(2^8)$
- Etappe 8 — Reed-Solomon-Decoder (Auslöschungen + `reedsolo`)

**Geplant:**

- Etappe 9 — EAN-13 von Hand zeichnen
- Etappe 10 — EAN-13 mit Python zeichnen
- Etappe 11 — Datamatrix: Layout, Module, ECC-200
- Etappe 12 — Datamatrix selbst zeichnen und decodieren

Lösungen zu allen Aufgaben stehen gesammelt im Anhang.

## Lesen

Aktuelle PDF-Ausgaben liegen unter
[**Releases**](https://github.com/cgommel/geheimnis-der-redundanz/releases).
Jeder Release-Tag liefert das vollständige Buch als
`geheimnis-der-redundanz.pdf`, gebaut aus dem Stand des
entsprechenden Commits.

## Aus den Quellen bauen

Bauanleitung, Container-Setup, Verzeichnisstruktur und
Layout-Eigenschaften stehen in [`BUILD.md`](BUILD.md). Kurz:

```bash
make           # baut das Hauptbuch nach pdf/latex/geheimnis-der-redundanz.pdf
make container # reproduzierbarer Container-Build
```

## Lizenz

- **Buchtext** (Kapitel, Aufgaben, Diagramme, Lösungen):
  [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
  — siehe [`LICENSE`](LICENSE). Du darfst teilen und bearbeiten, auch
  kommerziell, solange Du die Urheberschaft nennst und Bearbeitungen
  unter derselben Lizenz weitergibst.
- **Python-Snippets** unter [`latex/code/`](latex/code/):
  [MIT](latex/code/LICENSE) — wiederverwendbar in eigenen Projekten
  ohne Copyleft-Zwang.
- **Vendored Schriften** unter [`latex/fonts/`](latex/fonts/) (Source Pro
  Familie, STIX Two Math): [SIL Open Font License 1.1](https://openfontlicense.org)
  — Lizenztexte je Familie unter `latex/fonts/<familie>/`.
