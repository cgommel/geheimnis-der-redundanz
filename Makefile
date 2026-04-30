# Build-Targets für das Buchprojekt.
#
# `make` / `make buch`     baut das Hauptbuch (alle Etappen, mit Titelseite)
#                          nach pdf/latex/geheimnis-der-redundanz.pdf.
# `make redundanz-tagN`    baut den Standalone „Buch bis Etappe N" ohne
#                          Titelseite nach pdf/latex/redundanz-tagN.pdf
#                          (N = 1 .. 8).
# `make standalones`       baut alle Standalones der Reihe nach.
# `make test-code`         prüft alle Python-Snippets syntaktisch.
# `make clean`             räumt LaTeX-Build-Artefakte auf.
# `make shell`             öffnet eine Subshell im latex/-Verzeichnis.

LATEX_DIR  := latex
CODE_DIR   := $(LATEX_DIR)/code
HAUPTBUCH  := geheimnis-der-redundanz
ETAPPEN    := 1 2 3 4 5 6 7 8 9
STANDALONES := $(addprefix redundanz-tag,$(ETAPPEN))

.PHONY: all buch standalones $(STANDALONES) clean shell test-code container container-clean

all: buch

# --- Hauptbuch -------------------------------------------------------
# latexmk gibt beim Cold-Start einen non-zero Exit-Code zurück, obwohl
# das PDF erfolgreich gebaut wird (Glossar braucht zwei Durchläufe,
# hyperref-Warnings beim ersten Durchlauf). Wir tolerieren das mit dem
# vorangestellten "-" und prüfen am Ende explizit auf das PDF.
buch: test-code
	mkdir -p pdf/latex/kapitel $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f $(HAUPTBUCH).tex
	@test -f pdf/latex/$(HAUPTBUCH).pdf && echo "✓ pdf/latex/$(HAUPTBUCH).pdf"

# --- Standalones „Buch bis Etappe N" --------------------------------
# Pro Etappe ein Master latex/redundanz-tagN.tex; sie teilen sich den
# Body in latex/buch-rumpf.tex. Selber Cold-Start-Workaround.
$(STANDALONES): test-code
	mkdir -p pdf/latex/kapitel $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f $@.tex
	@test -f pdf/latex/$@.pdf && echo "✓ pdf/latex/$@.pdf"

standalones: $(STANDALONES)

# --- Code-Sanity ----------------------------------------------------
# Syntaxprüfung aller Python-Snippets vor dem LaTeX-Build.
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
