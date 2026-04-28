#!/usr/bin/env bash
# Baut das Buch in einem Container, sodass die lokale Maschine
# weder TeX Live noch Pygments installiert haben muss.
#
# Engine-Auswahl: bevorzugt Apples "container" (nativ auf Apple
# Silicon), Fallback ist "docker". Beide sprechen dasselbe OCI-Image,
# das Dockerfile ist also identisch.
#
# Aufruf:
#   build/in-container.sh           → baut das Buch (default)
#   build/in-container.sh test-code → führt nur die Snippet-Prüfung aus
#   build/in-container.sh clean     → räumt im Container auf
#   ENGINE=docker build/in-container.sh   → erzwingt Docker

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_TAG="redundancy-book:latest"

# --- Engine-Auswahl ---
if [[ -n "${ENGINE:-}" ]]; then
    : # via Umgebungsvariable explizit gesetzt
elif command -v container >/dev/null 2>&1; then
    ENGINE="container"
elif command -v docker >/dev/null 2>&1; then
    ENGINE="docker"
else
    echo "✗ Weder Apples 'container' noch 'docker' gefunden." >&2
    echo "  Installiere eine OCI-kompatible Container-Engine." >&2
    exit 1
fi

echo "── Container-Engine: $ENGINE"

# --- Image bauen, falls nötig ---
# Beide CLIs verstehen `images inspect` analog. Wir prüfen nicht
# zu fein und bauen einfach immer; Layer-Caching macht den Bau
# nach dem ersten Mal sehr schnell.
echo "── Image bauen (Cache greift, falls Dockerfile unverändert)"
"$ENGINE" build -t "$IMAGE_TAG" -f "$REPO_ROOT/build/Dockerfile" "$REPO_ROOT"

# --- Container starten und make-Target ausführen ---
# Repo wird unter /work gemountet. Default-Target ist `make`
# (aus dem CMD im Dockerfile); abweichende Argumente werden weitergegeben.
echo "── Buch bauen"
exec "$ENGINE" run --rm \
    -v "$REPO_ROOT:/work" \
    -w /work \
    "$IMAGE_TAG" \
    make "$@"
