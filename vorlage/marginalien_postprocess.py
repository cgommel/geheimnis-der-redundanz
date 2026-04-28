#!/usr/bin/env python3
r"""
Postprozessor für die pandoc-erzeugte body.tex.

Wandelt Aufgaben-Überschriften in Marginalien-Marker um:

  \subsubsection{✏️ Bleistiftübung 3 -- Parität von Hand}\label{...}
                          ↓
  \bleistiftuebung{3}{Parität von Hand}

Genauso für 💻 Python-Einheit und 🛠️ Werkzeug-Check.

Aufruf:
  python3 marginalien_postprocess.py body.tex
"""

import re
import sys
from pathlib import Path

# Variation Selector U+FE0F kommt manchmal direkt nach den Emojis vor.
# Wir akzeptieren ihn optional.
VS = '\uFE0F?'

PATTERNS = [
    # ✏️ Bleistiftübung N – Titel
    (
        re.compile(
            r'\\subsubsection\{✏' + VS + r'\s*Bleistiftübung\s*(\d+)\s*[-–—]+\s*([^}]+)\}'
            r'(?:\\label\{[^}]*\})?',
            re.UNICODE
        ),
        lambda m: r'\bleistiftuebung{%s}{%s}' % (m.group(1), m.group(2).strip())
    ),
    # 💻 Python-Einheit N – Titel
    (
        re.compile(
            r'\\subsubsection\{💻' + VS + r'\s*Python-Einheit\s*(\d+)\s*[-–—]+\s*([^}]+)\}'
            r'(?:\\label\{[^}]*\})?',
            re.UNICODE
        ),
        lambda m: r'\pythoneinheit{%s}{%s}' % (m.group(1), m.group(2).strip())
    ),
    # 🛠️ Werkzeug-Check: Titel
    (
        re.compile(
            r'\\subsubsection\{🛠' + VS + r'\s*Werkzeug-Check:\s*([^}]+)\}'
            r'(?:\\label\{[^}]*\})?',
            re.UNICODE
        ),
        lambda m: r'\werkzeugcheck{%s}' % m.group(1).strip()
    ),
    # Auch \paragraph-Variante (kommt vor bei tieferer Verschachtelung in pandoc)
    (
        re.compile(
            r'\\paragraph\{✏' + VS + r'\s*Bleistiftübung\s*(\d+)\s*[-–—]+\s*([^}]+)\}'
            r'(?:\\label\{[^}]*\})?',
            re.UNICODE
        ),
        lambda m: r'\bleistiftuebung{%s}{%s}' % (m.group(1), m.group(2).strip())
    ),
    (
        re.compile(
            r'\\paragraph\{💻' + VS + r'\s*Python-Einheit\s*(\d+)\s*[-–—]+\s*([^}]+)\}'
            r'(?:\\label\{[^}]*\})?',
            re.UNICODE
        ),
        lambda m: r'\pythoneinheit{%s}{%s}' % (m.group(1), m.group(2).strip())
    ),
]


def postprocess(text: str) -> tuple[str, int]:
    """Wendet alle Regeln an und gibt (neuen Text, Ersetzungs-Anzahl) zurück."""
    total = 0
    for pat, repl in PATTERNS:
        text, n = pat.subn(repl, text)
        total += n
    return text, total


def main():
    if len(sys.argv) != 2:
        print("Usage: marginalien_postprocess.py <body.tex>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    original = path.read_text(encoding='utf-8')
    new, count = postprocess(original)

    if count == 0:
        print(f"Hinweis: Keine Aufgaben-Überschriften gefunden in {path}.")
    else:
        print(f"{count} Aufgaben-Überschriften in Marginalien umgewandelt.")

    path.write_text(new, encoding='utf-8')


if __name__ == '__main__':
    main()
