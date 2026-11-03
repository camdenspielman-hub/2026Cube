# The 2026 Cube

A 360-card, high-powered cube built only from Magic's 2026 releases: the seven
main sets (**Lorwyn Eclipsed, Teenage Mutant Ninja Turtles, Secrets of
Strixhaven, Marvel Super Heroes, The Hobbit, Reality Fracture, Star Trek**) plus
the Commander, Eternal, and Jumpstart products that came with them.

It aims well above retail-draft power. Most archetypes have build-arounds, and
each one draws on at least four of the seven sets.

| File | What it is |
|---|---|
| [`CARDLIST.md`](CARDLIST.md) | The full 360, by color, with cost, type, set, and archetype tags |
| [`cube/2026_cube.txt`](cube/2026_cube.txt) | One card per line, for CubeCobra's text import |
| [`cube/2026_cube_cubecobra.csv`](cube/2026_cube_cubecobra.csv) | CubeCobra CSV with exact printings (set + collector number) and archetype tags |
| [`cube/cube_list.txt`](cube/cube_list.txt) | The source list, by section, that the other files are generated from |
| [`data/eligible_pool.csv`](data/eligible_pool.csv) | All 2,518 eligible cards, flagged `in_cube`. Use it to find swaps |
| [`data/cube_cards.json`](data/cube_cards.json) | Scryfall data (text, printings, image links) for the 360 |
| [`tools/`](tools/) | Scripts to re-fetch from Scryfall, rebuild the pool, and regenerate everything |

---

## At a glance

| Section | Cards | Creatures | Avg. MV | Notes |
|---|---:|---:|---:|---|
| White | 46 | 31 | 2.87 | Premium removal, blink engines, equipment and counter payoffs |
| Blue | 47 | 32 | 3.00 | 7 counterspells, card advantage, flash threats, blink |
| Black | 47 | 30 | 3.28 | Deepest removal, reanimation, "second card" payoffs, Ninjas |
| Red | 47 | 31 | 3.00 | Burn, spell payoffs, Dwarves and equipment, Treasure |
| Green | 47 | 38 | 3.26 | Mana creatures, fatties, landfall, +1/+1 counters |
| Multicolor | 64 | 52 | 3.52 | 6 per pair (7 for WB) plus 3 three-color cards |
| Colorless | 28 | 12 | 3.54 | Fixing rocks, equipment, prepared enablers, big finishers |
| Lands | 34 | — | — | 3 dual lands per color pair, plus 4 utility lands |
| **Total** | **360** | **226** | **3.21** | 54 instants/sorceries, 11 planeswalkers, 47 artifacts |

**By set family** (main set + its supplemental product):

| Marvel | Strixhaven | Lorwyn | Reality Fracture | Star Trek | TMNT | Hobbit |
|---:|---:|---:|---:|---:|---:|---:|
| 65 | 60 | 58 | 55 | 49 | 41 | 32 |

313 cards come from main-set printings and 47 are new cards from supplemental
products: Marvel Commander/Jumpstart 22, Strixhaven Commander 11, Lorwyn Commander 7,
TMNT Eternal 3, Star Trek Commander 3, Hobbit Eternal 1.

---

## How the pool was built

I pulled every 2026 printing from Scryfall (data as of 3 Nov 2026, after Star
Trek spoilers ended) and applied your eligibility rules card by card:

* **Printed in a 2026 main set → eligible**, new or reprint. That gives us all
  10 shocklands (5 in Lorwyn Eclipsed, 5 in Star Trek), all 10 slowlands (5 in
  Strixhaven, 5 in Reality Fracture), Tarmogoyf, Chandra, Torch of Defiance,
  Engineered Explosives, Spell Snare, Nameless Inversion, Crib Swap, and so on.
* **First printed in a 2026 supplemental product → eligible.** These products
  count: Lorwyn Eclipsed Commander, TMNT Eternal, Secrets of Strixhaven Commander,
  Marvel Super Heroes Commander (which includes the Jumpstart cards), Hobbit
  Eternal, Reality Fracture Commander, and Star Trek Commander.
* **Reprint that appears only in a supplemental product → not eligible.**
  This is the Palace Jailer / The One Ring / Armageddon rule: 909 cards excluded.
* **Excluded entirely:** Mystery Booster Commander (per your follow-up; it was
  all reprints anyway), The Zeta Set (all reprints), the Strixhaven Mystical
  Archive, Alchemy, and three MagicFest promo-only cards not tied to any of the
  seven sets.

The result: **2,518 eligible cards**, 1,767 from main sets and 751 new
supplemental cards. Every one is in `data/eligible_pool.csv`.

The cube uses 31 reprints: the 20 dual lands, Tarmogoyf, Chandra, Engineered
Explosives, Spell Snare, Nameless Inversion, Crib Swap, Bloom Tender, Web Up,
Lightning Strike, Quick Study, and Wood Elves. All of them were printed in a main set.

---

## Design pillars

**1. Strixhaven's "prepared" cards set the power level.**
Secrets of Strixhaven has creatures that come with a Power-level spell attached.
Reality Fracture and the Strixhaven Commander deck continue the mechanic. A
prepared creature can cast a copy of its spell once, and every re-entry to the
battlefield re-arms it. The cube has 25 of them:

| Creature | Spell | | Creature | Spell |
|---|---|---|---|---|
| Emeritus of Truce | **Swords to Plowshares** | | Emeritus of Conflict | **Lightning Bolt** |
| Emeritus of Woe | **Demonic Tutor** | | Naktamun Lorespinner | **Wheel of Fortune** |
| Emeritus of Ideation | **Ancestral Recall** | | Stensian Sanguinist | **Exsanguinate** |
| Emeritus of Abundance | **Regrowth** | | Dirgur Focusmage | **Braingeyser** |
| Grave Researcher | **Reanimate** | | Scheming Silvertongue | Sign in Blood |
| Harmonized Trio | **Brainstorm** | | Studious First-Year | Rampant Growth |
| Vastlands Scavenger | Bind to Life | | Spellbook Seeker | Careful Study |
| Cheerful Osteomancer | Raise Dead | | Variable Chaser | Arc of Fortune (wheel) |
| Skycoach Conductor | All Aboard (blink) | | Diviner of Victory | Unwind History |
| Elite Interceptor | Rejoinder | | Joined Researchers | Secret Rendezvous |
| Quill-Blade Laureate | Twofold Intent | | Pompous Battlemage | Improvised Act |
| Pyre Rhymer | Molten Tide | | Maelstrom Artisan | Rocket Volley |
| Tam, Observant Sequencer | Deep Sight | | | |

Four colorless cards make prepared a deliberate archetype rather than a set of
lucky cards: **Codie, Ravenous Codex** (copies every prepared spell you cast),
**Biblioplex Tomekeeper**, **Skycoach Waypoint**, and **Hexhaven Dueling Arena**.
Every flicker effect in the cube re-arms these creatures too.

**2. Every archetype is cross-set.** I gave priority to mechanics and themes that
appear in more than one set:

| Theme | Where it comes from |
|---|---|
| Prepared | Strixhaven, Strixhaven Commander, Reality Fracture |
| Flicker / ETB value | Lorwyn, Strixhaven, Marvel, Marvel Commander, Star Trek, Hobbit, Reality Fracture, TMNT |
| Sneak (ninjutsu for any card) | TMNT, Marvel (Elektra) |
| "Draw your second card each turn" / *Seek out* | Marvel, Marvel Commander, Hobbit, Star Trek Commander |
| -1/-1 counters & blight | Lorwyn, Lorwyn Commander, Marvel (M.O.D.O.K.) |
| +1/+1 counters | TMNT (Mutagen), Strixhaven (increment), Star Trek, Marvel, Hobbit |
| Landfall & extra land drops | Hobbit, Star Trek, Marvel, Strixhaven, Reality Fracture |
| Equipment | Hobbit, Marvel, TMNT, Reality Fracture, Star Trek |
| Treasure | Hobbit, Star Trek, Lorwyn, Marvel Commander |
| Elves (incidental typal) | Lorwyn, Hobbit, Strixhaven, Reality Fracture |

**3. Only self-contained mechanics.** Every single-set mechanic in the cube
works without other cards from its set: empower Jace makes its own Jace,
Mutagen tokens, station (like crew), monarch, amass, recruit, power-up, connive,
evoke, and Plans. There's no energy-style resource with only one card supporting it.

---

## The ten archetypes

Each pair has six multicolor signposts (seven for WB). The mono-color cards
below each archetype also feed one or two of the others.

### WU — Blink & Prepare
Flicker your prepared creatures and ETB creatures to reuse them over and over.
Every flicker of an Emeritus re-arms its Swords or Ancestral.

* **Engines:** Ennis, Debate Moderator, and Daydream (Strixhaven); Flickering
  Hound and Rescue Girl (Reality Fracture); Quantum Entanglement and Rescue,
  Pepper Potts (Marvel Commander); The Mind Stone (Marvel); Miles O'Brien and
  Ghost of Illyria (Star Trek); Prehistoric Pet (TMNT); Skycoach Conductor;
  Silver Surfer, Cosmic Voyager.
* **Payoffs:** the white and blue prepared creatures, Seasoned Cryomancer,
  Justice, Wesley Crusher, Elektra, Azog, Splinter, Aging Champion, Curious
  Colossus, Captain Marvel, Shooting Star, and the Incarnations. Evoke one and
  flicker it with the sacrifice trigger on the stack, and you keep the body.
* **Signposts:** Don & Leo, Problem Solvers · The Mighty Thor, Jane Foster ·
  King T'Challa · Bard, Heir of Girion · Constable Odo · Proctor of Potential.

### UB — Seek Out (draw-two control)
Marvel, the Hobbit, and Star Trek Commander all reward drawing your second card
each turn. Here that becomes a flash-and-counterspell control deck whose
threats run off its card draw.

* **Payoffs:** M.O.D.O.K., Evil Intellect (an edict every time it triggers),
  Construct a Cosmic Cube, Madame Masque, Data, Professor of Humanities, Data,
  Exploring Humanity, Daughter of the Deep, Kang, Temporal Tyrant, King T'Challa,
  Lyra, Tolarian Archangel.
* **Enablers:** Mr. Spock, Science Officer (every draw is doubled, so your draw
  step alone triggers everything), Seven of Nine, Unassimilated, Spock, Logical
  Choice, Doctor Doom, Unrivaled, Sinister Gnarlbark, Loch Mare, Brainstorm,
  Quick Study, Plunder the Trollshaws, Riddles in the Dark, Confusticate and
  Bebother, Impossible Choice, Cloistered Telepath, Voracious Tome-Skimmer, and
  the two Food cantrip artifacts.
* **Reanimator sub-theme:** Reanimate (Grave Researcher), Too Evil to Stay Dead,
  Rewrite Regrets, Liliana the Repentant, and Karai. They're fed by Careful Study,
  Cryomancer, Formidable Speaker, and the wheels. Targets include Armaggon,
  Captain Marvel, Curious Colossus, Emrakul, the Exigent Doom, Tri-Sentinel,
  Kitsune, and Lamentation.

### UR — Spellslinger
Strixhaven's Opus, Reality Fracture's prowess, and Marvel's "whenever you cast a
noncreature spell" all reward the same deck. It has 54 instants and sorceries to
draw from, plus 25 prepared spells.

* **Payoffs:** Colorstorm Stallion, Rootha, Prismari Pianist, and Molten-Core
  Maestro (Strixhaven); Saheeli, Jewel of Avishkar, Pyre Rhymer, Pompous
  Battlemage, Variable Chaser, and Stingcaster Mage (Reality Fracture); Thor, God
  of Thunder, The Vision and Scarlet Witch, The Vision, and Valeria Richards
  (Marvel); Gandalf, Goblins' Bane and Bilbo, Thief in the Night (Hobbit);
  Romulan Bird-of-Prey and Lieutenant Commander Data (Star Trek); Spinerock
  Tyrant (Lorwyn). Emeritus of Conflict re-arms its Lightning Bolt whenever you
  cast your third spell in a turn.
* **Cost reducers:** Geist of Saint Thalia, Dirgur Focusmage, Iron Lad, Valeria,
  and Great Hall of the Biblioplex.

### UG — Ramp & Landfall
Extra land drops and landfall payoffs, from Lorwyn Eclipsed through Star Trek.

* **Ramp:** Bloom Tender, Frog Butler, Great Forest Druid, Jadzia Dax,
  Rampant Growth, Simulacrum Shaper, Transdimensional Bovine, Mona Lisa, and
  Rok-Tahk. Wood Elves can fetch a Forest-typed shockland or Sodden Verdure.
* **Landfall:** Captain Janeway (Star Trek), Thranduil's Company and Dancing
  from Dark to Dawn (Hobbit), Mole Man (Marvel), Tam, Observant Sequencer
  (Strixhaven), Silvan Reveler, Beorn's Hospitality, and Hexhaven Invigorator
  (Reality Fracture).
* **Payoffs and mana sinks:** Oko, Lorwyn Liege, Wistfulness, Mind into Matter,
  Slumbering Trudge, Kinetic Ooze, Kitsune, Gigantic Big Bear, Emrakul, Crystalline
  Entity, and Bruce Banner.

### BR — Sacrifice & Treasure
* **Outlets:** Gowron and L'Rell (Star Trek), The Sackville-Bagginses and
  Snowslope Hunter (Hobbit), Khan, Vengeful Heart, and Witherbloom Charm.
* **Fodder:** Bitterbloom Bearer's Faeries, L'Rell's hasty Klingons, Ultron's
  Robots, Retched Wretch, and Treasure from Scuzzback Scrounger, Smaug, Luke
  Cage, Noggle Robber, and Village Pillagers.
* **Payoffs:** Super Shredder grows whenever any permanent leaves, including
  sacrificed Treasure and your opponent's removal targets. Also Smaug, Wicked
  Worm, Grave Venerations, and Draconic Visitor (your Treasures become 5/5
  Dragons). Worf, Intelligence Contractor and The Wrath of Khan steal creatures
  for you to sacrifice.

### BG — Blight & Graveyard
Lorwyn's -1/-1 counters become a resource, backed by graveyard value from
Strixhaven, TMNT, and Star Trek.

* **Counters as a resource:** blight costs (Scuzzback Scrounger, Cinder Strike,
  Wild Unraveling, Sinister Gnarlbark) and creatures that start with counters
  (Moonshadow, Creakwood Safewright, Bristlebane Battler, Loch Mare, Retched
  Wretch).
* **Payoffs:** Dread Tiller, Shadow Urchin, Auntie Ool, High Perfect Morcant,
  Village Pillagers, and Rhys. Mikey & Leo draws a card when *you* put a
  counter on your own creature, and blight counts.
* **Graveyard:** Trystan, Midnight Tilling, Liliana, Tarmogoyf, The Last Ronin,
  Professor Dellian Fel, Regrowth, Bind to Life, Dr. McCoy.
* There are 11 Elves (Lorwyn, Hobbit, Strixhaven, Reality Fracture), so Morcant,
  Creakwood Safewright, Trystan, and Thranduil's Company all have support.

### RG — Big Stompy
* **Haste:** Samut, Hazoret's Champion, Hit It!, and Wolverine, plus double
  strike from Raphael, the Nightwatcher.
* **Bodies:** Gigantic Big Bear, Hexhaven Invigorator, Mugato, Hit-Monkey,
  Leatherhead, Beorn the Fierce, Groundchuck & Dirtbag, Aerid Konstrari,
  Vibrance, Luke Cage, Kiora.
* **Engines:** Garruk, Curse Breaker draws whenever a 4-power creature enters,
  and Michelangelo cheats creatures and lands into play.

### RW — Equipment Aggro
Hobbit Dwarves, Marvel's arsenal, and TMNT's Hard-Won Jitte.

* **Equipment (10, plus two Axe tokens):** Hard-Won Jitte, Mjölnir, Lich's
  Relic, Warrior's Blades, Orcrist, Sting, Iron Man Armor, Captain America's
  Shield, Vibranium Strike Gauntlets, and Type-2 Phaser. Iron Hills Blacksmith
  and Dáin Ironfoot each make an Axe token.
* **Payoffs:** Kíli (draws when an Equipment or Dwarf enters, and makes equips free), Dwalin (hone
  counters), Thorin, Mountain-king, Dáin Ironfoot (double strike), Quill-Blade
  Laureate, Kinscaer Sentry, both Captain Americas, Raph & Leo (an extra combat),
  Excava, Quintorius, Catharsis.
* Mjölnir can only equip "worthy" creatures, meaning legendary non-Villain red
  or white creatures. The cube has 61.

### WB — Ninjas & Sneak
TMNT's sneak plus Marvel's Elektra. Hit with something evasive, then return it
to hand to put a Ninja (or a removal spell) into play.

* **Sneak cards:** Leonardo, Cutting Edge, Leonardo, Sewer Samurai, Splinter,
  Hamato Yoshi, Shark Shredder, Splinter's Technique (a tutor), Shredder's
  Technique (removal), Elektra, Dark Leo & Shredder, Karai, Turncoat Kunoichi.
* **Evasive enablers:** Bitterbloom Bearer, Scheming Silvertongue, Abigale,
  Captain America, Wings of Freedom, Soaring Stoneglider, Black Widow, Super Spy,
  Prehistoric Pet. Endless Foot Assault makes an attacking Ninja token every time
  you attack.
* Returning a creature to hand also lets you recast Elektra, Splinter, Aging
  Champion, Salt Vampire, Cloak and Dagger, and Emptiness for their ETBs again.
  There are 18 Ninjas, so Splinter's anthem and Dark Leo's deathtouch both have
  plenty to work with.

### GW — Counters & Tokens
* **Counter engines:** Deanna Troi (Star Trek), Agent Bishop and Michelangelo,
  Weirdness to 11 (TMNT), Dr. M'Benga (doubles counters), Okoye, Mighty and
  Adored (monarch), Jadzia Dax, Ambitious Augmenter, Beorn's Hospitality,
  Dancing from Dark to Dawn.
* **Counter payoffs:** Mikey & Leo and Phlox draw cards, Mona Lisa makes mana,
  and Lieutenant Commander Data and Kinetic Ooze use counters too.
* **Tokens:** Captain Jean-Luc Picard (an anthem, and an Officer for every creature
  you cast), Ajani, Outland Chaperone, Antiquities on the Loose, Triceraton
  Commander, The Unbeatable Squirrel Girl, Holo-Engineer, Brigid, Enterprise-A,
  The Arkenstone, Kwia Vigorbloom.

### Three-color and five-color
Thanos, the Mad Titan (a 3-mana 4/4 deathtouch lifelink in RWB), Auntie Ool
(Jund blight), and Bruce Banner. Bruce is a 1-mana blue draw engine that turns
into a Temur Hulk. With 30 duals, Surveillance Room, mana creatures, and rocks,
three-color decks are realistic.

---

## Interaction

* **Removal (48 cards):** White has Swords, Erode, 70,000 Light-Years from Home,
  Prophesied End, and Harsh Annotation at 1–2 mana. Black has Dark Deed,
  Vraska's Final Mercy, Bilbo's Deadly Slice, Death in the Family, Resistance Is
  Futile, and Lich's Relic. Red has Bolt, Lightning Strike, Sear, Impractical
  Joke, Khaaaaaaaaaaaannn!, and End-Blaze Epiphany. Green has bite spells and
  Chomping Changeling. There's also colorless removal: Henchbots, Archive Arbiter,
  and Engineered Explosives.
* **Sweepers (8):** Ceaseless Conflict, Withering Curse, Avengers Disassembled,
  Jennika's Technique, The Last Ronin, Engineered Explosives, The Echoverse
  Fulcrum, Crystalline Entity.
* **Counterspells:** Spell Snare, Wild Unraveling, Countersculpt, Mana Sculpt,
  Highly Illogical, Brush Off, and Confusticate. Glen Elendra Guardian, Wesley
  Crusher, and Theorix Charm add soft counters.
* **Planeswalkers (11):** Oko, Ajani, Outland Chaperone, Ral Zarek, Garruk ×2,
  Chandra ×2, The Theorist Jace, Professor Dellian Fel, Ajani Unrelenting,
  Quintorius.

## Mana

Every color pair gets three duals:

| Pair | Shock | Slow land | Third dual |
|---|---|---|---|
| WU | Hallowed Fountain | Deserted Beach | Gleaming Bastion |
| UB | Watery Grave | Shipwreck Marsh | Hidden Lair |
| UR | Steam Vents | Stormcarved Coast | Scorched Geyser |
| UG | Breeding Pool | Dreamroot Cascade | Sodden Verdure |
| BR | Blood Crypt | Haunted Ridge | Dark Fortress |
| BG | Overgrown Tomb | Deathcap Glade | Illegitimate Business |
| RG | Stomping Ground | Rockfall Vale | Training Compound |
| RW | Sacred Foundry | Sundown Pass | Dimension X |
| WB | Godless Shrine | Shattered Sanctum | Eclipsed Steppe |
| GW | Temple Garden | Overgrown Farmland | Gathering Place |

The shocklands come from Lorwyn and Star Trek, the slow lands from Strixhaven
and Reality Fracture. The Marvel duals enter untapped if you control a basic. The
typed checklands are new in the Commander decks. The Illegitimate Business and
Dimension X gain lands are from TMNT.

Utility lands: **Skycoach Waypoint** and **Hexhaven Dueling Arena** (prepared),
**Great Hall of the Biblioplex** (spells), and **Surveillance Room** (any color).
Fixing rocks and creatures: H.E.R.B.I.E., Lovable Robot, Firdoch Core, Murmuring
Volume, Foraging Wickermaw, Giant's Boulder, The Mind Stone, Bloom Tender, Frog
Butler, Great Forest Druid, Wood Elves.

---

## Trap audit

You asked me to avoid cards that imply synergy the cube doesn't have. For every
card that leans on something else, here is the support that exists:

| Card(s) | Needs | In the cube |
|---|---|---|
| Splinter, Hamato Yoshi; Dark Leo & Shredder | Ninjas | 18 Ninja cards and token makers |
| Kíli; Dwalin; Thorin; Dáin; Jane Foster | Equipment | 10 Equipment and 2 Axe-token makers |
| Mjölnir | "Worthy" creatures | 61 legendary non-Villain R/W creatures |
| High Perfect Morcant; Creakwood Safewright; Thranduil's Company; Trystan | Elves | 11 Elves |
| Codie; Biblioplex Tomekeeper; Waypoint; Dueling Arena | Prepared creatures | 25, plus 15 flicker and bounce-your-own effects and 14 sneak cards |
| The seek-out payoffs | Extra draws | Mr. Spock, Seven of Nine, Spock, Doom, Gnarlbark, ~12 cantrips and instant-speed draws |
| Mikey & Leo; Phlox; M'Benga; Lt. Cmdr. Data | Counters on your creatures | Mutagen, increment, Deanna Troi, Agent Bishop, landfall counters, plus every -1/-1 counter |
| Smaug ×2; Draconic Visitor | Treasure | 8 Treasure makers |
| Opus / prowess / noncreature payoffs | Instants and sorceries | 54, plus 25 prepared spells |
| Gowron (draws if you sacrifice a Klingon); Picard (Spacecraft tutor) | Klingons; Spacecraft | Bonuses only, not needed. L'Rell and Worf make Klingons. There are 3 Spacecraft |
| Kinscaer Sentry; Captain America, Wings of Freedom | Attackers; Heroes | Works alone, and there are lots of Marvel Heroes |

**Left out as traps** (strong cards whose synergy isn't in the cube):

* Devil Dinosaur (no Dinosaurs).
* Seven of Nine (the UB "dilemma" version). I chose Seven of Nine, Unassimilated
  instead.
* The Hero/Villain lords: Avengers Assemble!, The Masters of Evil, Baron Strucker,
  Madame Hydra.
* Behold and typal payoffs: the Lorwyn Champion cycle, Chronicle of Victory,
  Turtle Power!, An Unexpected Party.
* Quark, Humble Proprietor (its Treasures can't be sacrificed).
* The Federation and "Strange new worlds" cards, the Reality Fracture
  "Way of the…" enchantments, and multiplayer-only Commander cards (Battlefront,
  goad, Council's dilemma).

## Close calls (good swap candidates)

These were cut on curve or slot pressure, not power: Super-Skrull, Savanti
Romero, Moment of Reckoning, Lorehold the Historian, Silverquill the Disputant,
Quandrix the Proof, Jennifer Walters, Monica Rambeau, Splatter Technique, Glen
Elendra's Answer, Raphael's Technique, Bard's Company, Vraska, the Cutting Glare,
Ingris Stingerquill, Dina's Guidance, Twilight Diviner, Mathemagics, Gollum,
Riddle Master, Kinbinding, Yavimaya Bloomsage (Channel). Filter
`data/eligible_pool.csv` on `in_cube` to browse the rest of the pool.

---

## Importing to CubeCobra

* Fastest: *Add/Remove → Bulk Upload →* paste `cube/2026_cube.txt`.
* With exact printings and tags: *Import → CSV →* `cube/2026_cube_cubecobra.csv`.
  Tags are `;`-separated (for example `WU Blink;Prepared;Removal`).

## Rebuilding from Scryfall

```bash
python3 tools/fetch_sets.py raw ecl ecc pecl tmt tmc pza sos soc soa psos msh msc hob hoc fra frc pfra trk trc sds
python3 tools/build_pool.py raw raw/eligible_pool.json
python3 tools/export_data.py raw/eligible_pool.json
python3 tools/build_outputs.py
```

To change the cube, edit `cube/cube_list.txt` (and `tools/tags.py` for tags).
Then re-run the last two commands.
