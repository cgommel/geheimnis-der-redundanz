# Build-Targets für das Buchprojekt.
#
# `make`            baut das LaTeX-Buch nach pdf/latex/buch.pdf.
# `make test-code`  prüft alle Python-Snippets syntaktisch.
# `make clean`      räumt LaTeX-Build-Artefakte auf.
# `make shell`      öffnet eine Subshell im latex/-Verzeichnis (für ad-hoc latexmk).

.PHONY: all buch clean shell test-code

LATEX_DIR := latex
CODE_DIR := $(LATEX_DIR)/code

all: buch

buch: test-code
	mkdir -p pdf/latex/kapitel $(LATEX_DIR)/.snippets
	cd $(LATEX_DIR) && latexmk

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
