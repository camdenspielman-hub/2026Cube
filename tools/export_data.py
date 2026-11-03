#!/usr/bin/env python3
"""Export data/cube_cards.json and data/eligible_pool.csv.

Usage: python3 tools/export_data.py <eligible_pool.json from build_pool.py>
"""
import csv
import json
import os
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().replace('"', "").replace("'", "")


def faces(c):
    if "card_faces" in c and (c.get("layout") not in ("split", "flip", "adventure") or "oracle_text" not in c):
        return c["card_faces"]
    return None


def joined(c, key):
    f = faces(c)
    return c.get(key) if not f else " // ".join(x.get(key, "") for x in f)


def export_card(oid, entry):
    c = entry["card"]
    f = faces(c)
    img = c.get("image_uris") or (c.get("card_faces") or [{}])[0].get("image_uris") or {}
    back = None
    if c.get("card_faces") and len(c["card_faces"]) > 1 and c["card_faces"][1].get("image_uris"):
        back = c["card_faces"][1]["image_uris"].get("normal")
    colors = c.get("colors")
    if colors is None:
        colors = (c.get("card_faces") or [{}])[0].get("colors", [])
    out = {
        "name": c["name"], "oracle_id": oid, "mana_cost": joined(c, "mana_cost"),
        "cmc": c.get("cmc", 0), "type_line": c.get("type_line", ""),
        "oracle_text": c.get("oracle_text") if not f else "\n//\n".join(x.get("oracle_text", "") for x in f),
        "power": c.get("power"), "toughness": c.get("toughness"), "loyalty": c.get("loyalty"),
        "colors": colors, "color_identity": c.get("color_identity", []), "layout": c.get("layout"),
        "set": c["set"], "set_name": c.get("set_name"), "collector_number": c["collector_number"],
        "rarity": c["rarity"], "released_at": c.get("released_at"), "eligibility": entry["why"],
        "printed_in_2026": entry["sets"], "image": img.get("normal"), "image_small": img.get("small"),
        "image_back": back, "scryfall_uri": c.get("scryfall_uri"),
    }
    if f:
        out["faces"] = [{k: x.get(k) for k in ("name", "mana_cost", "type_line", "oracle_text",
                                                "power", "toughness", "loyalty")} for x in f]
    return out


def main(pool_path):
    pool = json.load(open(pool_path))
    by_name = {}
    for oid, e in pool.items():
        by_name[norm(e["card"]["name"])] = oid
        by_name.setdefault(norm(e["card"]["name"].split(" // ")[0]), oid)

    cube, section = [], None
    for line in open(os.path.join(ROOT, "cube", "cube_list.txt"), encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            section = line[3:]
            continue
        oid = by_name[norm(line)]
        card = export_card(oid, pool[oid])
        card["section"] = section
        cube.append(card)
    json.dump(cube, open(os.path.join(ROOT, "data", "cube_cards.json"), "w", encoding="utf-8"),
              indent=1, ensure_ascii=False)

    in_cube = {c["oracle_id"] for c in cube}
    with open(os.path.join(ROOT, "data", "eligible_pool.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["name", "mana_cost", "type_line", "color_identity", "rarity", "set",
                    "collector_number", "eligibility", "printed_in_2026_products", "in_cube"])
        for oid, e in sorted(pool.items(), key=lambda kv: (kv[1]["card"]["set"], kv[1]["card"]["name"])):
            c = e["card"]
            w.writerow([c["name"], joined(c, "mana_cost"), c.get("type_line", ""),
                        "".join(c.get("color_identity", [])) or "C", c["rarity"], c["set"],
                        c["collector_number"], e["why"], " ".join(e["sets"]),
                        "yes" if oid in in_cube else ""])
    print(f"cube cards: {len(cube)}, eligible pool: {len(pool)}")


if __name__ == "__main__":
    main(sys.argv[1])
