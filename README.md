# NeuroArt

Erzeuge digitale Neurokunst im Stil von Greg Dunn. Das Skript `neuro_art.py` generiert ein neuronenähnliches Liniengeflecht auf dunklem Hintergrund mit goldenen Akzenten und speichert das Ergebnis als PNG.

## Voraussetzungen

- Python 3.9+
- Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

## Nutzung

```bash
python neuro_art.py --width 1920 --height 1080 --seed 42 --output output/neuro_art.png
```

Parameter:
- `--width` / `--height`: Größe des Bildes.
- `--seed`: Startwert für reproduzierbare Zufallsstrukturen.
- `--output`: Pfad für das gespeicherte Bild.

Nach dem Lauf findest du das finale Kunstwerk unter dem angegebenen Ausgabe-Pfad.
