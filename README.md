# NeuroArt

Erzeuge digitale Neurokunst im Stil von Greg Dunn. Das Skript `neuro_art.py` generiert ein neuronenähnliches Liniengeflecht auf
dunklem Hintergrund mit goldenen Akzenten und speichert das Ergebnis als PNG.

## Voraussetzungen

- Python 3.9+
- (Optional) eigenes virtuelles Environment, damit die Abhängigkeiten isoliert bleiben:
  ```bash
  python -m venv .venv
  source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
  ```
- Abhängigkeiten installieren (Pillow wird für die Bildausgabe benötigt):
  ```bash
  pip install -r requirements.txt
  ```
  Falls die Internetverbindung blockiert ist, kannst du auch ein lokal gespeichertes Pillow-Wheel installieren, z. B.:
  ```bash
  pip install Pillow-10.3.0-cp311-cp311-manylinux_2_28_x86_64.whl
  ```

## Nutzung

1. Lege den Ausgabepfad fest und stelle sicher, dass der Ordner existiert (hier `output/`):
   ```bash
   mkdir -p output
   ```
2. Starte das Skript mit den gewünschten Parametern:
   ```bash
   python neuro_art.py --width 1920 --height 1080 --seed 42 --output output/neuro_art.png
   ```
3. Das fertige Bild findest du anschließend unter dem angegebenen Pfad.

### Wichtige Parameter

- `--width` / `--height`: Größe des Bildes in Pixeln.
- `--seed`: Startwert für reproduzierbare Zufallsstrukturen.
- `--output`: Dateipfad für das gespeicherte PNG.

Tipp: Weitere Optionen oder Standardwerte kannst du jederzeit mit `python neuro_art.py --help` anzeigen.
