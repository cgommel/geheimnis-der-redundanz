# Build-Targets für das Buchprojekt.
#
# `make` / `make buch`     baut das Hauptbuch (alle Etappen, mit Titelseite)
#                          nach pdf/geheimnis-der-redundanz.pdf.
# `make redundanz-tagN`    baut den Auszug zu Etappe N (nur Etappe N
#                          plus zugehörige Lösung) nach pdf/redundanz-tagN.pdf
#                          (N = 1 .. 9).
# `make standalones`       baut alle Auszüge der Reihe nach.
# `make test-code`         prüft alle Python-Snippets syntaktisch.
# `make clean`             räumt Build-Artefakte und PDFs auf.
# `make shell`             öffnet eine Subshell im latex/-Verzeichnis.
#
# LaTeX-Zwischendateien landen unter build/latex/, fertige PDFs werden
# nach pdf/ kopiert. Beide sind gitignored.

LATEX_DIR  := latex
CODE_DIR   := $(LATEX_DIR)/code
BUILD_DIR  := build/latex
PDF_DIR    := pdf
HAUPTBUCH  := geheimnis-der-redundanz
ETAPPEN    := 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
STANDALONES := $(addprefix redundanz-tag,$(ETAPPEN))
VORLAGEN    := zeichenvorlage-ean13 zeichenvorlage-datamatrix

.PHONY: all alles buch standalones $(STANDALONES) vorlagen $(VORLAGEN) clean shell test-code container container-clean

all: buch

# `make alles` baut Hauptbuch + alle Auszüge + alle Werkstatt-Vorlagen.
# Wird vom CI-Release verwendet, damit jedes PDF einzeln als Asset
# hochgeladen werden kann.
alles: buch standalones vorlagen

# --- Hauptbuch -------------------------------------------------------
# latexmk gibt beim Cold-Start einen non-zero Exit-Code zurück, obwohl
# das PDF erfolgreich gebaut wird (Glossar braucht zwei Durchläufe,
# hyperref-Warnings beim ersten Durchlauf). Wir tolerieren das mit dem
# vorangestellten "-" und prüfen am Ende explizit auf das PDF.
#
# Etappe 9 bindet pdf/zeichenvorlage-ean13.pdf via pdfpages ein,
# Etappe 13 zusätzlich pdf/zeichenvorlage-datamatrix.pdf — beide
# Vorlagen müssen also vor dem Buch-Build da sein.
buch: test-code $(PDF_DIR)/zeichenvorlage-ean13.pdf \
                $(PDF_DIR)/zeichenvorlage-datamatrix.pdf
	mkdir -p $(BUILD_DIR)/kapitel $(PDF_DIR) $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f $(HAUPTBUCH).tex
	@cp $(BUILD_DIR)/$(HAUPTBUCH).pdf $(PDF_DIR)/
	@test -f $(PDF_DIR)/$(HAUPTBUCH).pdf && echo "✓ $(PDF_DIR)/$(HAUPTBUCH).pdf"

# --- Auszüge pro Etappe ---------------------------------------------
# Pro Etappe N gibt es einen Master latex/redundanz-tagN.tex; sie
# rendern jeweils nur die eine Etappe + ihre Lösung. Selber Cold-Start-
# Workaround wie beim Hauptbuch.
$(STANDALONES): test-code
	mkdir -p $(BUILD_DIR) $(PDF_DIR) $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f $@.tex
	@cp $(BUILD_DIR)/$@.pdf $(PDF_DIR)/
	@test -f $(PDF_DIR)/$@.pdf && echo "✓ $(PDF_DIR)/$@.pdf"

# Etappe 9 hängt zusätzlich vom EAN-13-Werkstattbogen ab,
# Etappe 13 vom Datamatrix-Werkstattbogen.
redundanz-tag9:  $(PDF_DIR)/zeichenvorlage-ean13.pdf
redundanz-tag13: $(PDF_DIR)/zeichenvorlage-datamatrix.pdf

standalones: $(STANDALONES)

# --- Werkstatt-Vorlagen (Etappe 9 ff.) -------------------------------
# zeichenvorlage-ean13.pdf — EAN-13-Werkstattbogen für Etappe 9.
$(PDF_DIR)/zeichenvorlage-ean13.pdf: $(LATEX_DIR)/zeichenvorlage-ean13.tex \
                                     $(LATEX_DIR)/zeichenfeld.tex \
                                     $(LATEX_DIR)/ean13-encoding.tex
	mkdir -p $(BUILD_DIR) $(PDF_DIR) $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f zeichenvorlage-ean13.tex
	@cp $(BUILD_DIR)/zeichenvorlage-ean13.pdf $(PDF_DIR)/
	@test -f $(PDF_DIR)/zeichenvorlage-ean13.pdf && echo "✓ $(PDF_DIR)/zeichenvorlage-ean13.pdf"

zeichenvorlage-ean13: $(PDF_DIR)/zeichenvorlage-ean13.pdf

# zeichenvorlage-datamatrix.pdf — Datamatrix-Werkstattbogen für Etappe 13.
$(PDF_DIR)/zeichenvorlage-datamatrix.pdf: \
        $(LATEX_DIR)/zeichenvorlage-datamatrix.tex \
        $(LATEX_DIR)/zeichenfeld-datamatrix.tex
	mkdir -p $(BUILD_DIR) $(PDF_DIR) $(LATEX_DIR)/.snippets
	-cd $(LATEX_DIR) && latexmk -f zeichenvorlage-datamatrix.tex
	@cp $(BUILD_DIR)/zeichenvorlage-datamatrix.pdf $(PDF_DIR)/
	@test -f $(PDF_DIR)/zeichenvorlage-datamatrix.pdf && echo "✓ $(PDF_DIR)/zeichenvorlage-datamatrix.pdf"

zeichenvorlage-datamatrix: $(PDF_DIR)/zeichenvorlage-datamatrix.pdf

vorlagen: $(VORLAGEN)

# --- Code-Sanity ----------------------------------------------------
# Syntaxprüfung aller Python-Snippets vor dem LaTeX-Build.
# -B unterdrückt das Schreiben von .pyc-Dateien.
test-code:
	@find $(CODE_DIR) -name "*.py" -type f -print0 \
	    | xargs -0 -I {} python3 -B -m py_compile {}
	@echo "✓ Alle Python-Snippets syntaktisch sauber"

clean:
	cd $(LATEX_DIR) && latexmk -C
	rm -rf $(BUILD_DIR) $(PDF_DIR) $(LATEX_DIR)/.snippets

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
