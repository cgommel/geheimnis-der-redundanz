# latexmk-Konfiguration für das Buchprojekt.
#
# Aufruf via Makefile (im Repo-Root):
#   `make`                    → geheimnis-der-redundanz.tex (Hauptbuch)
#   `make redundanz-tagN`     → redundanz-tagN.tex (Standalone)
#   `make standalones`        → alle 8 Standalones der Reihe nach
# Output (PDF und Build-Artefakte) landet in ../pdf/latex/.

$pdf_mode = 5;        # XeLaTeX
# Bei $pdf_mode = 5 wird $xelatex (nicht $pdflatex) verwendet.
# -shell-escape ist nötig für minted (Pygments) und unseren \pythoncodeteil.
$xelatex = 'xelatex -interaction=nonstopmode -synctex=1 -shell-escape -file-line-error %O %S';

$out_dir = '../build/latex';

# Wenn latexmk ohne Argument aufgerufen wird, bauen wir das Hauptbuch.
@default_files = ('geheimnis-der-redundanz.tex');
