# Build-Image für "Das Geheimnis der Redundanz".
#
# Enthält die komplette Toolchain, die das Buch baut:
#   - TeX Live mit xelatex, latexmk, tcolorbox, fvextra, glossaries,
#     imakeidx, minted-Backend etc. (collection-latexextra in Debian-Sprache)
#   - DejaVu-Schriftfamilien (Serif, Sans, Sans Mono — fontspec-tauglich)
#   - Python 3 mit Pygments für minted
#   - make, latexmk
#
# Wird über build/in-container.sh aufgerufen. Sowohl Docker als auch
# Apples "container"-CLI bauen und starten dieses Image (OCI-konform).

FROM debian:trixie-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        texlive-xetex \
        texlive-latex-extra \
        texlive-fonts-recommended \
        texlive-fonts-extra \
        texlive-lang-german \
        texlive-pictures \
        texlive-science \
        texlive-plain-generic \
        texlive-extra-utils \
        latexmk \
        python3 \
        python3-pygments \
        fonts-dejavu \
        make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# Default: das Buch bauen. Beim Aufruf kann jedes andere make-Target
# als Argument mitgegeben werden (z. B. `make clean`).
CMD ["make"]
