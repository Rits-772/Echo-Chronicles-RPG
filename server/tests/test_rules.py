"""
Test suite for Rules Engine.
Tests stat calculations, level-up mechanics, and game formulas.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine.rules import RulesEngine


class TestRulesEngine(unittest.TestCase):
    """Test cases for RulesEngine."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.settings = {
            "scaling": {
                "hp_per_point": 5,
                "mp_per_point": 5,
                "other_stats_per_point": 1
            },
            "experience": {
                "exp_per_node": 10,
                "level_up_threshold": 100,
                "threshold_increase_per_level": 50
            },
            "player": {
                "level_up_points": 2
            }
        }
        self.rules = RulesEngine(self.settings)
        
        # Standard player stats
        self.player_stats = {
            "level": 1,
            "experience": 0,
            "free_stat_points": 5,
            "hp": 50,
            "mp": 25,
            "strength": 5,
            "defence": 5,
            "agility": 5,
            "vitality": 5,
            "wisdom": 5,
            "perception": 5,
            "lifeforce": 100
        }
    
    def test_level_up_threshold_calculation(self):
        """Test level up threshold formula."""
        # Level 1: 100
        self.assertEqual(self.rules.calculate_level_up_threshold(1), 100)
        # Level 2: 100 + 50 = 150
        self.assertEqual(self.rules.calculate_level_up_threshold(2), 150)
        # Level 3: 100 + 100 = 200
        self.assertEqual(self.rules.calculate_level_up_threshold(3), 200)
    
    def test_process_level_up(self):
        """Test level up grants stat points."""
        initial_level = self.player_stats["level"]
        initial_points = self.player_stats["free_stat_points"]
        
        self.rules.process_level_up(self.player_stats)
        
        self.assertEqual(self.player_stats["level"], initial_level + 1)
        self.assertEqual(self.player_stats["free_stat_points"], initial_points + 2)
        self.assertEqual(self.player_stats["experience"], 0)
    
    def test_allocate_stat_point_hp(self):
        """Test allocating point to HP scales by 5."""
        self.rules.allocate_stat_point(self.player_stats, "hp")
        self.assertEqual(self.player_stats["hp"], 55)  # 50 + 5
        self.assertEqual(self.player_stats["free_stat_points"], 4)
    
    def test_allocate_stat_point_strength(self):
        """Test allocating point to strength scales by 1."""
        self.rules.allocate_stat_point(self.player_stats, "strength")
        self.assertEqual(self.player_stats["strength"], 6)  # 5 + 1
        self.assertEqual(self.player_stats["free_stat_points"], 4)
    
    def test_allocate_stat_point_lifeforce_blocked(self):
        """Test that lifeforce cannot be allocated."""
        result = self.rules.allocate_stat_point(self.player_stats, "lifeforce")
        self.assertFalse(result)
        self.assertEqual(self.player_stats["lifeforce"], 100)
        self.assertEqual(self.player_stats["free_stat_points"], 5)
    
    def test_allocate_stat_point_no_points(self):
        """Test allocation fails when no free points."""
        self.player_stats["free_stat_points"] = 0
        result = self.rules.allocate_stat_point(self.player_stats, "strength")
        self.assertFalse(result)
    
    def test_stat_check_success(self):
        """Test stat check passes when stat >= difficulty."""
        result = self.rules.perform_stat_check(self.player_stats, "strength", 5)
        self.assertTrue(result)
    
    def test_stat_check_failure(self):
        """Test stat check fails when stat < difficulty."""
        result = self.rules.perform_stat_check(self.player_stats, "strength", 10)
        self.assertFalse(result)
    
    def test_add_experience_no_level_up(self):
        """Test adding experience without reaching threshold."""
        result = self.rules.add_experience(self.player_stats, 50)
        self.assertFalse(result)
        self.assertEqual(self.player_stats["experience"], 50)
        self.assertEqual(self.player_stats["level"], 1)
    
    def test_add_experience_with_level_up(self):
        """Test adding experience that triggers level up."""
        result = self.rules.add_experience(self.player_stats, 100)
        self.assertTrue(result)
        self.assertEqual(self.player_stats["level"], 2)
        self.assertEqual(self.player_stats["experience"], 0)
        self.assertEqual(self.player_stats["free_stat_points"], 7)  # 5 + 2
    
    def test_calculate_damage(self):
        """Test damage calculation."""
        attacker = {"strength": 7}
        defender = {"defence": 5}
        damage = self.rules.calculate_damage(attacker, defender)
        # base 5 + (7-5) strength bonus - (5-5)/2 defence reduction = 5 + 2 - 0 = 7
        self.assertEqual(damage, 7)
    
    def test_calculate_damage_minimum(self):
        """Test damage has minimum of 1."""
        attacker = {"strength": 3}
        defender = {"defence": 10}
        damage = self.rules.calculate_damage(attacker, defender)
        self.assertGreaterEqual(damage, 1)
    
    def test_apply_damage(self):
        """Test damage reduces HP."""
        result = self.rules.apply_damage(self.player_stats, 10)
        self.assertTrue(result)  # Still alive
        self.assertEqual(self.player_stats["hp"], 40)
    
    def test_apply_damage_death(self):
        """Test damage can kill player."""
        result = self.rules.apply_damage(self.player_stats, 60)
        self.assertFalse(result)  # Dead
        self.assertEqual(self.player_stats["hp"], 0)
    
    def test_heal(self):
        """Test healing increases HP."""
        self.player_stats["hp"] = 30
        self.rules.heal(self.player_stats, 20)
        self.assertEqual(self.player_stats["hp"], 50)
    
    def test_heal_capped(self):
        """Test healing doesn't exceed max HP."""
        self.player_stats["hp"] = 40
        self.rules.heal(self.player_stats, 20)
        self.assertEqual(self.player_stats["hp"], 50)
    
    def test_is_alive(self):
        """Test alive check."""
        self.assertTrue(self.rules.is_alive(self.player_stats))
        self.player_stats["hp"] = 0
        self.assertFalse(self.rules.is_alive(self.player_stats))


class TestNodeRequirements(unittest.TestCase):
    """Test cases for node engine requirement validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.settings = {
            "scaling": {
                "hp_per_point": 5,
                "mp_per_point": 5,
                "other_stats_per_point": 1
            },
            "experience": {
                "exp_per_node": 10,
                "level_up_threshold": 100,
                "threshold_increase_per_level": 50
            },
            "player": {
                "level_up_points": 2
            }
        }
        from engine.rules import RulesEngine
        from engine.node_engine import NodeEngine
        
        self.rules_engine = RulesEngine(self.settings)
        self.node_engine = NodeEngine({}, self.rules_engine)
        
        self.player_stats = {
            "strength": 10,
            "defence": 5,
            "perception": 8
        }
        self.player_flags = {"key_found": True}
        self.inventory = [{"name": "sword", "type": "weapon"}]
    
    def test_validate_empty_requirements(self):
        """Test empty requirements always pass."""
        result = self.node_engine.validate_requirements(
            self.player_stats,
            self.player_flags,
            self.inventory,
            {}
        )
        self.assertTrue(result)
    
    def test_validate_stat_requirement_pass(self):
        """Test stat requirement passes."""
        requirements = {"stats": {"strength": 10}}
        result = self.node_engine.validate_requirements(
            self.player_stats,
            self.player_flags,
            self.inventory,
            requirements
        )
        self.assertTrue(result)
    
    def test_validate_stat_requirement_fail(self):
        """Test stat requirement fails."""
        requirements = {"stats": {"strength": 15}}
        result = self.node_engine.validate_requirements(
            self.player_stats,
            self.player_flags,
            self.inventory,
            requirements
        )
        self.assertFalse(result)
    
    def test_validate_flag_requirement(self):
        """Test flag requirement."""
        requirements = {"flags": {"key_found": True}}
        result = self.node_engine.validate_requirements(
            self.player_stats,
            self.player_flags,
            self.inventory,
            requirements
        )
        self.assertTrue(result)
    
    def test_validate_item_requirement(self):
        """Test item requirement."""
        requirements = {"items": ["sword"]}
        result = self.node_engine.validate_requirements(
            self.player_stats,
            self.player_flags,
            self.inventory,
            requirements
        )
        self.assertTrue(result)
    
    def test_validate_item_requirement_fail(self):
        """Test item requirement fails."""
        requirements = {"items": ["wand"]}
        result = self.node_engine.validate_requirements(
            self.player_stats,
            self.player_flags,
            self.inventory,
            requirements
        )
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
