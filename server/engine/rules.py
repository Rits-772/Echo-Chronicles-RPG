"""
Rules Engine: Handles stat checks, leveling, damage calculations, and game formulas.
Encapsulates all game mechanics and balance logic.
"""

from typing import Dict, Any, Optional
from enum import Enum


class StatCheck(Enum):
    """Types of stat checks."""
    STRENGTH = "strength"
    DEFENCE = "defence"
    AGILITY = "agility"
    VITALITY = "vitality"
    WISDOM = "wisdom"
    PERCEPTION = "perception"


class RulesEngine:
    """Encapsulates all game rules and formulas."""
    
    def __init__(self, settings: Dict[str, Any]):
        """Initialize rules with game settings."""
        self.settings = settings
        self.stat_scaling = settings["scaling"]
        self.exp_config = settings["experience"]
        self.player_config = settings["player"]
    
    def calculate_level_up_threshold(self, level: int) -> int:
        """
        Calculate experience threshold for a given level.
        
        Formula: base_threshold + (threshold_increase * (level - 1))
        """
        base = self.exp_config["level_up_threshold"]
        increase = self.exp_config["threshold_increase_per_level"]
        return base + (increase * (level - 1))
    
    def process_level_up(self, player_stats: Dict[str, int]) -> None:
        """
        Process a level up, granting stat points.
        
        Modifies player_stats in-place, adding free_stat_points.
        """
        level = player_stats.get("level", 1)
        points_granted = self.player_config["level_up_points"]
        
        player_stats["level"] = level + 1
        player_stats["free_stat_points"] = player_stats.get("free_stat_points", 0) + points_granted
        player_stats["experience"] = 0  # Reset experience for next level
    
    def allocate_stat_point(self, player_stats: Dict[str, Any], stat_name: str) -> bool:
        """
        Allocate one free stat point to a stat.
        
        Returns True if successful, False if no points available or invalid stat.
        Stat name cannot be 'lifeforce'.
        """
        if stat_name == "lifeforce":
            return False
        
        if stat_name not in player_stats:
            return False
        
        free_points = player_stats.get("free_stat_points", 0)
        if free_points <= 0:
            return False
        
        # Apply scaling
        if stat_name in ["hp", "mp"]:
            scaling = self.stat_scaling["hp_per_point" if stat_name == "hp" else "mp_per_point"]
        else:
            scaling = self.stat_scaling["other_stats_per_point"]
        
        player_stats[stat_name] += scaling
        player_stats["free_stat_points"] -= 1
        return True
    
    def perform_stat_check(self, player_stats: Dict[str, int], stat_name: str, difficulty: int) -> bool:
        """
        Perform a stat check against a difficulty.
        
        Returns True if stat >= difficulty, False otherwise.
        """
        stat_value = player_stats.get(stat_name, 0)
        return stat_value >= difficulty
    
    def add_experience(self, player_stats: Dict[str, int], amount: int) -> bool:
        """
        Add experience to player. Returns True if player leveled up.
        """
        player_stats["experience"] = player_stats.get("experience", 0) + amount
        level = player_stats.get("level", 1)
        threshold = self.calculate_level_up_threshold(level)
        
        if player_stats["experience"] >= threshold:
            self.process_level_up(player_stats)
            return True
        return False
    
    def calculate_damage(self, attacker_stats: Dict[str, int], defender_stats: Dict[str, int], attacker_equipment: Dict[str, Any] = None) -> int:
        """
        Calculate damage from attacker to defender.
        
        Formula: base_damage + strength_bonus + weapon_bonus - defence_reduction
        base_damage = 5
        """
        base_damage = 5
        strength_bonus = attacker_stats.get("strength", 5) - 5  # Above baseline
        
        # Equipment bonus
        weapon_bonus = 0
        if attacker_equipment and attacker_equipment.get("weapon"):
            weapon_bonus = attacker_equipment["weapon"].get("effect", {}).get("strength", 0)

        defence_reduction = max(0, (defender_stats.get("defence", 5) - 5) // 2)
        
        damage = base_damage + strength_bonus + weapon_bonus - defence_reduction
        return max(1, damage)  # Minimum 1 damage
    
    def apply_damage(self, player_stats: Dict[str, int], damage: int) -> bool:
        """
        Apply damage to player HP. Returns True if player survives.
        """
        current_hp = player_stats.get("hp", 50)
        player_stats["hp"] = max(0, current_hp - damage)
        return player_stats["hp"] > 0
    
    def heal(self, player_stats: Dict[str, int], amount: int) -> None:
        """Heal player HP (capped at max HP for their vitality)."""
        max_hp = 50 + (player_stats.get("vitality", 5) - 5) * self.stat_scaling["hp_per_point"]
        current_hp = player_stats.get("hp", 50)
        player_stats["hp"] = min(max_hp, current_hp + amount)
    
    def restore_mana(self, player_stats: Dict[str, int], amount: int) -> None:
        """Restore player MP (capped at max MP for their wisdom)."""
        max_mp = 25 + (player_stats.get("wisdom", 5) - 5) * self.stat_scaling["mp_per_point"]
        current_mp = player_stats.get("mp", 25)
        player_stats["mp"] = min(max_mp, current_mp + amount)
    
    def is_alive(self, player_stats: Dict[str, int]) -> bool:
        """Check if player is alive."""
        return player_stats.get("hp", 0) > 0
