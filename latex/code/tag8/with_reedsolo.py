# Praxis: Reed-Solomon mit der reedsolo-Bibliothek.
# Installation einmalig:  pip install reedsolo
#
# Library übernimmt den vollständigen Encoder UND Decoder
# (auch ohne bekannte Fehlerpositionen — Berlekamp-Massey + Forney).

# region praxis
try:
    import reedsolo
except ImportError:
    print("reedsolo nicht installiert.  Installiere mit:")
    print("    pip install reedsolo")
    raise SystemExit(1)


# RS-Code mit 4 Prüfsymbolen — korrigiert bis zu 2 Symbol-Fehler
# oder bis zu 4 Auslöschungen.
rsc = reedsolo.RSCodec(4)

nachricht = b"GRETA"
codewort = rsc.encode(nachricht)
print(f"Original:   {nachricht}")
print(f"Codewort:   {codewort.hex()}")

# Zwei Symbole verfälschen — der Decoder soll das korrigieren
gestoert = bytearray(codewort)
gestoert[1] = 0xAB
gestoert[3] = 0xCD
print(f"Gestört:    {bytes(gestoert).hex()}")

# Decoder
korrigiert, _, fehlerpositionen = rsc.decode(bytes(gestoert))
print(f"Korrigiert: {korrigiert}")
print(f"Erkannte Fehlerpositionen: {fehlerpositionen}")
# endregion


# region grenze
# Was passiert jenseits der Korrekturkraft? Drei Symbol-Fehler bei
# nur 2 möglichen Korrekturen.
gestoert = bytearray(codewort)
gestoert[0] = 0x11
gestoert[1] = 0x22
gestoert[2] = 0x33

try:
    korrigiert, _, _ = rsc.decode(bytes(gestoert))
    print(f"Glück gehabt: {korrigiert}")
except reedsolo.ReedSolomonError as e:
    print(f"Decoder erkennt: {e}")

# Bei drei Fehlern hat der Decoder nicht genug Information — er
# kann das ursprüngliche Codewort nicht eindeutig rekonstruieren
# und meldet einen Fehler. Genau diese Schwelle entspricht der
# Theorie: ⌊(n-k)/2⌋ Fehler korrigierbar.
# endregion
