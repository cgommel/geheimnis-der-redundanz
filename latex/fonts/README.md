# Vendored Fonts

Hausschriften des Buchprojekts, beschafft direkt aus den jeweiligen
Primärquellen. Alle vier Familien stehen unter der **SIL Open Font
License 1.1** (OFL-1.1), siehe `LICENSE.md` / `OFL.txt` in den
einzelnen Unterordnern.

## Provenance

| Familie         | Version      | Quelle                                                                 | Commit-SHA |
|-----------------|--------------|------------------------------------------------------------------------|------------|
| Source Serif 4  | 4.005R       | https://github.com/adobe-fonts/source-serif/releases/tag/4.005R        | `2823e993c53fca27c5c8749f529b56a5a7c77b6b` |
| Source Sans 3   | 3.052R       | https://github.com/adobe-fonts/source-sans/releases/tag/3.052R         | `5d173ba058bda87bcff2bb2d53b9d2c59d440ff6` |
| Source Code Pro | release/HEAD | https://github.com/adobe-fonts/source-code-pro (Tag `2.042R-u/1.062R-i/1.026R-vf` enthält Slashes — Commit-SHA des `release`-Branches gepinnt) | `803b7e23ec97ae58b6232ea76519a76d428ba268` |
| STIX Two Math   | 2.13 b171    | https://github.com/stipub/stixfonts/releases/tag/v2.13b171              | `744a22a4dd626cd14d75728aef34fc8ad7c85db0` |

## Schnitte je Familie

Pro Familie sind nur die im Buch tatsächlich genutzten Schnitte
abgelegt. Falls weitere Gewichte (Light, Semibold, Black, …) gebraucht
werden, aus den oberen Quellen nachladen.

- **Source Serif / Sans / Code Pro:** Regular, Italic, Bold, BoldItalic
- **STIX Two Math:** nur Regular (Math-Schrift, alle Symbole im
  Regular-Schnitt)

## Aktualisieren

```bash
# Beispiel: Source Serif auf neuen Tag heben
SHA_OR_TAG=4.005R   # oder eine spezifische Commit-SHA
for f in Regular It Bold BoldIt; do
  curl -fsSL -o "latex/fonts/source-serif/SourceSerif4-$f.otf" \
    "https://raw.githubusercontent.com/adobe-fonts/source-serif/$SHA_OR_TAG/OTF/SourceSerif4-$f.otf"
done
curl -fsSL -o "latex/fonts/source-serif/LICENSE.md" \
  "https://raw.githubusercontent.com/adobe-fonts/source-serif/$SHA_OR_TAG/LICENSE.md"
```

Beim Updaten Tabelle oben mit neuer Version und neuer Commit-SHA
mitziehen.
