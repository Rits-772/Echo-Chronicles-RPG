# XP Minima RPG

**Terminal-first, stats-driven narrative RPG.**

A laptop-only, browser-less, pure-terminal RPG where player agency and stat-driven mechanics drive a branching narrative with multiple endings.

## Overview

XP Minima RPG is a text-based RPG inspired by the design philosophy of *Minima*. It emphasizes:

- **Stats-Driven Mechanics**: Player abilities unlock story paths based on Strength, Defence, Agility, Vitality, Wisdom, and Perception.
- **Modular Narrative**: Nodes and choices create a branching story that responds to player stats, flags, and inventory.
- **Terminal-First Design**: Play entirely in the terminal. No GUI, no dependencies beyond Python.
- **Incremental Growth**: Start with a single story arc. Scale modularly with more nodes, items, and mechanics.

## Current Phase: **Phase 1** ✨

**Phase 1 Features:**
- ✅ 40+ interconnected narrative nodes with branching paths
- ✅ Three distinct ending routes (Freedom, Guardian, Rebellion)
- ✅ Combat system with turn-based mechanics
- ✅ 10+ consumable items with stat-boost and healing effects
- ✅ NPC encounters (Elena, Lyra, Sarah, mysterious prisoner)
- ✅ Multiple narrative threads (manor investigation, escape, truth-seeking)
- ✅ Expanded world with multiple locations (manor, forest, village, mountains, underground)

## Features (Phase 1)

✅ **Narrative & World**
- 40+ fully interconnected story nodes
- Multiple branching paths based on stat checks and flags
- Secret passages and hidden areas
- Multiple ending routes with significant consequences

✅ **Combat System**
- Turn-based combat with player and enemy actions
- Stat-based damage calculations
- Defend mechanic to reduce incoming damage
- Simple enemy AI

✅ **Consumables & Items**
- Healing potions (restore HP)
- Mana potions (restore MP)
- Stat-boost consumables (Strength, Agility, Wisdom, etc.)
- Quest items that unlock narrative paths
- Weapons that provide stat bonuses
- Stat-based skill checks for narrative choices

✅ **Narrative System**
- Modular nodes (JSON-driven story segments)
- Branching choices with stat/flag/inventory requirements
- Dynamic effects that modify game state

✅ **Inventory & Items**
- Item management (add, remove, consume)
- Quest items and consumables with effects

✅ **Terminal Commands**
- `stats` – View current stats
- `inventory` – View inventory
- `levelup` – Allocate stat points
- `choose <n>` – Make a choice
- `save` – Save game
- `exit` – Save and quit

✅ **State Persistence**
- Player state saved/loaded from JSON
- World state management
- Session logging ready

## Installation

### Requirements
- Python 3.8+

### Setup

1. **Clone or extract the project:**
   ```bash
   cd "d:\Storage\Programs\Minima RPG"
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Run the game:**
   ```bash
   python main.py
   ```

## Game Structure

```
Minima RPG/
├── main.py                # Entry point
├── config/
│   └── settings.json      # Game-wide configuration
├── data/
│   ├── player/
│   │   └── player_state.json
│   ├── world/
│   │   └── world_state.json
│   └── nodes/
│       └── nodes.json     # All narrative nodes
├── engine/
│   ├── state_manager.py   # Load/save state
│   ├── rules.py           # Stat checks, level-up, formulas
│   ├── node_engine.py     # Node/choice processing
│   └── game_loop.py       # Main game loop
├── ui/
│   └── json_loader.py     # JSON utilities
├── logs/
│   └── session.log        # Session logs
└── tests/
    └── test_rules.py      # Unit tests
```

## Player Stats

| Stat | Start | Per Point | Role |
|------|-------|-----------|------|
| **HP** | 50 | +5 | Health pool |
| **MP** | 25 | +5 | Mana pool |
| **Strength** | 5 | +1 | Attack power |
| **Defence** | 5 | +1 | Damage reduction |
| **Agility** | 5 | +1 | Evasion, speed |
| **Vitality** | 5 | +1 | HP resilience |
| **Wisdom** | 5 | +1 | Magic efficiency |
| **Perception** | 5 | +1 | Hidden options, secrets |
| **Lifeforce** | 100 | N/A | Meta-life energy, immutable |

### Leveling
- **Starting Points**: 5 free stat points
- **Per Level-Up**: 2 stat points
- **Experience Threshold**: Base 100 XP, increases by 50 per level

## Gameplay

### Opening
You wake in a dim, abandoned manor with no memory. Explore, uncover clues, and make choices that branch the narrative.

### Mechanics
1. **Choose**: Enter a number (1, 2, 3, ...) to select a narrative choice.
2. **Stat Checks**: Some choices require specific stat values (e.g., Perception ≥ 7).
3. **Flags**: Boolean markers track events (e.g., `saw_symbol`, `key_found`).
4. **Inventory**: Carry items that unlock paths or apply effects.
5. **Level-Up**: Gain EXP from nodes and events. Reach thresholds to level up and allocate stat points.

### Example Game Flow
```
You wake up in a quiet, dim room...

1. Investigate the light carefully
2. Ignore the light and explore the room
3. Try to move and see if anything hurts

> 1
> Examine the symbol more closely
> Try to remember more
> Try to decipher the journal entries

[Explore, unlock paths, collect items, build stats]
```

## Commands

```
stats          Display current stats, level, EXP, free points
inventory      Show items carried
levelup        Allocate a free stat point
choose <n>     Select a choice (1, 2, 3, ...)
use <item>     Consume an item
move <node>    Jump to a node (debug)
save           Save game to JSON
exit           Save and quit
help           Show commands
```

## Story Overview (Phase 1)

You awaken in an abandoned manor with no memory. As you explore, you uncover a complex truth: you are a **seal**—a human anchor binding a powerful ancient entity to the space between worlds. The ritual that created you is weakening, and others are watching. 

Throughout the game, you'll encounter:
- **Elena**: A remorseful researcher who wants to help you escape
- **Lyra**: A mysterious figure seeking peaceful coexistence between worlds
- **The Entity**: An ancient, intelligent being trapped by human betrayal
- **Unknown Pursuers**: Those who want to reinforce the seal at any cost

Your choices determine not just your fate, but the fate of two civilizations. Three endings await:
1. **Freedom** - Escape and live a normal life, but leave the seal to break naturally
2. **Guardian** - Accept your role and protect the world by maintaining the binding
3. **Rebellion** - Break the seal intentionally and reshape reality itself

### Adding Nodes
Edit `data/nodes/nodes.json`. Each node has:
```json
{
  "intro_01": {
    "text": "Narrative text shown to player.",
    "choices": [
      {
        "label": "Player-facing choice text",
        "requirements": {
          "stats": {"perception": 5},
          "flags": {"saw_light": true},
          "items": ["torch"]
        },
        "effects": {
          "stats": {"hp": -5},
          "flags": {"used_torch": true},
          "items": [{"name": "ash", "type": "consumable"}],
          "experience": 25
        },
        "next": "next_node_id"
      }
    ]
  }
}
```

### Adding Items
Items are stored in inventory and referenced in `effects`:
```json
{
  "name": "Healing Potion",
  "type": "consumable",
  "effect": {"hp": 20}
}
```

### Adding Combat
Edit `engine/rules.py` to expand `calculate_damage()` and add new methods like `perform_combat()`.

### Adding LLM Text Flavor
Integrate an LLM API (OpenAI, Anthropic, etc.) into `game_loop.py` to dynamically enhance node text without affecting mechanics.

## Testing

Run the test suite:
```bash
python -m pytest tests/
# or
python -m unittest discover tests/
```

Current tests cover:
- Stat allocation and scaling
- Experience and level-up mechanics
- Stat checks
- Damage calculations
- Node requirement validation
- Effect application

## Roadmap

### Phase 1 (Current)
✅ Intro sequence with 40+ nodes
✅ Combat system skeleton
✅ Consumable items
✅ Multiple endings based on stats/flags
✅ NPC encounters and dialogue

### Phase 2
- Interactive combat (player chooses actions each turn)
- More enemy types and combat encounters embedded in narrative
- Equipment system (armor, jewelry, weapons with synergy)
- Skill trees and special abilities
- More detailed NPC questlines
- Expanded world (neighboring regions, dungeons)

### Phase 3
- LLM-driven text generation for flavor text
- Randomized encounters and procedural elements
- Save/load multiple profiles
- New Game+ mode with story variations
- Music and sound effects (optional terminal integration)
- Analytics dashboard for player choices and endings

## Credits

Designed with the philosophy of *Minima*: minimal resources, maximum agency.

## License

MIT License

---

**Get started:** `python main.py`
