#!/usr/bin/env python3
"""Goldfish mana simulator: how well does a 40-card deck's mana base cast its spells?

For each trial: shuffle, draw 7 on the play (London mulligan to 6 if the hand
has <2 or >5 lands), then play turns 1-6. Each turn the bot plays the land that
lets it spend the most mana this turn (preferring tapped lands when that costs
nothing), then casts the spells that use the most mana given exact colored pips.
Mana creatures and rocks are ignored (a conservative baseline).

Metrics per deck configuration:
  on-curve  : P(spent >= T mana on turn T), averaged over turns 2-5
  mana T1-5 : mean total mana spent on turns 1-5 (tempo)
  screw T4  : P(on turn 4 a spell with MV <= lands is stuck only because of colors)
  life      : mean life paid to shocklands by turn 6
"""
import itertools
import random
import statistics

from cubelib import BASIC_FOR


def land_colors(land, state):
    """Colors this land can produce right now (set; 'C' = colorless only)."""
    kind, cols = land["kind"], set(land["colors"])
    if kind == "basic":
        return cols
    if kind == "basiccheck_msh":
        if land.get("entered_this_turn") or any(l["kind"] == "basic" for l in state["lands"]):
            return cols
        return {"C"}
    if kind in ("colorless", "fetchbasic", "filter_any"):
        return {"C"}
    return cols


def enters_tapped(land, state):
    kind = land["kind"]
    if kind in ("basic", "shock", "basiccheck_msh", "colorless", "filter_any"):
        return False
    if kind == "slow":
        return len(state["lands"]) < 2
    if kind == "typedcheck":
        return sum(l["kind"] == "basic" for l in state["lands"]) < 2
    if kind in ("tapped", "pwcheck", "turbulent"):
        return True
    if kind == "fetchbasic":
        return True
    return False


def can_pay(spells, sources):
    """Can the list of spells be paid by the given list of source color-sets?"""
    need, generic = [], 0
    for s in spells:
        for col, n in s["fixed"].items():
            need += [{col}] * n
        for h in s["hybrid"]:
            need.append(set(h))
        generic += s["generic"]
    if len(need) + generic > len(sources):
        return False
    # match colored pips to sources (small sizes: backtracking)
    need.sort(key=len)
    used = [False] * len(sources)

    def bt(i):
        if i == len(need):
            return True
        for j, src in enumerate(sources):
            if not used[j] and (src & need[i]):
                used[j] = True
                if bt(i + 1):
                    return True
                used[j] = False
        return False
    return bt(0)


def best_cast(hand_spells, sources):
    """Max mana value castable from hand with these sources (greedy over subsets)."""
    best, best_set = 0, ()
    spells = [s for s in hand_spells if s["cmc"] <= len(sources)]
    spells.sort(key=lambda s: -s["cmc"])
    for r in range(1, min(4, len(spells)) + 1):
        for combo in itertools.combinations(spells, r):
            tot = sum(s["cmc"] for s in combo)
            if tot <= len(sources) and tot > best and can_pay(combo, sources):
                best, best_set = tot, combo
    return best, best_set


def simulate(spells, lands, trials=4000, seed=7, turns=6):
    rng = random.Random(seed)
    deck = [("spell", s) for s in spells] + [("land", l) for l in lands]
    on_curve = {t: 0 for t in range(2, 6)}
    mana_total, screw4, life_paid = [], 0, []
    for _ in range(trials):
        lib = deck[:]
        rng.shuffle(lib)
        hand = lib[:7]
        nl = sum(k == "land" for k, _ in hand)
        if nl < 2 or nl > 5:
            rng.shuffle(lib)
            hand = lib[:7]
            # bottom one card: a land if >=4 lands else a spell with highest MV
            nl = sum(k == "land" for k, _ in hand)
            if nl >= 4:
                idx = next(i for i, (k, _) in enumerate(hand) if k == "land")
            else:
                idx = max(range(7), key=lambda i: hand[i][1]["cmc"] if hand[i][0] == "spell" else -1)
            hand.pop(idx)
        lib = lib[7:]  # (a mulliganed card goes to the bottom and is never reached)
        state = {"lands": [], "tapped_now": set()}
        total, life = 0, 0
        for t in range(1, turns + 1):
            if t > 1 and lib:
                hand.append(lib.pop(0))
            hand_lands = [x for k, x in hand if k == "land"]
            hand_spells = [x for k, x in hand if k == "spell"]
            choice = None
            for cand in hand_lands:
                tapped = enters_tapped(cand, state)
                fetched = cand["kind"] == "fetchbasic"
                temp = state | {"lands": state["lands"] + [dict(cand, entered_this_turn=True)]}
                srcs = [land_colors(l, temp) for l in state["lands"]]
                if not tapped:
                    srcs.append(land_colors(dict(cand, entered_this_turn=True), temp))
                val, _ = best_cast(hand_spells, srcs)
                # prefer: most mana spent now; then a tapped land (keep untapped ones for later);
                # then the land producing the most colors
                pref = (val, 1 if tapped else 0, len(cand["colors"]) + (0.5 if fetched else 0))
                if choice is None or pref > choice[0]:
                    choice = (pref, cand)
            if choice:
                cand = choice[1]
                hand.remove(("land", cand))
                if cand["kind"] == "fetchbasic":
                    # crack immediately for the most-needed basic color, enters tapped
                    want = needed_color(hand_spells, state["lands"])
                    newl = {"kind": "basic", "colors": [want], "name": BASIC_FOR[want], "tapped_turn": t}
                    state["lands"].append(newl)
                else:
                    newl = dict(cand)
                    if enters_tapped(cand, state):
                        newl["tapped_turn"] = t
                    if cand["kind"] == "shock":
                        life += 2 if needs_untapped(hand_spells, state, cand) else 0
                    newl["entered_this_turn"] = True
                    state["lands"].append(newl)
            srcs = [land_colors(l, state) for l in state["lands"] if l.get("tapped_turn") != t]
            for l in state["lands"]:
                l.pop("entered_this_turn", None)
            val, cast = best_cast(hand_spells, srcs)
            for s in cast:
                hand.remove(("spell", s))
            if t <= 5:
                total += val
            if 2 <= t <= 5 and val >= t:
                on_curve[t] += 1
            if t == 4:
                n_lands = len(srcs)
                stuck = [s for k, s in hand if k == "spell" and s["cmc"] <= n_lands]
                if val < n_lands and stuck and not any(can_pay([s], srcs) for s in stuck):
                    screw4 += 1
        mana_total.append(total)
        life_paid.append(life)
    return {
        "on_curve": statistics.mean(on_curve[t] / trials for t in on_curve),
        "on_curve_by_turn": {t: on_curve[t] / trials for t in on_curve},
        "mana_t1_5": statistics.mean(mana_total),
        "screw_t4": screw4 / trials,
        "life": statistics.mean(life_paid),
    }


def needed_color(spells, lands):
    have = {c for l in lands for c in l["colors"]}
    counts = {}
    for s in spells:
        for c, n in s["fixed"].items():
            counts[c] = counts.get(c, 0) + n * (2 if c not in have else 1)
    if not counts:
        return next(iter(have)) if have else "W"
    return max(counts, key=counts.get)


def needs_untapped(spells, state, land):
    return any(s["cmc"] <= len(state["lands"]) for s in spells)


def spell_profile(card):
    import re
    fixed, hybrid, generic = {}, [], 0
    for sym in re.findall(r"\{([^}]+)\}", card["cost"]):
        if sym in "WUBRG":
            fixed[sym] = fixed.get(sym, 0) + 1
        elif sym.isdigit():
            generic += int(sym)
        elif "/" in sym:
            parts = sym.split("/")
            cols = [p for p in parts if p in "WUBRG"]
            if any(p.isdigit() for p in parts):
                generic += 1
            elif cols:
                hybrid.append(cols)
        elif sym == "C":
            generic += 1
    cmc = int(card["cmc"]) if "{X}" not in card["cost"] else int(card["cmc"]) + 1
    return {"name": card["short"], "fixed": fixed, "hybrid": hybrid, "generic": max(0, cmc - sum(fixed.values()) - len(hybrid)), "cmc": cmc}
