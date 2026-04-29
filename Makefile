# Build-Targets für das Buchprojekt.
#
# `make`            baut das LaTeX-Buch nach pdf/latex/buch.pdf.
# `make test-code`  prüft alle Python-Snippets syntaktisch.
# `make clean`      räumt LaTeX-Build-Artefakte auf.
# `make shell`      öffnet eine Subshell im latex/-Verzeichnis (für ad-hoc latexmk).

.PHONY: all buch buch_tag7 buch_tag8 buch_tag7_8 clean shell test-code container container-clean

LATEX_DIR := latex
CODE_DIR := $(LATEX_DIR)/code

all: buch

buch: test-code
	mkdir -p pdf/latex/kapitel $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f
	@test -f pdf/latex/buch.pdf && echo "✓ pdf/latex/buch.pdf"

# Standalone-Auszüge — Vorab-PDFs einzelner Kapitel (Greta-Material,
# solange das Hauptbuch noch im Polish-Sprint hängt).
# latexmk gibt bei diesen Auszügen einen non-zero Exit-Code zurück,
# obwohl das PDF erfolgreich gebaut wird (Cold-Start-Quirk mit
# Glossar plus hyperref-Warnings). Wir tolerieren das mit dem
# vorangestellten "-" und prüfen am Ende explizit auf das PDF.
buch_tag7: test-code
	mkdir -p pdf/latex/kapitel $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f -jobname=buch_tag7 buch_tag7.tex
	@test -f pdf/latex/buch_tag7.pdf && echo "✓ pdf/latex/buch_tag7.pdf"

buch_tag8: test-code
	mkdir -p pdf/latex/kapitel $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f -jobname=buch_tag8 buch_tag8.tex
	@test -f pdf/latex/buch_tag8.pdf && echo "✓ pdf/latex/buch_tag8.pdf"

buch_tag7_8: test-code
	mkdir -p pdf/latex/kapitel $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f -jobname=buch_tag7_8 buch_tag7_8.tex
	@test -f pdf/latex/buch_tag7_8.pdf && echo "✓ pdf/latex/buch_tag7_8.pdf"

# Syntaxprüfung aller Code-Snippets vor dem LaTeX-Build.
# -B unterdrückt das Schreiben von .pyc-Dateien.
test-code:
	@find $(CODE_DIR) -name "*.py" -type f -print0 \
	    | xargs -0 -I {} python3 -B -m py_compile {}
	@echo "✓ Alle Python-Snippets syntaktisch sauber"

clean:
	cd $(LATEX_DIR) && latexmk -C
	rm -rf pdf/latex $(LATEX_DIR)/.snippets

shell:
	cd $(LATEX_DIR) && exec $$SHELL

# --- Container-Build -------------------------------------------------
# `make container`        baut das Buch im Container (Engine-Auto-Detection:
#                         bevorzugt Apple `container`, Fallback Docker).
# `make container-clean`  ruft `make clean` im Container auf.
# Erzwungene Engine: `ENGINE=docker make container`.

container:
	./build/in-container.sh

container-clean:
	./build/in-container.sh clean
