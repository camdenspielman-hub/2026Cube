"""Shared helpers for the 2026 Cube simulators: load cards, colors, lands."""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, HERE)

from tags import TAGS  # noqa: E402
from ratings import RATINGS  # noqa: E402

PAIR_ARCHETYPE = {
    frozenset("WU"): "WU Blink", frozenset("UB"): "UB Seek Out", frozenset("UR"): "UR Spells",
    frozenset("UG"): "UG Ramp", frozenset("BR"): "BR Sacrifice", frozenset("BG"): "BG Blight",
    frozenset("RG"): "RG Stompy", frozenset("RW"): "RW Equipment", frozenset("WB"): "WB Ninjas",
    frozenset("GW"): "GW Counters",
}
PAIRS = list(PAIR_ARCHETYPE)
BASIC_FOR = {"W": "Plains", "U": "Island", "B": "Swamp", "R": "Mountain", "G": "Forest"}


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace('"', "").replace("'", "")


def short(name):
    return name.split(" // ")[0]


def load_cube(path=None, pool_json=None):
    """Return list of card dicts for a cube list file (default cube/cube_list.txt).

    Card data comes from data/cube_cards.json, or from a full eligible-pool JSON
    (the output of tools/build_pool.py) when pool_json is given, so older or
    hypothetical lists can be simulated too."""
    path = path or os.path.join(ROOT, "cube", "cube_list.txt")
    if pool_json:
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        from export_data import export_card
        pool = json.load(open(pool_json))
        data = [export_card(oid, e) for oid, e in pool.items()]
    else:
        data = json.load(open(os.path.join(ROOT, "data", "cube_cards.json"), encoding="utf-8"))
    by = {}
    for c in data:
        by[norm(c["name"])] = c
        by[norm(short(c["name"]))] = c
    extra = {}
    cards, section = [], None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            section = line[3:]
            continue
        c = by.get(norm(line)) or extra.get(norm(line))
        if c is None:
            raise KeyError(line)
        cards.append(make_card(c, section))
    return cards


def make_card(c, section):
    name = c["name"]
    tl = c["type_line"]
    main_type = tl.split(" // ")[0]
    cost = c.get("mana_cost") or ""
    front_cost = cost.split(" // ")[0]
    ci = set(c.get("color_identity", []))
    is_land = "Land" in main_type and "Creature" not in main_type
    card = {
        "name": name, "short": short(name), "section": section, "type": tl,
        "is_land": is_land, "is_creature": "Creature" in main_type,
        "cmc": c.get("cmc", 0), "cost": front_cost, "ci": ci,
        "tags": TAGS.get(short(name)) or TAGS.get(name) or [],
        "rating": RATINGS.get(short(name)) or RATINGS.get(name),
        "text": c.get("oracle_text") or "",
        "power": c.get("power"), "toughness": c.get("toughness"),
    }
    card["pips"] = pips(front_cost)
    card["need"] = set(card["pips"]["fixed"])
    card["hyb"] = [set(h) for h in card["pips"]["hybrid"]]
    # colors used for draft commitment: what you need to cast it, plus hybrid options
    card["commit"] = card["need"] | (set().union(*card["hyb"]) if card["hyb"] and not card["need"] else set())
    if is_land:
        card["land"] = land_profile(card)
    return card


def castable(card, colors):
    """Can this card be cast using only these colors (hybrid satisfied by either)?"""
    if not card["need"] <= colors:
        return False
    return all(h & colors for h in card["hyb"])


def pips(cost):
    """Colored pip counts of a mana cost like {1}{W}{U/B}. Hybrid counts as either."""
    out, hybrid = {}, []
    for sym in re.findall(r"\{([^}]+)\}", cost):
        if sym in "WUBRG":
            out[sym] = out.get(sym, 0) + 1
        elif "/" in sym:
            parts = [p for p in sym.split("/") if p in "WUBRG"]
            if parts and not any(p.isdigit() for p in sym.split("/")):
                hybrid.append(tuple(parts))
            # {2/W} style counts as generic for castability purposes
    return {"fixed": out, "hybrid": hybrid}


def land_profile(card):
    """Classify a land for the mana simulator."""
    t = card["text"]
    colors = sorted(card["ci"])
    if "As this land enters, you may pay 2 life" in t:
        kind = "shock"
    elif "unless you control two or more other lands" in t:
        kind = "slow"
    elif "Activate only if this land entered this turn or if you control a basic land" in t:
        kind = "basiccheck_msh"
    elif "unless you control two or more basic lands" in t:
        kind = "typedcheck"
    elif "unless you control a planeswalker" in t:
        kind = "pwcheck"
    elif "Search your library for a basic land card, put it onto the battlefield tapped" in t:
        kind = "fetchbasic"
    elif "This land enters tapped" in t and len(colors) == 2:
        kind = "tapped"
    elif "{1}, {T}: Add one mana of any color" in t:
        kind = "filter_any"
    else:
        kind = "colorless"
    return {"kind": kind, "colors": colors}
