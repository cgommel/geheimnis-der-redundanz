# Build-Targets für das Buchprojekt.
#
# `make`        baut das LaTeX-Buch nach pdf/latex/buch.pdf.
# `make alt`    baut die alten markdown-basierten Tageshefte (Brücke).
# `make clean`  räumt LaTeX-Build-Artefakte auf.
# `make shell`  öffnet eine Subshell im latex/-Verzeichnis (für ad-hoc latexmk).

.PHONY: all alt clean shell tag1 tag2 tag3 tag4

LATEX_DIR := latex

all: buch

buch:
	mkdir -p pdf/latex/kapitel
	cd $(LATEX_DIR) && latexmk

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
