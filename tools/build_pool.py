#!/usr/bin/env python3
"""Build the eligible card pool for the 2026 Cube from Scryfall set dumps.

Usage:
    python3 tools/fetch_sets.py raw ecl ecc pecl tmt tmc pza sos soc soa psos \
        msh msc hob hoc fra frc pfra trk trc sds
    python3 tools/build_pool.py raw data/eligible_pool.json

Eligibility rules (from the cube brief):
  * Any card printed in one of the seven 2026 main sets is eligible, whether it
    is new or a reprint (e.g. the shocklands in Star Trek, Nameless Inversion
    in Lorwyn Eclipsed).
  * A card that first appeared in a 2026 supplemental product tied to one of
    those sets (Commander decks, the TMNT / Hobbit "Eternal" decks, the Marvel
    Jumpstart-style Commander product, promos) is eligible.
  * A reprint that appears ONLY in a supplemental product is not eligible
    (e.g. Palace Jailer in MSC, The One Ring in HOC, Armageddon in the
    Mystical Archive).
  * Excluded entirely: Mystery Booster Commander, The Zeta Set (all reprints),
    Alchemy (digital only), tokens, art cards, basic lands, and the generic
    MagicFest / WPN promos that are not tied to any of the seven sets.
"""
import collections
import json
import os
import sys

MAIN = ["ecl", "tmt", "sos", "msh", "hob", "fra", "trk"]
SUPPLEMENTAL = ["ecc", "tmc", "soc", "msc", "hoc", "frc", "trc",
                "pecl", "psos", "pfra", "pza", "sds", "soa"]


def main(raw_dir, out_path):
    by_oracle = collections.defaultdict(list)
    for code in MAIN + SUPPLEMENTAL:
        path = os.path.join(raw_dir, f"{code}.json")
        if not os.path.exists(path):
            print("missing", path, file=sys.stderr)
            continue
        for card in json.load(open(path)):
            oid = card.get("oracle_id") or (card.get("card_faces") or [{}])[0].get("oracle_id")
            if oid:
                by_oracle[oid].append(card)

    pool, counts = {}, collections.Counter()
    for oid, prints in by_oracle.items():
        first = prints[0]
        type_line = first.get("type_line", "")
        if ("Token" in type_line or type_line.startswith("Basic Land")
                or first.get("layout") in ("token", "double_faced_token", "art_series", "emblem")
                or first.get("digital")):
            continue
        sets = sorted({p["set"] for p in prints})
        in_main = [s for s in sets if s in MAIN]
        new_supp = sorted({p["set"] for p in prints if p["set"] in SUPPLEMENTAL and not p.get("reprint")})
        if in_main:
            why = "main-set printing"
        elif new_supp:
            why = "new card in supplemental product"
        else:
            counts["excluded: supplemental-only reprint"] += 1
            continue
        counts[why] += 1
        rep = sorted(prints, key=lambda p: (p["set"] not in MAIN, bool(p.get("reprint")) and not in_main,
                                            p.get("promo", False),
                                            p.get("frame_effects") is not None, p["set"],
                                            len(p["collector_number"]), p["collector_number"]))[0]
        pool[oid] = {"why": why, "sets": sets, "card": rep}

    json.dump(pool, open(out_path, "w"))
    for k, v in counts.items():
        print(f"{k}: {v}")
    print("eligible:", len(pool))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
