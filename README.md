# Conway's Game of Life

Complex patterns emerging from four tiny rules on a grid of living and dead cells.

Part of my portfolio of small, from-scratch visualisations of computer-science ideas. Built on numpy and matplotlib, so every moving part is visible.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python game_of_life.py                  # live animated window
python game_of_life.py --save out.gif   # export a looping GIF
python game_of_life.py --save out.mp4   # smaller file, best for the web (needs ffmpeg)
```
