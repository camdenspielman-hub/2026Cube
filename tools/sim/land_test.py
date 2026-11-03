#!/usr/bin/env python3
"""Compare third-dual options for a color pair using decks from simulated drafts.

For each sampled two-color deck we hold the 23 spells fixed and try several
17-land configurations, then report the mana-simulator metrics averaged over
the decks.

Usage: python3 tools/sim/land_test.py --pair BG --pair RW [--decks 24] [--trials 3000]
"""
import argparse
import random
import statistics

import draft_sim
from cubelib import load_cube
from mana_sim import simulate, spell_profile

CONFIGS = {
    "shock+slow+basics (2 duals)": [],
    "+ tapped dual (Turbulent/gain)": ["tapped"],
    "+ typed checkland (Vernal Fen-style)": ["typedcheck"],
    "+ Marvel basic-check dual": ["basiccheck_msh"],
    "+ Evolving Wilds-style fetch": ["fetchbasic"],
    "+ tapped dual + fetch": ["tapped", "fetchbasic"],
}


def basics_for(spells, colors, n):
    weight = {c: 0.0 for c in colors}
    for s in spells:
        for c, k in s["fixed"].items():
            if c in weight:
                weight[c] += k
        for h in s["hybrid"]:
            for c in h:
                if c in weight:
                    weight[c] += 0.5 / len(h)
    tot = sum(weight.values()) or 1
    counts = {c: int(round(n * w / tot)) for c, w in weight.items()}
    while sum(counts.values()) > n:
        counts[max(counts, key=counts.get)] -= 1
    while sum(counts.values()) < n:
        counts[min(counts, key=counts.get)] += 1
    out = []
    for c, k in counts.items():
        out += [{"kind": "basic", "colors": [c], "name": c}] * k
    return out


def lands_for(spells, colors, extra):
    duals = [{"kind": "shock", "colors": sorted(colors)}, {"kind": "slow", "colors": sorted(colors)}]
    for kind in extra:
        if kind == "fetchbasic":
            duals.append({"kind": "fetchbasic", "colors": []})
        else:
            duals.append({"kind": kind, "colors": sorted(colors)})
    return duals + basics_for(spells, colors, 17 - len(duals))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pair", action="append", required=True)
    ap.add_argument("--decks", type=int, default=24)
    ap.add_argument("--trials", type=int, default=3000)
    ap.add_argument("--list", default=None)
    args = ap.parse_args()
    cards = load_cube(args.list)
    rng = random.Random(3)
    wanted = {p: [] for p in args.pair}
    seed = 100
    while any(len(v) < args.decks for v in wanted.values()) and seed < 400:
        st = draft_sim.run(cards, 25, seed)
        for d in st["decks"]:
            key = "".join(x for x in "WUBRG" if x in d["pair"])
            for p in wanted:
                if set(p) == set(key) and not d["splash"] and len(wanted[p]) < args.decks:
                    wanted[p].append(d)
        seed += 1
    for p, decks in wanted.items():
        print(f"\n== {p}: {len(decks)} sampled decks, {args.trials} goldfish games each ==")
        print(f"{'configuration':40} {'on-curve T2-5':>14} {'mana T1-5':>10} {'color-screw T4':>15} {'shock life':>10}")
        for name, extra in CONFIGS.items():
            res = []
            for d in decks:
                spells = [spell_profile(c) for c in d["cards"]]
                lands = lands_for(spells, set(p), extra)
                res.append(simulate(spells, lands, trials=args.trials, seed=rng.randrange(10**6)))
            print(f"{name:40} {100 * statistics.mean(r['on_curve'] for r in res):13.1f}% "
                  f"{statistics.mean(r['mana_t1_5'] for r in res):10.2f} "
                  f"{100 * statistics.mean(r['screw_t4'] for r in res):14.1f}% "
                  f"{statistics.mean(r['life'] for r in res):10.2f}")


if __name__ == "__main__":
    main()
