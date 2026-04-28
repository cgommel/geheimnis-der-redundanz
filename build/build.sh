#!/usr/bin/env bash
# Build-Skript für die Tutorial-Hefte
#
# Verwendung:
#   ./build.sh tag3       Baut nur Tag 3
#   ./build.sh all        Baut alle Hefte
#
# Das Skript erwartet die Markdown-Dateien in ../markdown/
# und legt die fertigen PDFs in ../pdf/ ab.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MD_DIR="$REPO_ROOT/markdown"
VORLAGE_DIR="$REPO_ROOT/vorlage"
OUT_DIR="$REPO_ROOT/pdf"

mkdir -p "$OUT_DIR"

# Mapping Tag → Markdown-Dateiname → Heft-Titel
declare -A TAG_DATEI
TAG_DATEI[tag1]="tag1_pruefziffern.md"
TAG_DATEI[tag2]="tag2_isbn_luhn_hamming.md"
TAG_DATEI[tag3]="tag3_hamming_code.md"
TAG_DATEI[tag4]="tag4_secded_crc_interleaving.md"

declare -A TAG_TITEL
TAG_TITEL[tag1]="Tag 1 \\textperiodcentered{} Prüfziffern und Fehlererkennung"
TAG_TITEL[tag2]="Tag 2 \\textperiodcentered{} Cleverere Prüfziffern \\& Hamming-Distanz"
TAG_TITEL[tag3]="Tag 3 \\textperiodcentered{} Hamming-Codes: erstes echtes Korrigieren"
TAG_TITEL[tag4]="Tag 4 \\textperiodcentered{} Bündelfehler, Interleaving, CRC"

build_tag() {
    local tag="$1"
    local md_file="${TAG_DATEI[$tag]:-}"
    local titel="${TAG_TITEL[$tag]:-}"

    if [[ -z "$md_file" ]]; then
        echo "Unbekannter Tag: $tag" >&2
        echo "Verfügbar: ${!TAG_DATEI[*]}" >&2
        return 1
    fi

    echo "── Baue $tag ($md_file)"

    # Temporäres Build-Verzeichnis
    local build_dir
    build_dir=$(mktemp -d)
    trap 'rm -rf "$build_dir"' RETURN

    cd "$build_dir"

    # 1. Markdown → LaTeX-Body
    pandoc "$MD_DIR/$md_file" -t latex -o body.tex --highlight-style=tango

    # 2. Postprozessor
    python3 "$VORLAGE_DIR/marginalien_postprocess.py" body.tex

    # 3. main.tex
    cat > main.tex <<EOF
\\newcommand{\\heftTitel}{$titel}
\\input{vorlage_koma.tex}
EOF

    # 4. Vorlage hineinkopieren
    cp "$VORLAGE_DIR/vorlage_koma.tex" .

    # 5. xelatex zweimal
    xelatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true
    xelatex -interaction=nonstopmode main.tex >/dev/null 2>&1 || true

    if [[ ! -f main.pdf ]]; then
        echo "✗ Build von $tag fehlgeschlagen" >&2
        return 1
    fi

    # 6. PDF an Zielort
    cp main.pdf "$OUT_DIR/${md_file%.md}.pdf"
    local size
    size=$(stat -c%s "$OUT_DIR/${md_file%.md}.pdf")
    echo "✓ $OUT_DIR/${md_file%.md}.pdf ($size Bytes)"
}

# Hauptprogramm
case "${1:-}" in
    "")
        echo "Verwendung: $0 <tag1|tag2|...|all>" >&2
        exit 1
        ;;
    all)
        for tag in tag1 tag2 tag3 tag4; do
            build_tag "$tag"
        done
        ;;
    *)
        build_tag "$1"
        ;;
esac
