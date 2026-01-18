"""
Node Engine: Processes narrative nodes and validates choice requirements.
Routes player actions to next nodes and applies effects.
"""

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

if False:
    from engine.rules import RulesEngine


class NodeProcessResult:
    """Result of processing a node/choice."""
    
    def __init__(self, success: bool, message: str = "", next_node: Optional[str] = None, effects: Optional[Dict[str, Any]] = None):
        self.success = success
        self.message = message
        self.next_node = next_node
        self.effects = effects or {}


class NodeEngine:
    """Processes narrative nodes and handles choice logic."""
    
    def __init__(self, nodes_data: Dict[str, Any], rules_engine: 'RulesEngine'):
        """
        Initialize NodeEngine.
        
        Args:
            nodes_data: Dictionary of node definitions
            rules_engine: RulesEngine instance for stat checks
        """
        self.nodes = nodes_data
        self.rules_engine = rules_engine
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a node by ID."""
        return self.nodes.get(node_id)
    
    def validate_requirements(self, player_stats: Dict[str, int], player_flags: Dict[str, bool],
                              player_inventory: List[Dict[str, Any]], 
                              requirements: Dict[str, Any]) -> bool:
        """
        Validate if player meets all requirements for a choice.
        
        Requirements format:
        {
            "stats": {"stat_name": min_value, ...},
            "flags": {"flag_name": required_value, ...},
            "items": ["item_name", ...]
        }
        """
        if not requirements:
            return True
        
        # Check stats
        if "stats" in requirements:
            for stat_name, min_value in requirements["stats"].items():
                if player_stats.get(stat_name, 0) < min_value:
                    return False
        
        # Check flags
        if "flags" in requirements:
            for flag_name, required_value in requirements["flags"].items():
                if player_flags.get(flag_name, False) != required_value:
                    return False
        
        # Check inventory
        if "items" in requirements:
            for item_name in requirements["items"]:
                has_item = any(item.get("name") == item_name for item in player_inventory)
                if not has_item:
                    return False
        
        return True
    
    def apply_effects(self, player_stats: Dict[str, int], player_flags: Dict[str, bool],
                      player_inventory: List[Dict[str, Any]], effects: Dict[str, Any]) -> None:
        """
        Apply effects to player state.
        
        Effects format:
        {
            "stats": {"stat_name": delta, ...},
            "flags": {"flag_name": value, ...},
            "items": [{"name": "...", "type": "...", "effect": {...}}, ...],
            "experience": amount
        }
        """
        if not effects:
            return
        
        # Apply stat changes
        if "stats" in effects:
            for stat_name, delta in effects["stats"].items():
                if stat_name in player_stats:
                    player_stats[stat_name] += delta
        
        # Apply flag changes
        if "flags" in effects:
            for flag_name, value in effects["flags"].items():
                player_flags[flag_name] = value
        
        # Add items
        if "items" in effects:
            for item in effects["items"]:
                player_inventory.append(item)
        
        # Add experience
        if "experience" in effects:
            self.rules_engine.add_experience(player_stats, effects["experience"])
    
    def get_available_choices(self, player_stats: Dict[str, int], player_flags: Dict[str, bool],
                              player_inventory: List[Dict[str, Any]], node_id: str) -> Tuple[Optional[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Get available choices for a node, filtering by requirements.
        
        Returns (node_dict, filtered_choices)
        """
        node = self.get_node(node_id)
        if not node:
            return None, []
        
        available_choices = []
        if "choices" in node:
            for i, choice in enumerate(node["choices"]):
                requirements = choice.get("requirements", {})
                if self.validate_requirements(player_stats, player_flags, player_inventory, requirements):
                    # Add choice index for selection
                    choice_with_index = choice.copy()
                    choice_with_index["_index"] = i
                    available_choices.append(choice_with_index)
        
        return node, available_choices
    
    def process_choice(self, player_stats: Dict[str, int], player_flags: Dict[str, bool],
                       player_inventory: List[Dict[str, Any]], node_id: str, choice_index: int) -> NodeProcessResult:
        """
        Process a player choice at a node.
        
        Args:
            player_stats: Player stat dictionary
            player_flags: Player flag dictionary
            player_inventory: Player inventory list
            node_id: Current node ID
            choice_index: Index of the choice selected
        
        Returns:
            NodeProcessResult with success status, next node, and effects applied
        """
        node = self.get_node(node_id)
        if not node:
            return NodeProcessResult(False, f"Node '{node_id}' not found")
        
        if "choices" not in node or choice_index < 0 or choice_index >= len(node["choices"]):
            return NodeProcessResult(False, "Invalid choice")
        
        choice = node["choices"][choice_index]
        
        # Validate requirements
        requirements = choice.get("requirements", {})
        if not self.validate_requirements(player_stats, player_flags, player_inventory, requirements):
            return NodeProcessResult(False, "Choice requirements not met")
        
        # Apply effects
        effects = choice.get("effects", {})
        self.apply_effects(player_stats, player_flags, player_inventory, effects)
        
        # Get next node
        next_node = choice.get("next", node_id)
        
        return NodeProcessResult(
            success=True,
            message=choice.get("label", ""),
            next_node=next_node,
            effects=effects
        )
    
    def render_node_text(self, node_id: str) -> str:
        """Get display text for a node."""
        node = self.get_node(node_id)
        if not node:
            return f"Node '{node_id}' not found"
        return node.get("text", "")
