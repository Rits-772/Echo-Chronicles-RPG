"""
Consumables data: Potions, elixirs, and usable items.
"""

CONSUMABLES = {
    "Healing Potion": {
        "type": "consumable",
        "description": "Restores 30 HP",
        "effect": {
            "hp": 30
        }
    },
    "Greater Healing Potion": {
        "type": "consumable",
        "description": "Restores 60 HP",
        "effect": {
            "hp": 60
        }
    },
    "Mana Potion": {
        "type": "consumable",
        "description": "Restores 20 MP",
        "effect": {
            "mp": 20
        }
    },
    "Mana Elixir": {
        "type": "consumable",
        "description": "Restores 40 MP",
        "effect": {
            "mp": 40
        }
    },
    "Strength Draught": {
        "type": "consumable",
        "description": "Temporarily increases Strength by 2 for one encounter",
        "effect": {
            "strength": 2
        }
    },
    "Vitality Brew": {
        "type": "consumable",
        "description": "Temporarily increases Vitality by 2",
        "effect": {
            "vitality": 2
        }
    },
    "Agility Tonic": {
        "type": "consumable",
        "description": "Temporarily increases Agility by 2",
        "effect": {
            "agility": 2
        }
    },
    "Wisdom Tea": {
        "type": "consumable",
        "description": "Temporarily increases Wisdom by 2",
        "effect": {
            "wisdom": 2
        }
    },
    "Perception Essence": {
        "type": "consumable",
        "description": "Temporarily increases Perception by 2",
        "effect": {
            "perception": 2
        }
    },
    "Antidote": {
        "type": "consumable",
        "description": "Cures poison",
        "effect": {}
    }
}
