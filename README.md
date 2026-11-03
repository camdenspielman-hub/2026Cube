# The 2026 Cube

A 360-card, high-powered draft cube built only from Magic's 2026 releases. It
draws on the seven main sets (**Lorwyn Eclipsed, Teenage Mutant Ninja
Turtles, Secrets of Strixhaven, Marvel Super Heroes, The Hobbit, Reality
Fracture, Star Trek**) and the Commander, Eternal, and Jumpstart products that
came with them.

It aims well above retail-draft power. Most archetypes have build-arounds, and
each one draws on at least four of the seven sets. The list has been through
simulated drafts, mana and curve tests, and an independent review. See
**[TESTING.md](TESTING.md)** for the method, results, and the 57 changes made
since the first version.

| File | What it is |
|---|---|
| [`CARDLIST.md`](CARDLIST.md) | The full 360, by color, with cost, type, set, and archetype tags |
| [`TESTING.md`](TESTING.md) | How the cube was tested and revised, with before/after numbers |
| [`cube/2026_cube.txt`](cube/2026_cube.txt) | One card per line, for CubeCobra's text import |
| [`cube/2026_cube_cubecobra.csv`](cube/2026_cube_cubecobra.csv) | CubeCobra CSV with exact printings (set + collector number) and archetype tags |
| [`cube/cube_list.txt`](cube/cube_list.txt) | The source list, by section, that the other files are generated from |
| [`data/eligible_pool.csv`](data/eligible_pool.csv) | All 2,518 eligible cards, flagged `in_cube`. Use it to find swaps |
| [`data/cube_cards.json`](data/cube_cards.json) | Scryfall data (text, printings, image links) for the 360 |
| [`tools/`](tools/) | Scripts to fetch from Scryfall, rebuild the pool, regenerate the files, and run the simulators (`tools/sim/`) |

---

## At a glance

| Section | Cards | Creatures | Avg. MV | Notes |
|---|---:|---:|---:|---|
| White | 48 | 32 | 2.98 | Premium cheap removal, blink engines, equipment carriers, go-wide |
| Blue | 48 | 34 | 3.25 | Counterspells, card advantage engines, flash threats, blink |
| Black | 47 | 29 | 3.13 | Removal, reanimation, "second card" payoffs, Ninjas, sacrifice |
| Red | 49 | 32 | 3.10 | Burn, spell payoffs, Dwarves and equipment, hasty threats |
| Green | 50 | 41 | 3.40 | Mana creatures, snowballing threats, landfall, +1/+1 counters |
| Multicolor | 70 | 54 | 3.64 | 6–8 per color pair, weighted toward the pairs that needed help |
| Colorless | 16 | 6 | 3.88 | Equipment, sweepers, the prepared engine, big finishers |
| Lands | 32 | — | — | 3 dual lands per color pair, plus 2 utility lands |
| **Total** | **360** | **228** | **3.31** | 59 instants/sorceries, 11 planeswalkers, 35 artifacts |

**By set family** (main set + its supplemental product):

| Marvel | Strixhaven | Lorwyn | Reality Fracture | Star Trek | TMNT | Hobbit |
|---:|---:|---:|---:|---:|---:|---:|
| 66 | 63 | 55 | 55 | 53 | 39 | 29 |

301 cards come from main-set printings and 59 are new cards from supplemental
products: Marvel Commander/Jumpstart 28, Strixhaven Commander 12, Star Trek
Commander 8, Lorwyn Commander 6, TMNT Eternal 4, Hobbit Eternal 1.

**Test summary** (4,000 simulated 8-player drafts):

* Every color pair is drafted 8.6–11.4% of the time.
* Each color makes up 19.3–20.5% of the cards that get played.
* Every archetype still yields 8 or more on-theme cards when three drafters
  fight over it.

Details are in [TESTING.md](TESTING.md).

---

## How the pool was built

I pulled every 2026 printing from Scryfall (data as of 3 Nov 2026, after Star
Trek spoilers ended) and applied your eligibility rules card by card:

* **Printed in a 2026 main set → eligible**, new or reprint. That gives us all
  10 shocklands (5 in Lorwyn Eclipsed, 5 in Star Trek), all 10 slow lands (5 in
  Strixhaven, 5 in Reality Fracture), Tarmogoyf, Chandra, Torch of Defiance,
  Engineered Explosives, Crib Swap, and so on.
* **First printed in a 2026 supplemental product → eligible.** These products
  count: Lorwyn Eclipsed Commander, TMNT Eternal, Secrets of Strixhaven
  Commander, Marvel Super Heroes Commander (which includes the Jumpstart cards),
  Hobbit Eternal, Reality Fracture Commander, and Star Trek Commander.
* **Reprint that appears only in a supplemental product → not eligible.**
  This is the Palace Jailer / The One Ring / Armageddon rule: 909 cards excluded.
  It also excludes the BG and RW checklands **Vernal Fen** and **Radiant Summit**.
  They debuted in *Edge of Eternities Commander* (2025), and in 2026 they were only
  reprinted in Commander products.
* **Excluded entirely:**
  * Mystery Booster Commander, per your follow-up; it was all reprints anyway.
  * The Zeta Set (all reprints).
  * The Strixhaven Mystical Archive.
  * Alchemy.
  * Three MagicFest promo-only cards not tied to any of the seven sets.

The result is **2,518 eligible cards**: 1,767 from main sets and 751 new
supplemental cards. Every one is in `data/eligible_pool.csv`.

The cube uses 28 reprints:
* the 20 dual lands;
* Tarmogoyf and Chandra, Torch of Defiance;
* Engineered Explosives;
* Crib Swap, Bloom Tender, Web Up, Lightning Strike and Quick Study.

All of them were printed in a main set.

---

## Design pillars

**1. Strixhaven's "prepared" cards set the power level.**
Secrets of Strixhaven has creatures that come with a Power-level spell attached.
Reality Fracture and the Strixhaven Commander deck continue the mechanic. A
prepared creature can cast a copy of its spell once, and every re-entry to the
battlefield re-arms it.

The cube has 21 of them. The table separates those that **enter prepared**
from those that need a condition, so you know which ones reliably give you
their spell:

| Enters prepared | Spell | | Prepared on a condition | Spell (condition) |
|---|---|---|---|---|
| Emeritus of Woe | **Demonic Tutor** | | Emeritus of Truce | **Swords to Plowshares** (opponent has more creatures; you can give them the Inkling) |
| Emeritus of Ideation | **Ancestral Recall** | | Grave Researcher | **Reanimate** (3+ creature cards in your graveyard) |
| Emeritus of Abundance | **Regrowth** | | Emeritus of Conflict | **Lightning Bolt** (your third spell in a turn) |
| Vastlands Scavenger | Bind to Life (put a creature from the top 7 into play) | | Naktamun Lorespinner | **Wheel of Fortune** (a player has ≤1 card in hand) |
| Studious First-Year | Rampant Growth | | Stensian Sanguinist | **Exsanguinate** (a deathtouch hit) |
| Jadzi, Steward of Fate | Oracle's Gift (X Fractals) | | Scheming Silvertongue | Sign in Blood (gain 2+ life) |
| Spellbook Seeker | Careful Study | | Tam, Observant Sequencer | Deep Sight (landfall) |
| Skycoach Conductor | All Aboard (blink) | | | |
| Variable Chaser | Arc of Fortune (wheel) | | | |
| Diviner of Victory | Unwind History (bounce) | | | |
| Elite Interceptor | Rejoinder | | | |
| Quill-Blade Laureate | Twofold Intent | | | |
| Maelstrom Artisan | Rocket Volley | | | |
| Carnivorous Cultivator | Enroot | | | |

**Codie, Ravenous Codex** copies every prepared spell you cast. Every flicker
effect in the cube re-arms these creatures, which is what the WU deck is built on.

**2. Every archetype is cross-set.** I gave priority to mechanics and themes that
appear in more than one set:

| Theme | Where it comes from |
|---|---|
| Prepared | Strixhaven, Strixhaven Commander, Reality Fracture |
| Flicker / ETB value | Strixhaven, Marvel, Marvel Commander, Star Trek, Reality Fracture, TMNT, Lorwyn |
| Sneak (ninjutsu for any card) | TMNT, Marvel (Elektra) |
| "Draw your second card each turn" / *Seek out* | Marvel, Marvel Commander, Star Trek Commander, Hobbit |
| -1/-1 counters & blight | Lorwyn, Reality Fracture (Hapatra), Marvel (M.O.D.O.K.) |
| +1/+1 counters | TMNT (Mutagen), Marvel (both Hulks), Star Trek, Strixhaven (Paradigm), Hobbit |
| Landfall & extra land drops | Hobbit, Star Trek, Marvel, Strixhaven, Reality Fracture |
| Equipment | Hobbit, Marvel, TMNT, Reality Fracture, Star Trek |
| Treasure | Hobbit, Star Trek, Lorwyn, Marvel Commander |
| Elves (incidental typal) | Lorwyn, Hobbit, Strixhaven, Reality Fracture |

**3. Only self-contained mechanics.** Every single-set mechanic in the cube
works without other cards from its set. Empower Jace makes its own Jace.
Mutagen tokens, station (like crew), monarch, amass, recruit, power-up,
connive, evoke, squad, web-slinging and Paradigm need nothing else either.
There's no energy-style resource with only one card supporting it.

---

## The ten archetypes

Each pair has 6–8 multicolor signposts. The pairs that tested weakest got the
extra signposts. Mono-color cards below feed one or two archetypes each.

### WU — Blink & Prepare
Flicker your prepared creatures and ETB creatures to reuse them over and over.
Every flicker of an Emeritus re-arms its Swords or Ancestral.

* **Engines:**
  * Ennis, Debate Moderator and Daydream (Strixhaven).
  * Rescue Girl (Reality Fracture).
  * Quantum Entanglement and Rescue, Pepper Potts (Marvel Commander).
  * The Mind Stone (Marvel).
  * Miles O'Brien and Ghost of Illyria (Star Trek).
  * Amazing Spider-Girl, whose web-slinging returns a creature to hand to recast.
  * Skycoach Conductor and Silver Surfer, Cosmic Voyager.
* **Payoffs:**
  * The prepared creatures above.
  * Seasoned Cryomancer, Justice, Wesley Crusher.
  * ETB removal: Elektra, Azog, Splinter, Aging Champion, Captain Marvel,
    Shooting Star, Curious Colossus.
  * The Incarnations. Evoke one and flicker it with the sacrifice trigger on the
    stack, and you keep the body.
* **Signposts:** Don & Leo, Problem Solvers · The Mighty Thor, Jane Foster ·
  King T'Challa · Bard, Heir of Girion · Bard's Company · Denzilore Fatehold ·
  Proctor of Potential.

### UB — Seek Out (card-advantage control)
Marvel, Star Trek Commander, and the Hobbit all reward drawing your second
card each turn. Here that becomes a flash-and-counterspell control deck whose
threats run off its card draw.

* **Payoffs:**
  * M.O.D.O.K., Evil Intellect (an edict every time it triggers).
  * Data, Professor of Humanities and Data, Exploring Humanity.
  * Kang, Temporal Tyrant and King T'Challa.
  * Lyra, Tolarian Archangel (three cards in a turn makes an Angel).
* **Engines:**
  * Mr. Spock, Science Officer. Every draw is doubled, so your draw step alone
    triggers everything.
  * Decorum Dissertation. Thanks to Paradigm, it draws two every turn.
  * Leader, Super-Genius (a draw plus a connive every combat).
  * Seven of Nine, Unassimilated; Spock, Logical Choice; Doctor Doom,
    Unrivaled; Sinister Gnarlbark; Kurn; Loch Mare.
  * Instant-speed card draw: Quick Study, Plunder the Trollshaws, Riddles in the
    Dark, Confusticate and Bebother, Impossible Choice, Cloistered Telepath,
    Voracious Tome-Skimmer.
* **Control tools:**
  * Counterspells: Wild Unraveling, Mana Sculpt, Countersculpt, Highly
    Illogical, Glen Elendra's Answer.
  * Flash threats: Glen Elendra Guardian, Sphinx of False Conclusions, The
    Wondrous Wasp, Subcommander T'Pol, Renet, Bitterbloom Bearer.
* **Reanimator sub-theme:**
  * Reanimation: Reanimate (Grave Researcher), Too Evil to Stay Dead, Rewrite
    Regrets, Liliana the Repentant, Karai.
  * Fuel: Careful Study, Cryomancer, Formidable Speaker, Jadzi, and the wheels.
  * Targets: Captain Marvel, Shooting Star, Curious Colossus, Emrakul, the
    Exigent Doom, Tri-Sentinel, Kitsune, Verdant Kraken, Lamentation.
* **Signposts:** Kang, Temporal Tyrant · Deceit · Voracious Tome-Skimmer ·
  Theorix Charm · Uldaros Theorix · Null Summoner.

### UR — Spellslinger
Strixhaven's Opus, Reality Fracture's prowess, and Marvel's "whenever you cast a
noncreature spell" all reward the same deck.

* **Payoffs:**
  * Strixhaven: Colorstorm Stallion, Rootha, Prismari Pianist, Molten-Core
    Maestro.
  * Reality Fracture: Saheeli, Jewel of Avishkar, Stingcaster Mage, Variable
    Chaser.
  * Marvel: Thor, God of Thunder, Thor, Asgard's Avenger, The Vision and Scarlet
    Witch, The Vision, Valeria Richards, Hawkeye, Avenging Archer.
  * Hobbit: Gandalf, Goblins' Bane and Bilbo, Thief in the Night.
  * Star Trek: Romulan Bird-of-Prey and Lieutenant Commander Data.
  * Lorwyn: Spinerock Tyrant.
  * Emeritus of Conflict re-arms its Lightning Bolt on your third spell each turn.
* **Spells:** Prismari Charm, Vibrant Outburst, Traumatic Critique, Splatter
  Technique, and the red burn suite. Geist of Saint Thalia and Great Hall of the
  Biblioplex make spells cheaper.
* **Signposts:** Colorstorm Stallion · Traumatic Critique · Saheeli · Rootha ·
  Vibrant Outburst · Hawkeye, Avenging Archer · Splatter Technique · Prismari Charm.

### UG — Ramp & Landfall
* **Ramp:** Bloom Tender, Frog Butler, Great Forest Druid, Noxious Newt, Jadzia
  Dax, Rampant Growth, Simulacrum Shaper, Transdimensional Bovine, Giant-Man,
  Rok-Tahk, Weather Maker.
* **Lands matter:**
  * Captain Janeway (Star Trek).
  * Thranduil's Company and Dancing from Dark to Dawn (Hobbit).
  * Mole Man (Marvel), who replays lands from your graveyard.
  * Tam, Observant Sequencer and Carnivorous Cultivator.
  * Verdant Kraken (a land creature every upkeep) and Benjamin Sisko, Besieged
    (play lands and creatures off the top).
* **Payoffs:** Oko, Lorwyn Liege, Wistfulness, Mind into Matter, Quandrix, the
  Proof, Mind Meanderer, U.S.S. Discovery, Kitsune, Gigantic Big Bear, Emrakul,
  Crystalline Entity.
* **Signposts:** Oko · Wistfulness · Thranduil's Company · Tam · Mind into Matter ·
  Quandrix, the Proof · Proctor's Gaze · Mind Meanderer.

### BR — Sacrifice & Treasure
* **Outlets:** Gowron and L'Rell (Star Trek), The Sackville-Bagginses (Hobbit),
  Kingpin's Enforcers (Marvel), Khan, Vengeful Heart.
* **Fodder:**
  * Bitterbloom Bearer's Faeries, L'Rell's hasty Klingons, Ultron's Robots,
    Heirloom Auntie.
  * Tasha Yar, who leaves a card behind when she dies.
  * Treasure from Scuzzback Scrounger, Smaug, Luke Cage, Noggle Robber,
    Bejeweled Warg, and Village Pillagers.
* **Payoffs:**
  * Super Shredder grows whenever any permanent leaves.
  * Smaug, Wicked Worm, Grave Venerations, Heirloom Auntie.
  * Draconic Visitor, which turns your Treasures into 5/5 Dragons.
  * Worf, Intelligence Contractor and The Wrath of Khan steal creatures for you
    to sacrifice.
* **Signposts:** Gowron · L'Rell · Tokka & Rahzar · Shadow Urchin · Smaug, Wicked
  Worm · Stingerquill Charm.

### BG — Blight & Graveyard
Lorwyn's -1/-1 counters become a resource, backed by graveyard value from
Strixhaven, TMNT, and Star Trek.

* **Counters as a resource:**
  * Blight costs: Scuzzback, Cinder Strike, Requiting Hex, Wild Unraveling,
    Soul Immolation, Sinister Gnarlbark.
  * Creatures that start with counters: Moonshadow, Heirloom Auntie, Bristlebane
    Battler, Loch Mare.
  * Counters on their side: Blight Rot, Hapatra, Dread Tiller.
* **Payoffs:**
  * Dread Tiller, Shadow Urchin, High Perfect Morcant, Village Pillagers, and Rhys.
  * Mikey & Leo draws a card when *you* put a counter on your own creature, and
    blight counts.
* **Graveyard:** Trystan, Liliana, Tarmogoyf, The Last Ronin, Professor Dellian
  Fel, Ral Zarek, Regrowth, Bind to Life, Reanimate, Too Evil to Stay Dead,
  Rewrite Regrets, Dr. McCoy, Kurn.
* **Signposts:** Professor Dellian Fel · The Last Ronin · Dread Tiller · High
  Perfect Morcant · Witherbloom Charm · Trystan · Vraska, the Cutting Glare · Hapatra.

### RG — Big Stompy
* **Haste:** Samut, Hazoret's Champion, Hit It!, and Wolverine, plus double
  strike from Raphael, the Nightwatcher.
* **Threats:**
  * Hulk, Strongest There Is doubles its counters every upkeep.
  * Hulk, Brutal Brawler, Slash, Tenacious Tosk, Leatherhead, Hit-Monkey, Beorn.
  * Aerid Konstrari, Vibrance, Luke Cage, Gigantic Big Bear, Verdant Kraken.
* **Engines:** Garruk, Curse Breaker draws whenever a 4-power creature enters.
  Also Michelangelo, Improviser, Giant-Man, and Soul Immolation.
* **Signposts:** Vibrance · Wolverine · Aerid Konstrari · Noggle Robber · Gert and
  Old Lace · Hit It! · Konstrari Charm.

### RW — Equipment Aggro
* **Equipment:** Hard-Won Jitte, Mjölnir, Lich's Relic, Warrior's Blades,
  Orcrist, Sting, Iron Man Armor, Type-2 Phaser, Vibranium Strike Gauntlets.
  Iron Hills Blacksmith and Dáin Ironfoot each make an Axe token.
  Captain America, Liberator tutors an Equipment directly onto the battlefield.
* **Payoffs:**
  * Kíli draws when an Equipment or Dwarf enters, and makes equips free.
  * Thorin, Mountain-king and Dáin Ironfoot (double strike).
  * Quill-Blade Laureate, Kinscaer Sentry, three Captain Americas, Spider-Man,
    Imperial Hullbreachers (battle cry).
  * Raph & Leo (an extra combat), Excava, Quintorius, Catharsis, Lorehold.
* Mjölnir can only equip "worthy" creatures, meaning legendary non-Villain red
  or white creatures. The cube has 68.
* **Signposts:** Catharsis · Raph & Leo, Sibling Rivals · Quintorius · Lorehold, the
  Historian · Warrior's Blades · Excava.

### WB — Ninjas & Sneak
TMNT's sneak plus Marvel's Elektra. Hit with something evasive, then return it
to hand to put a Ninja (or a removal spell) into play.

* **Sneak cards:**
  * Leonardo, Cutting Edge and Leonardo, Sewer Samurai.
  * Splinter, Hamato Yoshi and Shark Shredder.
  * Splinter's Technique (a tutor) and Shredder's Technique (removal).
  * Elektra, Dark Leo & Shredder, Karai, Turncoat Kunoichi.
* **Evasive enablers:** Bitterbloom Bearer, Scheming Silvertongue, Abigale,
  Captain America, Wings of Freedom, Soaring Stoneglider, Black Widow, Super Spy,
  Imperial Hullbreachers, Lyra, Archangel of Dawn. Endless Foot Assault makes an
  attacking Ninja token every time you attack.
* Returning a creature to hand also lets you recast Elektra, Splinter, Aging
  Champion, Salt Vampire, Cloak and Dagger, and Emptiness for their ETBs again.
* **Signposts:** Dark Leo & Shredder · Karai · Cloak and Dagger · Emptiness ·
  Abigale · Turncoat Kunoichi · Eirdu.

### GW — Counters & Tokens
* **Counter engines:**
  * Deanna Troi, Agent Bishop, Michelangelo, Weirdness to 11, Michelangelo,
    the Heart.
  * Dr. M'Benga (doubles counters) and Hulk, Brutal Brawler.
  * Germination Practicum (two counters on your team every turn, via Paradigm).
  * Okoye, Mighty and Adored (monarch), Jadzia Dax, Dancing from Dark to Dawn.
* **Counter payoffs:** Mikey & Leo and Phlox draw cards. Lieutenant Commander
  Data and Kinetic Ooze also use counters.
* **Tokens:**
  * Captain Jean-Luc Picard: an anthem, plus an Officer for every creature you cast.
  * Ajani, Outland Chaperone, Antiquities on the Loose, Triceraton Commander,
    Royal Talon Fighter Jet.
  * The Unbeatable Squirrel Girl, Holo-Engineer, Brigid, Enterprise-A.
  * The Arkenstone, Kwia Vigorbloom.
* **Signposts:** Mikey & Leo · Phlox · Okoye, Mighty and Adored · Figure of Fable ·
  Brigid · Kwia Vigorbloom · Jennifer Walters.

---

## Interaction

* **Removal:**
  * White: Swords, Erode, 70,000 Light-Years from Home, Prophesied End, and
    Harsh Annotation at 1–2 mana.
  * Black: Dark Deed, Vraska's Final Mercy, Bilbo's Deadly Slice, Death in the
    Family, Resistance Is Futile, Requiting Hex, Blight Rot, Lich's Relic.
  * Red: Bolt, Lightning Strike, Sear, Impractical Joke, Khaaaaaaaaaaaannn!,
    End-Blaze Epiphany, Explosive Prodigy.
  * Green: bite spells (Quarrel, Tenderize, Super Combo) and Konstrari Charm.
  * Blue: Noggle the Mind, Retro-Mutation.
* **Sweepers (10):** Ceaseless Conflict, Withering Curse, Avengers Disassembled,
  Jennika's Technique, Soul Immolation, Splatter Technique, The Last Ronin,
  Engineered Explosives, The Echoverse Fulcrum, Crystalline Entity.
* **Counterspells:** Wild Unraveling, Mana Sculpt, Countersculpt, Highly
  Illogical, Confusticate, and Glen Elendra's Answer. Theorix Charm, Wesley
  Crusher, Glen Elendra Guardian, and Subcommander T'Pol add soft counters.
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
| BG | Overgrown Tomb | Deathcap Glade | Turbulent Fen |
| RG | Stomping Ground | Rockfall Vale | Training Compound |
| RW | Sacred Foundry | Sundown Pass | Turbulent Steppe |
| WB | Godless Shrine | Shattered Sanctum | Eclipsed Steppe |
| GW | Temple Garden | Overgrown Farmland | Gathering Place |

* The Marvel duals enter untapped and can be tapped for either color if you
  control a basic.
* The typed checklands are new in the Strixhaven and Lorwyn Commander decks.
* **BG and RW** have no eligible untapped third dual (see *How the pool was
  built*). The mana simulator showed a tapped third dual still cuts color screw
  by about 1.1–1.4 points for little tempo cost. So they get Turbulent Fen and
  Turbulent Steppe, which beat the gainlands: they can enter untapped late, and
  Turbulent Fen is Forest-typed.
* Utility lands: **Surveillance Room** (any color) and **Great Hall of the
  Biblioplex** (spells).
* Fixing elsewhere: The Mind Stone, H.E.R.B.I.E., Lovable Robot, Weather Maker,
  Bloom Tender, Frog Butler, Great Forest Druid, Noxious Newt, Transdimensional
  Bovine.

---

## Trap audit

You asked me to avoid cards that imply synergy the cube doesn't have. For every
card that leans on something else, here is the support that exists in the final
list:

| Card(s) | Needs | In the cube |
|---|---|---|
| Splinter, Hamato Yoshi; Dark Leo & Shredder | Ninjas | 18 Ninja cards and token makers; 14 sneak cards |
| Kíli; Thorin; Dáin; Jane Foster; Captain America, Liberator | Equipment | 9 Equipment and 2 Axe-token makers |
| Mjölnir | "Worthy" creatures | 68 legendary non-Villain R/W creatures |
| High Perfect Morcant; Thranduil's Company; Trystan | Elves | 9 Elves |
| Codie | Prepared creatures | 21, plus about 15 flicker/bounce effects and 14 sneak cards |
| The seek-out payoffs | Extra draws | Mr. Spock, Decorum Dissertation, Leader, Seven of Nine (Unassimilated), Spock, Doom, Kurn, Gnarlbark, ~10 cantrips and instant-speed draws |
| Mikey & Leo; Phlox; M'Benga; Lt. Cmdr. Data | Counters on your creatures | Mutagen, Deanna Troi, Agent Bishop, both Hulks, Germination Practicum, plus every -1/-1 counter |
| Smaug ×2; Draconic Visitor | Treasure | 10 Treasure makers |
| Opus / prowess / noncreature payoffs | Instants and sorceries | 59, plus the prepared spells |
| Lyra, Archangel of Dawn (Angels and lifegain) | Lifegain | Works alone (she's an Angel); WB has lifelinkers |
| Gowron (draws if you sacrifice a Klingon); Picard (Spacecraft tutor) | Klingons; Spacecraft | Bonuses only, not needed. L'Rell and Worf make Klingons. There are 3 Spacecraft |

**Left out as traps** (strong cards whose synergy isn't in the cube):

* Devil Dinosaur (no Dinosaurs).
* Seven of Nine (the UB "dilemma" version).
* The Hero/Villain lords: Avengers Assemble!, The Masters of Evil, Baron Strucker,
  Madame Hydra.
* Behold and typal payoffs: the Lorwyn Champion cycle, Chronicle of Victory,
  Turtle Power!, An Unexpected Party.
* Quark, Humble Proprietor (its Treasures can't be sacrificed).
* Three-color cards, which testing showed had no home.
* The Federation and "Strange new worlds" cards, the "Way of the…" enchantments,
  and multiplayer-only Commander cards (Battlefront, goad, Council's dilemma).

## Close calls (good swap candidates)

These were cut on curve, color balance, or slot pressure, not power:
Super-Skrull, Savanti Romero, Silverquill, the Disputant, Moment of Reckoning,
Monica Rambeau, The Coming of Galactus, Overwrite the Multiverse, Age of Ultron,
Green Goblin, Back for More, Hulkling, Young Avenger, Iron Man, Tony Stark,
Klingon Strike Force, Gandalf, Spark Starter, Craftwork Crusher, Rhino, Terrible
Trampler, Edgar, Moonlit Sovereign, Ingris Stingerquill, Dina's Guidance,
Raphael's Technique, Your Fate Ends Here.

Every card cut from v1 is listed in [TESTING.md](TESTING.md). Filter
`data/eligible_pool.csv` on `in_cube` to browse the rest of the pool.

---

## Importing to CubeCobra

* Fastest: *Add/Remove → Bulk Upload →* paste `cube/2026_cube.txt`.
* With exact printings and tags: *Import → CSV →* `cube/2026_cube_cubecobra.csv`.
  The columns match CubeCobra's own CSV export. Tags are `;`-separated (for
  example `WU Blink;Prepared;Removal`).

## Rebuilding from Scryfall

```bash
python3 tools/fetch_sets.py raw ecl ecc pecl tmt tmc pza sos soc soa psos msh msc hob hoc fra frc pfra trk trc sds
```
```bash
python3 tools/build_pool.py raw raw/eligible_pool.json
```
```bash
python3 tools/export_data.py raw/eligible_pool.json
```
```bash
python3 tools/build_outputs.py
```

To change the cube, edit `cube/cube_list.txt` (and `tools/tags.py` and
`tools/sim/ratings.py` for any new card). Then re-run the last two commands,
and the simulators in `tools/sim/` to re-test.
