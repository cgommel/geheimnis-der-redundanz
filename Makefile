# Build-Targets für das Buchprojekt.
#
# `make`        baut das LaTeX-Buch nach pdf/latex/buch.pdf.
# `make alt`    baut die alten markdown-basierten Tageshefte (Brücke).
# `make clean`  räumt LaTeX-Build-Artefakte auf.
# `make shell`  öffnet eine Subshell im latex/-Verzeichnis (für ad-hoc latexmk).

.PHONY: all alt clean shell tag1 tag2 tag3 tag4 test-code

LATEX_DIR := latex
CODE_DIR := $(LATEX_DIR)/code

all: buch

buch: test-code
	mkdir -p pdf/latex/kapitel
	cd $(LATEX_DIR) && latexmk

# Syntaxprüfung aller Code-Snippets vor dem LaTeX-Build.
# -B unterdrückt das Schreiben von .pyc-Dateien.
test-code:
	@find $(CODE_DIR) -name "*.py" -type f -print0 \
	    | xargs -0 -I {} python3 -B -m py_compile {}
	@echo "✓ Alle Python-Snippets syntaktisch sauber"

# Alte Markdown-Toolchain (Brücke, wird mit M8 entfernt).
alt:
	./build/build.sh all

# Einzelne alte Tageshefte (Brücke).
tag1 tag2 tag3 tag4:
	./build/build.sh $@

clean:
	cd $(LATEX_DIR) && latexmk -C
	rm -rf pdf/latex

shell:
	cd $(LATEX_DIR) && exec $$SHELL
