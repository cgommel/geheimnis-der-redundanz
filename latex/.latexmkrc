# latexmk-Konfiguration für das Buchprojekt.
#
# Aufruf via Makefile (im Repo-Root): `make` baut buch.tex.
# Output (PDF und Build-Artefakte) landet in ../pdf/latex/.

$pdf_mode = 5;        # XeLaTeX
$pdflatex = 'xelatex -interaction=nonstopmode -synctex=1 -shell-escape -file-line-error %O %S';

$out_dir = '../pdf/latex';

# Damit \include-Dateien beim Editieren erkannt werden:
@default_files = ('buch.tex');
