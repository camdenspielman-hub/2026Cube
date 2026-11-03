# Testing & Revision Log

The first version of this cube (v1) was checked for eligibility, counts, and
synergy coverage, but it was never drafted or played. This document records
what I did next, what it found, and what changed. The scripts that produced
every number here are in [`tools/sim/`](tools/sim/) and can be re-run.

**Summary:** 57 cards changed (57 in, 57 out). Five rounds of simulation and
an independent review found these problems in v1:

* colors were imbalanced: black strongest, green weakest;
* BG and BR had the thinnest archetypes;
* the colorless section was mostly unplayed filler;
* three-color cards had no home;
* several "Power" prepared cards rarely turned on;
* the BG/RW mana was weaker.

After v1 was fixed, the tests caught a second problem in my own first revision:
decks got too top-heavy. That was fixed in v4.

---

## 1. Methods

### Draft simulator (`tools/sim/draft_sim.py`)
* **Setup:** 8 bots, 3 packs of 15. The 360 cards are split into 24 packs, so
  every card is seen in every draft.
* **How bots pick:** card rating (0–5, in `ratings.py`) plus random noise, plus
  a color-commitment bonus that grows through the draft, plus an archetype
  bonus for cards tagged with the bot's current pair (in `tags.py`).
* **How bots build decks:** the best 23-spell deck in any of the 10 color pairs,
  with an optional 1–3 card splash if the drafted duals support it. The builder
  is curve-aware: a soft cap of five 5+ drops, a hard cap of three 6+ drops, and
  at least five plays at MV ≤ 2.
* **What it measures:**
  * how often each pair is drafted;
  * color share of the cards played;
  * on-theme ("archetype") cards per deck;
  * interaction per deck (removal + sweepers + counterspells);
  * maindeck rate of every card;
  * how an archetype holds up when 2 or 3 drafters fight over it.
* **Caveat:** picks follow my own ratings. The simulator is reliable for
  structure (depth, balance, curve, contention), and only suggestive about
  individual card power.

### Mana simulator (`tools/sim/mana_sim.py`, `land_test.py`, `pair_mana.py`)
* **What it does:** goldfishes 40-card decks on the play with a London-mulligan
  heuristic, playing out turns 1–6. It models every land type exactly as
  printed: shock, slow land, the Marvel "if you control a basic" duals, typed
  checklands, Turbulent/tapped lands, and fetch-a-basic lands.
* **What it reports:**
  * on-curve rate: spent ≥ T mana on turn T, averaged over turns 2–5;
  * mana spent on turns 1–5;
  * color screw: on turn 4, a castable-by-count spell is stuck only on colors.
* **Caveat:** mana creatures and rocks are ignored, so these numbers are a
  conservative floor.

### Independent review
A separate agent got the card data and the eligible pool, but not my ratings
or reasoning. It reviewed the v1 list for weak inclusions, missed cards,
synergy traps, and structural issues. Its findings largely matched the
simulator's.

---

## 2. What v1 got wrong

| Finding | Evidence | Fix |
|---|---|---|
| **Green was the weakest color, black the strongest** | Top-10 average rating: green 3.59, black 4.03. Green had one card rated 4+, black had six. Color share: green 18.5%, black 21.8%. UG was drafted 7.4% of the time, RG 7.8%. | Added Hulk, Strongest There Is; U.S.S. Discovery; Benjamin Sisko; Verdant Kraken; Germination Practicum; Giant-Man; Hulk, Brutal Brawler; and cheaper threats. Cut green filler. Swapped some of black's redundant removal for synergy cards. |
| **Colorless filler** | The four fixing rocks (Firdoch Core, Murmuring Volume, Foraging Wickermaw, Giant's Boulder) were played in **0–1%** of 32,000 simulated decks. Most other colorless cards were played in under 15%. | 13 colorless cards cut. The section went from 28 to 16. |
| **Three-color cards had no home** | Auntie Ool: 0% maindeck. Thanos: requires WUBRG for its upside. Bruce Banner: filed as Temur but really a blue card. | All three cut. |
| **Some prepared spells rarely turn on** | Harmonized Trio only reaches Brainstorm by tapping three creatures. Dirgur Focusmage's Braingeyser needs a 5+ mana-value spell cast from hand. Joined Researchers' spell feeds the opponent too. | All three cut. Jadzi (enters prepared, loots two) and Carnivorous Cultivator (enters prepared) added. |
| **Thin BG and BR archetypes** | BG averaged 9.7 on-theme cards, the lowest, and fell to 6.9 when three drafters shared it. | Added Blight Rot, Requiting Hex, Heirloom Auntie, Kurn, Vraska, the Cutting Glare, Hapatra, Soul Immolation, Kingpin's Enforcers. Graveyard-recursion cards now carry the BG tag, matching the archetype's "blight *and* graveyard" definition. |
| **Prepared lands unplayed** | Skycoach Waypoint and Hexhaven Dueling Arena were each played 4–7% of the time. Few decks hold enough prepared cards for a colorless land to be worth it. | Both cut. Prepared stays a cross-cutting theme, with flicker and Codie as the engines. |
| **Weak or narrow cards** (simulator + reviewer) | Construct a Cosmic Cube needs 7 plan counters. Daughter of the Deep's Merfolk text does nothing here. Pompous Battlemage, Quicksilver, Kiora, Brush Off. Spell Snare and Archive Arbiter were the least-played colored or colorless cards in later rounds (3% and 2%). | Swapped for stronger cards on the same plan: Decorum Dissertation, Leader, Super-Genius, Thor, Asgard's Avenger, Slash, Glen Elendra's Answer, Renet, and more. |

### The gainlands
For BG and RW, every eligible third dual enters tapped: the gainlands, Turbulent
lands, surveil lands, and Hobbit lands alike. The only exception is Reality
Fracture's "Commons" lands, which need a planeswalker.

The checklands **Vernal Fen** and **Radiant Summit** do exist. Both debuted in
*Edge of Eternities Commander* (2025), and in 2026 they were only reprinted in
Commander products, so the reprint rule excludes them.

I measured whether a tapped third dual is worth the slot at all. Results are
from 16 simulated BG or RW decks each, 1,500 goldfish games per deck, with
spells held constant:

| Third dual | BG on-curve | BG color screw | RW on-curve | RW color screw |
|---|---|---|---|---|
| none (shock + slow + basics) | 55.7% | 8.4% | 58.1% | 6.6% |
| **tapped dual (Turbulent / gainland)** | 55.5% | **7.3%** | 57.6% | **5.2%** |
| Vernal Fen–style checkland *(ineligible)* | 56.1% | 6.5% | 58.6% | 4.9% |
| Evolving Wilds–style fetch | 55.1% | 8.1% | 57.2% | 6.4% |

A tapped dual is worth the slot: about 1.1–1.4 points less color screw, for
about 0.2–0.5 points of tempo. Turbulent and gainland play identically on
curve. Turbulent can enter untapped late, and Turbulent Fen is Forest-typed.
So I switched to **Turbulent Fen** and **Turbulent Steppe**.

---

## 3. A problem my own revision introduced (and the fix)

Rounds 2–3 (v2/v3) improved power and balance, but the curve check showed decks
had become **top-heavy**. Green had 17 cards at mana value 5+. Two-drops fell in
every pair.

Average mana value / plays at MV ≤ 2 / plays at MV 5+ per deck, using the
curve-aware builder:

| Pair | v1 | v3 | **Final (v4)** |
|---|---|---|---|
| RG | 3.48 / 6.1 / 5.0 | 3.86 / 5.3 / 8.2 | **3.59 / 6.2 / 5.8** |
| BR | 3.27 / 7.3 / 4.1 | 3.37 / 6.6 / 5.2 | **3.31 / 7.1 / 4.5** |
| WB | 3.19 / 8.0 / 3.6 | 3.29 / 7.2 / 4.4 | **3.22 / 7.7 / 4.2** |
| WG | 3.32 / 7.7 / 4.6 | 3.40 / 7.3 / 5.1 | **3.34 / 8.0 / 4.6** |
| UB | 3.37 / 6.6 / 4.1 | 3.47 / 5.7 / 4.8 | **3.45 / 5.8 / 4.7** |

v4 swapped expensive additions for strong cheap cards:

| Out | In |
|---|---|
| Rhino | Bejeweled Warg |
| Sauron | Michelangelo, the Heart |
| Mugato | Noxious Newt |
| Edgar | Saru |
| Hungering Puppetbeast | Tenacious Tosk |
| Klingon Strike Force | Tasha Yar |
| Gandalf, Spark Starter | Explosive Prodigy |
| Green Goblin | Gollum, Riddle Master |
| Age of Ultron | Requiting Hex |
| Craftwork Crusher | Konstrari Charm |

RG stays the heaviest pair on purpose: it's the ramp deck, with nine mana
creatures and ramp spells in green.

---

## 4. Final results vs. v1

Both runs: 4,000 simulated drafts (32,000 decks), identical seeds, ratings, tags,
and curve-aware builder.

| Metric | v1 | **Final** |
|---|---|---|
| Least – most drafted pair | 7.6% (UG) – 12.7% (WB) | **8.6% (UG) – 11.4% (WR)** |
| Color share of played cards | W 21.3 · U 18.9 · B 21.8 · R 19.5 · G 18.5 | **W 20.5 · U 19.3 · B 20.5 · R 19.3 · G 20.4** |
| Decks splashing a third color | 18.8% | 7.4% (three-color cards and rocks cut on purpose) |
| Decks unable to find 23 on-color playables | 0.02% | 0.05% |
| Mana: on-curve / color screw (drafted decks) | 55.4% / 9.9% | **55.4% / 9.6%** |

Per-archetype numbers below are mean on-theme cards per deck, then mean
interaction per deck. All ten archetypes gained on-theme cards.

| Archetype | v1 | **Final** |
|---|---|---|
| WU Blink & Prepare | 14.2 · 4.3 | **15.3 · 3.9** |
| UB Seek Out | 14.0 · 4.7 | **15.6 · 4.7** |
| UR Spells | 11.9 · 6.2 | **12.9 · 7.2** |
| UG Ramp & Landfall | 11.0 · 2.3 | **12.1 · 2.5** |
| BR Sacrifice & Treasure | 9.8 · 7.4 | **10.8 · 7.2** |
| BG Blight & Graveyard | 9.7 · 4.0 | **11.8 · 5.4** |
| RG Big Stompy | 10.9 · 3.9 | **12.8 · 4.3** |
| RW Equipment | 11.1 · 7.1 | **13.5 · 6.6** |
| WB Ninjas & Sneak | 10.5 · 7.2 | **11.5 · 7.1** |
| GW Counters & Tokens | 12.3 · 3.2 | **13.9 · 2.8** |

**Contention.** On-theme cards per deck when 1 / 2 / 3+ drafters share a pair
in the same pod:

| Archetype | v1 | Final |
|---|---|---|
| BG | 10.7 / 8.4 / 6.9 | **13.1 / 10.2 / 8.2** |
| BR | 10.9 / 8.5 / 7.1 | **11.8 / 9.3 / 7.7** |
| UG | 11.8 / 9.2 / 7.7 | **12.9 / 10.5 / 8.8** |
| RG | 11.7 / 9.2 / 7.3 | **13.9 / 10.9 / 9.0** |

Every archetype now supports two drafters.

**Robustness.** I re-ran with much noisier, more "human" picks (noise 0.8
instead of 0.35, 2,000 drafts). The improvements held:

| | v1 | Final |
|---|---|---|
| Pair share range | 7.6% – 11.6% | **8.6% – 11.1%** |
| Color share spread | 2.1 pts | **1.5 pts** |

### Least-played cards in the final cube, and why they stay
| Card(s) | Final maindeck rate | Why it stays |
|---|---|---|
| The Echoverse Fulcrum | 7% | Colorless sweeper for blue control decks, which have few others |
| Codie, Ravenous Codex | 8% | The cube's one dedicated prepared build-around. Bots don't model its synergy |
| Emrakul, the Exigent Doom; Tri-Sentinel | 7–9% | Reanimator and ramp targets. Bots don't draft reanimator |
| Cinder Strike; Tenderize | 10–12% | Cheap interaction for BG/BR blight and green. Bots favor creatures |
| Transdimensional Bovine | 10% | Ramp the bots underrate |

---

## 5. What the simulation can't tell you
* **No real games.** There is no opponent model, so these tests can't judge
  matchups, combat, or how strong control actually is. The next step is real
  playtesting, ideally a few drafts tracking which decks win.
* **Ratings drive picks.** If one of my ratings is wrong, the bots inherit the
  error. The independent review exists to cross-check this.
* **Mana is a floor.** The mana simulator ignores mana creatures and rocks.
  Green and ramp decks cast more than these numbers suggest.

## 6. Re-running the tests
`tools/sim` scripts need card data. The current list's data ships in
`data/cube_cards.json`. To test another list, build the full pool first (see
the README) and pass `--pool`.

```bash
python3 tools/sim/draft_sim.py --drafts 4000 --seed 7
```
```bash
python3 tools/sim/pair_mana.py --drafts 40 --trials 600
```
```bash
python3 tools/sim/land_test.py --pair BG --pair RW --decks 16 --trials 1500
```
```bash
python3 tools/sim/draft_sim.py --list path/to/other_list.txt --pool raw/eligible_pool.json
```
