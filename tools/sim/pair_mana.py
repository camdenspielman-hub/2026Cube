#!/usr/bin/env python3
"""Castability of real drafted decks, per color pair, using the lands each bot drafted.

Usage: python3 tools/sim/pair_mana.py [--drafts 40] [--trials 800] [--list cube/cube_list.txt]
"""
import argparse
import collections
import random
import statistics

import draft_sim
from cubelib import load_cube
from land_test import basics_for
from mana_sim import simulate, spell_profile


def deck_lands(deck):
    lands = []
    for l in deck["lands"] + deck["utility_lands"]:
        lands.append(dict(l["land"], name=l["short"]))
    colors = set(deck["pair"]) | ({deck["splash"]} if deck["splash"] else set())
    spells = [spell_profile(c) for c in deck["cards"]]
    main_colors = set(deck["pair"])
    return lands + basics_for(spells, main_colors, 17 - len(lands)), spells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts", type=int, default=40)
    ap.add_argument("--trials", type=int, default=800)
    ap.add_argument("--list", default=None)
    ap.add_argument("--seed", type=int, default=500)
    args = ap.parse_args()
    cards = load_cube(args.list)
    rng = random.Random(args.seed)
    res = collections.defaultdict(list)
    for d in range(args.drafts):
        st = draft_sim.run(cards, 1, args.seed + d)
        for deck in st["decks"]:
            lands, spells = deck_lands(deck)
            key = "".join(x for x in "WUBRG" if x in deck["pair"]) + ("+" + deck["splash"] if deck["splash"] else "")
            r = simulate(spells, lands, trials=args.trials, seed=rng.randrange(10**6))
            r["duals"] = len(deck["lands"])
            res[key[:2] if "+" not in key else "splash"].append(r)
    print(f"{'pair':7} {'decks':>5} {'duals':>6} {'on-curve T2-5':>14} {'mana T1-5':>10} {'color-screw T4':>15}")
    allr = []
    for k in sorted(res, key=lambda k: (k == "splash", k)):
        v = res[k]
        allr += v
        print(f"{k:7} {len(v):5d} {statistics.mean(r['duals'] for r in v):6.2f} {100 * statistics.mean(r['on_curve'] for r in v):13.1f}% "
              f"{statistics.mean(r['mana_t1_5'] for r in v):10.2f} {100 * statistics.mean(r['screw_t4'] for r in v):14.1f}%")
    print(f"{'ALL':7} {len(allr):5d} {statistics.mean(r['duals'] for r in allr):6.2f} {100 * statistics.mean(r['on_curve'] for r in allr):13.1f}% "
          f"{statistics.mean(r['mana_t1_5'] for r in allr):10.2f} {100 * statistics.mean(r['screw_t4'] for r in allr):14.1f}%")


if __name__ == "__main__":
    main()
