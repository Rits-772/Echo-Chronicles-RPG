"""
Combat Engine: Handles turn-based combat between player and enemies.
Encapsulates combat mechanics, turn order, and battle outcomes.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import random


class CombatAction(Enum):
    """Types of combat actions."""
    ATTACK = "attack"
    DEFEND = "defend"
    CAST_SPELL = "cast_spell"
    USE_ITEM = "use_item"
    FLEE = "flee"


class Enemy:
    """Represents an enemy in combat."""
    
    def __init__(self, name: str, hp: int, attack_power: int, defence: int, 
                 exp_reward: int, loot: Optional[List[Dict[str, Any]]] = None):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack_power = attack_power
        self.defence = defence
        self.exp_reward = exp_reward
        self.loot = loot or []
        self.is_alive = True
    
    def take_damage(self, damage: int) -> None:
        """Apply damage to enemy."""
        self.hp = max(0, self.hp - damage)
        if self.hp <= 0:
            self.is_alive = False
    
    def get_action(self) -> CombatAction:
        """Enemy AI: choose an action."""
        # Simple AI: attack with 70% chance, defend with 30%
        return CombatAction.ATTACK if random.random() < 0.7 else CombatAction.DEFEND


from dataclasses import dataclass, field

@dataclass
class CombatState:
    enemy: 'Enemy'
    log: List[str] = field(default_factory=list)
    turn_count: int = 0
    is_active: bool = True
    victory: bool = False
    
class CombatEngine:
    """Manages turn-based combat statefully."""
    
    """Manages turn-based combat statefully."""
    
    def __init__(self, rules_engine, data_dir=None):
        self.rules_engine = rules_engine
        self.enemies = []
        self.items = {}
        
        if data_dir:
            import json
            from pathlib import Path
            
            # Load Enemies
            enemies_path = Path(data_dir) / "enemies.json"
            if enemies_path.exists():
                with open(enemies_path, 'r') as f:
                    self.enemies = json.load(f)
                    
            # Load Items
            items_path = Path(data_dir) / "items.json"
            if items_path.exists():
                with open(items_path, 'r') as f:
                    # indexed by ID
                    items_list = json.load(f)
                    self.items = {item['id']: item for item in items_list}

    def get_random_enemy(self, difficulty: int) -> Enemy:
        """Get a random enemy appropriate for the difficulty."""
        candidates = [e for e in self.enemies if e.get("difficulty", 1) <= difficulty]
        if not candidates:
            # Fallback
            return Enemy("Rat", 10, 3, 0, 5)
            
        data = random.choice(candidates)
        return Enemy(
            name=data["name"],
            hp=data["hp"],
            attack_power=data["attack_power"],
            defence=data["defence"],
            exp_reward=data["exp_reward"],
            loot=data.get("loot_table", [])
        )
    
    def initialize_combat(self, enemy: Enemy) -> CombatState:
        """Start a new combat encounter."""
        return CombatState(
            enemy=enemy,
            log=[f"You encounter a {enemy.name}!"],
            is_active=True
        )
        
    def process_turn(self, state: CombatState, player_stats: Dict[str, Any], 
                    player_inventory: List[Dict[str, Any]], player_action: CombatAction,
                    player_equipment: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a single turn of combat.
        Returns a dict with the result of the turn to send to UI.
        """
        if not state.is_active:
            return {"error": "Combat is not active"}
            
        enemy = state.enemy
        log = []
        state.turn_count += 1
        
        # Player Turn
        player_defending = player_action == CombatAction.DEFEND
        
        if player_action == CombatAction.ATTACK:
            damage = self.rules_engine.calculate_damage(player_stats, {"defence": enemy.defence}, player_equipment)
            enemy.take_damage(damage)
            log.append(f"You attack {enemy.name} for {damage} damage!")
        elif player_action == CombatAction.DEFEND:
            log.append("You take a defensive stance.")
        elif player_action == CombatAction.FLEE:
            if self.can_flee(player_stats.get("agility", 5), enemy.defence):
                state.is_active = False
                log.append("You managed to escape!")
                state.log.extend(log)
                return self._build_turn_result(state, log)
            else:
                log.append("Failed to escape!")
        
        # Check Enemy Death
        if not enemy.is_alive:
            state.victory = True
            state.is_active = False
            exp = enemy.exp_reward
            self.rules_engine.add_experience(player_stats, exp)
            log.append(f"Victory! You defeated {enemy.name} and gained {exp} XP.")
            
            # Loot Logic
            if enemy.loot:
                for drop in enemy.loot:
                    if random.random() < drop["chance"]:
                        item_id = drop["item_id"]
                        item_data = self.items.get(item_id)
                        if item_data:
                            # Clone item to avoid ref issues
                            new_item = item_data.copy()
                            player_inventory.append(new_item)
                            log.append(f"Loot dropped: {new_item['name']}")
            
            state.log.extend(log)
            return self._build_turn_result(state, log)
            
        # Enemy Turn
        enemy_action = enemy.get_action()
        if enemy_action == CombatAction.ATTACK:
            damage = random.randint(1, 3) + max(0, enemy.attack_power - 5) # Reduced randomness base
            if player_defending:
                damage = max(1, damage // 2)
                log.append("Your defence reduced the damage!")
            
            if not self.rules_engine.apply_damage(player_stats, damage):
                log.append(f"{enemy.name} hits you for {damage} damage! You have been slain...")
                state.is_active = False
                state.victory = False # Loss
            else:
                log.append(f"{enemy.name} attacks you for {damage} damage.")
        
        state.log.extend(log)
        return self._build_turn_result(state, log)

    def _build_turn_result(self, state: CombatState, current_turn_log: List[str]) -> Dict[str, Any]:
        """Helper to build consistent response."""
        return {
            "is_active": state.is_active,
            "victory": state.victory,
            "enemy": {
                "name": state.enemy.name,
                "hp": state.enemy.hp,
                "max_hp": state.enemy.max_hp
            },
            "log": state.log[-10:], # Return last 10 log entries for UI
            "turn_log": current_turn_log
        }

    def can_flee(self, player_agility: int, enemy_defence: int) -> bool:
        """Attempt to flee."""
        flee_chance = max(0.2, (player_agility - enemy_defence) * 0.05 + 0.3)
        return random.random() < flee_chance
