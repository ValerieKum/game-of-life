from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from common.viz import (PALETTE, card_figure, caption, save_animation,
                        use_headless_if_saving)

# ---- tunables -------------------------------------------------------------
GRID = 64
DENSITY = 0.18         # fraction of random live cells in the soup
TOTAL_FRAMES = 150
SEED_GLIDER_GUN = True


def gosper_glider_gun(grid):
    """Stamp a Gosper glider gun near the top-left — it fires forever."""
    cells = [
        (5, 1), (5, 2), (6, 1), (6, 2),
        (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (9, 13),
        (3, 14), (9, 14), (6, 15), (4, 16), (8, 16), (5, 17), (6, 17),
        (7, 17), (6, 18),
        (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22),
        (2, 23), (6, 23), (1, 25), (2, 25), (6, 25), (7, 25),
        (3, 35), (4, 35), (3, 36), (4, 36),
    ]
    for r, c in cells:
        if r < grid.shape[0] and c < grid.shape[1]:
            grid[r, c] = 1


def neighbours(g):
    """Count of 8-neighbours for every cell, via rolled sums (toroidal)."""
    total = np.zeros_like(g)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            total += np.roll(np.roll(g, dr, 0), dc, 1)
    return total


def step(g):
    n = neighbours(g)
    return ((n == 3) | ((g == 1) & (n == 2))).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", metavar="OUT.gif")
    args = ap.parse_args()
    use_headless_if_saving(args.save)

    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.colors import LinearSegmentedColormap

    g = (np.random.rand(GRID, GRID) < DENSITY).astype(np.uint8)
    if SEED_GLIDER_GUN:
        gosper_glider_gun(g)

    cmap = LinearSegmentedColormap.from_list(
        "life", [PALETTE["bg"], PALETTE["pink"], PALETTE["hot"]])

    fig, ax = card_figure()
    # age buffer: cells that have been alive longer glow hotter
    age = np.zeros((GRID, GRID), dtype=np.float64)
    img = ax.imshow(age, cmap=cmap, vmin=0, vmax=1, interpolation="nearest")
    txt = caption(ax, "")
    state = {"g": g}

    def render(frame):
        state["g"] = step(state["g"])
        nonlocal age
        age = np.clip(age * 0.82 + state["g"], 0, 1)
        img.set_array(age)
        txt.set_text(f"gen {frame:>3}   pop {int(state['g'].sum()):>4}")
        return img, txt

    anim = FuncAnimation(fig, render, frames=TOTAL_FRAMES, interval=60,
                         blit=True)

    if args.save:
        save_animation(anim, args.save, fps=20)
    else:
        plt.show()


if __name__ == "__main__":
    main()
