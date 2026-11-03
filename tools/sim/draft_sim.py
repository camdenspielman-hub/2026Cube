#!/usr/bin/env python3
"""8-player draft simulator for the 2026 Cube.

Bots draft 3 packs x 15 cards. Each pick is scored by card rating plus a
color-commitment bonus (that ramps up over the draft) plus an archetype-synergy
bonus for cards tagged with the bot's current pair archetype. After the draft
every bot builds the best 40-card deck it can (two colors, optional 1-3 card
splash) and the results are aggregated.

Usage: python3 tools/sim/draft_sim.py [--drafts 2000] [--seed 1] [--list cube/cube_list.txt]
       [--json out.json]
"""
import argparse
import collections
import json
import random
import statistics

from cubelib import PAIR_ARCHETYPE, PAIRS, castable, load_cube

LAND_BASE = {"shock": 3.0, "slow": 2.9, "basiccheck_msh": 2.7, "typedcheck": 2.7,
             "pwcheck": 2.2, "tapped": 2.0, "fetchbasic": 2.1, "filter_any": 2.2, "colorless": 1.8}


class Bot:
    def __init__(self, rng, noise):
        self.rng, self.noise = rng, noise
        self.pool = []
        self.color_w = collections.Counter()
        self.tag_n = collections.Counter()

    def top2(self):
        ranked = [c for c, _ in self.color_w.most_common() if self.color_w[c] > 0]
        return frozenset(ranked[:2])

    def score(self, card, pick_no):
        commit = min(1.0, pick_no / 16.0)
        top = self.top2()
        if card["is_land"]:
            prof = card["land"]
            base = LAND_BASE[prof["kind"]]
            cols = set(prof["colors"])
            if len(cols) == 2:
                inside = len(cols & top)
                return {2: base + 0.2, 1: base - 0.8, 0: base - 1.6}[inside] * (0.6 + 0.4 * commit)
            return base * (0.5 + 0.3 * commit)
        r = card["rating"] + self.rng.gauss(0, self.noise)
        ci = card["commit"]
        if ci:
            off = len(ci - top) if len(top) == 2 else max(0, len(ci) - 1 - (len(ci & top) > 0))
            if card["hyb"] and not card["need"] and ci & top:
                off = 0
            if off == 0:
                r += 0.7 * commit
            else:
                r -= 0.9 * commit * off
            if len(ci) >= 2:
                r -= 0.35 * (1 - commit)  # gold cards are less flexible early
        else:
            r += 0.05
        arch = PAIR_ARCHETYPE.get(top)
        if arch and arch in card["tags"]:
            r += commit * (0.15 + min(0.6, 0.06 * self.tag_n[arch]))
        return r

    def take(self, card):
        self.pool.append(card)
        if not card["is_land"]:
            for c in card["commit"]:
                self.color_w[c] += card["rating"] / len(card["commit"]) ** 0.5
        for t in card["tags"]:
            self.tag_n[t] += 1

    def pick(self, pack, pick_no):
        ranked = sorted(pack, key=lambda c: -self.score(c, pick_no))
        best = ranked[0]
        pack.remove(best)
        self.take(best)
        self.last_ranked = ranked
        return best


def deck_value(card, arch, n_arch, colors=None):
    v = card["rating"]
    if colors is not None and not card["ci"] <= colors and card["short"] not in ACTIVATION_ONLY:
        v -= 0.4  # castable, but its other half / transform / sneak color is missing
    if arch in card["tags"]:
        v += 0.25 + 0.04 * min(n_arch, 12)
    return v


def pick_curve(scored, size=23, max_five=5, max_six=3, min_two=5, max_splash=3):
    """Choose `size` spells by value like a sensible human builder: soft cap on
    5+ drops, hard cap on 6+ drops, and at least `min_two` plays of MV <= 2."""
    chosen, five, six, n_splash = [], 0, 0, 0
    rest = []
    for v, c, sp in scored:
        mv = c["cmc"]
        if len(chosen) == size or (sp and n_splash >= max_splash) or (mv >= 6 and six >= max_six):
            rest.append((v, c, sp))
            continue
        if mv >= 5 and five >= max_five and v < 3.6:
            rest.append((v, c, sp))
            continue
        chosen.append((v, c, sp))
        five += mv >= 5
        six += mv >= 6
        n_splash += sp
    cheap = [x for x in rest if x[1]["cmc"] <= 2 and x[0] >= 2.4 and not x[2]]
    while sum(1 for _, c, _ in chosen if c["cmc"] <= 2) < min_two and cheap:
        add = cheap.pop(0)
        worst = min((x for x in chosen if x[1]["cmc"] >= 4), key=lambda x: x[0], default=None)
        if worst is None or worst[0] - add[0] > 0.7:
            break
        chosen.remove(worst)
        chosen.append(add)
    return chosen


def build_deck(pool):
    """Pick the best 2-color (+ optional splash) 23-spell deck from a pool."""
    best = None
    nonlands = [c for c in pool if not c["is_land"]]
    lands = [c for c in pool if c["is_land"]]
    for pair in PAIRS:
        arch = PAIR_ARCHETYPE[pair]
        main = [c for c in nonlands if castable(c, set(pair))]
        n_arch = sum(arch in c["tags"] for c in main)
        for splash in [None] + [x for x in "WUBRG" if x not in pair]:
            colors = set(pair) | ({splash} if splash else set())
            fix_sources = 0
            if splash:
                fix_sources = sum(1 for l in lands if splash in l["land"]["colors"]
                                  and set(l["land"]["colors"]) & set(pair)) + \
                              sum(1 for l in lands if l["land"]["kind"] in ("filter_any", "fetchbasic")) + \
                              sum(1 for c in main if c["short"] in FIXERS)
                if fix_sources < 2:
                    continue
            scored = []
            for c in main:
                scored.append((deck_value(c, arch, n_arch, colors), c, False))
            if splash:
                for c in nonlands:
                    if castable(c, colors) and not castable(c, set(pair)):
                        scored.append((deck_value(c, arch, n_arch, colors) - 0.6 - 0.3 * c["pips"]["fixed"].get(splash, 0), c, True))
            scored.sort(key=lambda x: -x[0])
            chosen = pick_curve(scored)
            n_splash = sum(1 for _, _, sp in chosen if sp)
            filler = 23 - len(chosen)
            if splash and n_splash == 0:
                continue
            duals = [l for l in lands if set(l["land"]["colors"]) <= colors and len(l["land"]["colors"]) == 2
                     and (set(l["land"]["colors"]) <= set(pair) or splash in l["land"]["colors"])]
            score = sum(v for v, _, _ in chosen) + filler * 0.5 + 0.15 * len(duals)
            if best is None or score > best["score"]:
                best = {"score": score, "pair": pair, "splash": splash, "arch": arch,
                        "cards": [c for _, c, _ in chosen], "filler": filler,
                        "splash_cards": [c for _, c, s in chosen if s], "lands": duals}
    deck = best
    nonland = deck["cards"]
    # utility lands worth playing
    util = []
    for l in lands:
        k = l["land"]["kind"]
        if l in deck["lands"]:
            continue
        name = l["short"]
        if name in ("Skycoach Waypoint", "Hexhaven Dueling Arena") and sum("Prepared" in c["tags"] for c in nonland) >= 4:
            util.append(l)
        elif name == "Great Hall of the Biblioplex" and sum(("Instant" in c["type"] or "Sorcery" in c["type"]) for c in nonland) >= 8:
            util.append(l)
        elif k in ("filter_any", "fetchbasic") and deck["splash"]:
            util.append(l)
        elif k in ("pwcheck",) and set(l["land"]["colors"]) <= set(deck["pair"]):
            util.append(l)
    deck["utility_lands"] = util[:2]
    return deck


ACTIVATION_ONLY = {"Codie, Ravenous Codex", "Thanos, the Mad Titan"}

FIXERS = {"Bloom Tender", "Frog Butler", "Great Forest Druid", "H.E.R.B.I.E., Lovable Robot",
          "Firdoch Core", "Murmuring Volume", "Foraging Wickermaw", "Giant's Boulder", "Wood Elves"}


def run(cards, n_drafts, seed, noise=0.35):
    rng = random.Random(seed)
    stats = {
        "pairs": collections.Counter(), "splash": collections.Counter(),
        "picked_at": collections.defaultdict(list), "maindeck": collections.Counter(),
        "drafted": collections.Counter(), "arch_density": collections.defaultdict(list),
        "deck_rating": collections.defaultdict(list), "creatures": collections.defaultdict(list),
        "removal": collections.defaultdict(list), "filler": collections.Counter(),
        "duals": collections.defaultdict(list), "decks": [], "color_share": collections.Counter(),
        "first_pick": collections.Counter(), "pick_log": [],
    }
    for d in range(n_drafts):
        deck_cards = cards[:]
        rng.shuffle(deck_cards)
        packs = [deck_cards[i * 15:(i + 1) * 15] for i in range(24)]
        bots = [Bot(rng, noise) for _ in range(8)]
        pick_no = 0
        for rnd in range(3):
            held = [packs[rnd * 8 + p] for p in range(8)]
            direction = 1 if rnd != 1 else -1
            for i in range(15):
                for p in range(8):
                    card = bots[p].pick(held[p], pick_no)
                    if d == 0 and p == 0:
                        stats["pick_log"].append((rnd + 1, i + 1, card["name"], [c["name"] for c in bots[p].last_ranked[1:3]]))
                    stats["picked_at"][card["name"]].append(i + 1)
                    stats["drafted"][card["name"]] += 1
                    if pick_no == 0:
                        stats["first_pick"][card["name"]] += 1
                held = [held[(p - direction) % 8] for p in range(8)]
                pick_no += 1
        built = [build_deck(b.pool) for b in bots]
        pair_counts = collections.Counter(frozenset(x["pair"]) for x in built)
        for deck in built:
            shared = pair_counts[frozenset(deck["pair"])]
            stats.setdefault("contention", collections.defaultdict(list))[(deck["arch"], min(shared, 3))].append(
                (sum(deck["arch"] in c["tags"] for c in deck["cards"]), statistics.mean(c["rating"] for c in deck["cards"])))
            key = "".join(x for x in "WUBRG" if x in deck["pair"])
            stats["pairs"][key] += 1
            if deck["splash"]:
                stats["splash"][deck["splash"]] += 1
            arch = deck["arch"]
            stats["arch_density"][key].append(sum(arch in c["tags"] for c in deck["cards"]))
            stats["deck_rating"][key].append(statistics.mean(c["rating"] for c in deck["cards"]))
            stats["creatures"][key].append(sum(c["is_creature"] for c in deck["cards"]))
            stats["removal"][key].append(sum(("Removal" in c["tags"] or "Sweeper" in c["tags"] or "Counterspell" in c["tags"]) for c in deck["cards"]))
            stats["duals"][key].append(len(deck["lands"]))
            stats["filler"][deck["filler"] > 0] += 1
            for c in deck["cards"] + deck["lands"] + deck["utility_lands"]:
                stats["maindeck"][c["name"]] += 1
            for c in deck["cards"]:
                for col in c["ci"]:
                    stats["color_share"][col] += 1
            if d < 25:
                stats["decks"].append(deck)
    return stats


def report(cards, stats, n_drafts, top=25):
    out = []
    n_decks = n_drafts * 8
    out.append(f"Drafts: {n_drafts}  decks: {n_decks}")
    out.append("\nColor pairs chosen (share of decks, mean archetype cards in 23, mean card rating, creatures, interaction (removal+sweepers+counters), on-color duals):")
    for key, n in stats["pairs"].most_common():
        out.append(f"  {key:3} {100 * n / n_decks:5.1f}%  arch={statistics.mean(stats['arch_density'][key]):4.1f}  "
                   f"rating={statistics.mean(stats['deck_rating'][key]):.2f}  crea={statistics.mean(stats['creatures'][key]):4.1f}  "
                   f"interact={statistics.mean(stats['removal'][key]):4.1f}  duals={statistics.mean(stats['duals'][key]):.2f}")
    if "contention" in stats:
        out.append("\nArchetype under contention (decks of the same pair in one draft: 1 / 2 / 3+): mean archetype cards | mean rating")
        archs = sorted({a for a, _ in stats["contention"]})
        for a in archs:
            cells = []
            for k in (1, 2, 3):
                v = stats["contention"].get((a, k), [])
                cells.append(f"{statistics.mean(x for x, _ in v):4.1f} | {statistics.mean(y for _, y in v):.2f} (n={len(v)})" if v else "   -")
            out.append(f"  {a:14} " + "   ".join(cells))
    sp = sum(stats["splash"].values())
    out.append(f"\nDecks splashing a third color: {100 * sp / n_decks:.1f}%  {dict(stats['splash'])}")
    out.append(f"Decks short of 23 on-color playables: {100 * stats['filler'][True] / n_decks:.2f}%")
    tot = sum(stats["color_share"].values())
    out.append("Color share of maindeck card-colors: " + "  ".join(f"{c}:{100 * stats['color_share'][c] / tot:.1f}%" for c in "WUBRG"))
    rows = []
    for c in cards:
        nm = c["name"]
        picks = stats["picked_at"].get(nm, [])
        rows.append((stats["maindeck"][nm] / n_drafts, statistics.mean(picks) if picks else 99, nm, c["section"]))
    rows.sort()
    out.append(f"\nLowest maindeck rate (fraction of drafts where the card made a deck), avg pick within pack (1-15):")
    for md, ap, nm, sec in rows[:top]:
        out.append(f"  {md:5.2f}  pick {ap:5.1f}  {nm} [{sec}]")
    out.append(f"\nHighest maindeck rate:")
    for md, ap, nm, sec in rows[-10:]:
        out.append(f"  {md:5.2f}  pick {ap:5.1f}  {nm} [{sec}]")
    by_sec = collections.defaultdict(list)
    for md, ap, nm, sec in rows:
        by_sec[sec].append(md)
    out.append("\nMean maindeck rate by section: " + "  ".join(f"{s}:{statistics.mean(v):.2f}" for s, v in by_sec.items()))
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--drafts", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--list", default=None)
    ap.add_argument("--noise", type=float, default=0.35)
    ap.add_argument("--json", default=None)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--pool", default=None, help="eligible pool JSON, to simulate lists not in data/cube_cards.json")
    args = ap.parse_args()
    cards = load_cube(args.list, args.pool)
    missing = [c["name"] for c in cards if not c["is_land"] and c["rating"] is None]
    if missing:
        raise SystemExit(f"unrated: {missing}")
    st = run(cards, args.drafts, args.seed, args.noise)
    print(report(cards, st, args.drafts, args.top))
    if args.json:
        json.dump({"maindeck": st["maindeck"], "pairs": st["pairs"],
                   "picked_at": {k: statistics.mean(v) for k, v in st["picked_at"].items()}},
                  open(args.json, "w"), indent=1)
