#!/usr/bin/env python3
"""Download every printing in the given Scryfall sets.

Usage: python3 tools/fetch_sets.py <out_dir> <set code> [<set code> ...]
Writes <out_dir>/<code>.json (a list of Scryfall card objects) per set and
skips sets that are already downloaded.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HEADERS = {"User-Agent": "2026CubeBuilder/1.0", "Accept": "application/json"}


def get(url):
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                return None
            time.sleep(2 ** attempt)
        except Exception:  # network hiccup: back off and retry
            time.sleep(2 ** attempt)
    raise RuntimeError(f"failed to fetch {url}")


def main(out_dir, codes):
    os.makedirs(out_dir, exist_ok=True)
    for code in codes:
        path = os.path.join(out_dir, f"{code}.json")
        if os.path.exists(path):
            continue
        query = urllib.parse.quote(f"e:{code}")
        url = (f"https://api.scryfall.com/cards/search?q={query}&unique=prints&order=set"
               "&include_extras=true&include_variations=true")
        cards = []
        while url:
            page = get(url)
            if page is None:
                break
            cards.extend(page["data"])
            url = page.get("next_page") if page.get("has_more") else None
            time.sleep(0.12)  # Scryfall asks for <10 requests/second
        json.dump(cards, open(path, "w"))
        print(code, len(cards), flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
