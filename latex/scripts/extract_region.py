#!/usr/bin/env python3
"""Extrahiert eine Region aus einer Python-Datei.

Region-Konvention in der Quelle (Marker am Zeilenanfang, evtl. mit
führenden Whitespace):

    # region <name>
    ... Inhalt ...
    # endregion

Aufruf:
    python3 extract_region.py <datei.py> <region-name>

Gibt den Inhalt der Region (ohne die Marker selbst) auf stdout aus.
Beendet mit Code 1, wenn die Region nicht gefunden wird.
"""
import re
import sys
from pathlib import Path


def extract(path: str, region: str) -> str:
    text = Path(path).read_text(encoding="utf-8")
    pattern = (
        rf"^[ \t]*#[ \t]*region[ \t]+{re.escape(region)}[ \t]*$"
        r"(?P<body>.*?)"
        r"^[ \t]*#[ \t]*endregion[ \t]*$"
    )
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        sys.exit(f"Region '{region}' in {path} nicht gefunden.")
    return match.group("body").strip("\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Aufruf: extract_region.py <datei.py> <region-name>")
    print(extract(sys.argv[1], sys.argv[2]))
