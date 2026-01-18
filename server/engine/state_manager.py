"""
State Manager: Handles loading/saving player and world state from JSON.
Tracks player stats, inventory, flags, and current narrative position.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class StateManager:
    """Manages game state persistence and retrieval."""
    
    def __init__(self, settings_path: str):
        """
        Initialize StateManager with settings file.
        
        Args:
            settings_path: Path to settings.json
        """
        self.settings = self._load_json(settings_path)
        self.base_path = Path(settings_path).parent.parent  # Root of project
        
        # Construct full paths
        self.player_state_path = self.base_path / self.settings["paths"]["player_state"]
        self.world_state_path = self.base_path / self.settings["paths"]["world_state"]
        self.nodes_path = self.base_path / self.settings["paths"]["nodes"]
        
    @staticmethod
    def _load_json(path: str) -> Dict[str, Any]:
        """Load JSON from file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def _save_json(path: Path, data: Dict[str, Any]) -> None:
        """Save JSON to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load_player_state(self) -> Dict[str, Any]:
        """Load player state from JSON."""
        # Check if active save exists
        if not self.player_state_path.exists():
            # Check for template
            template_path = self.player_state_path.parent / "player_template.json"
            if template_path.exists():
                # Create new save from template
                initial_state = self._load_json(str(template_path))
                self.save_player_state(initial_state)
                return initial_state
            
            raise FileNotFoundError(f"Player state not found at {self.player_state_path} and no template found.")
            
        return self._load_json(str(self.player_state_path))
    
    def save_player_state(self, state: Dict[str, Any]) -> None:
        """Save player state to JSON."""
        self._save_json(self.player_state_path, state)
    
    def load_world_state(self) -> Dict[str, Any]:
        """Load world state from JSON."""
        if not self.world_state_path.exists():
            return {}
        return self._load_json(str(self.world_state_path))
    
    def save_world_state(self, state: Dict[str, Any]) -> None:
        """Save world state to JSON."""
        self._save_json(self.world_state_path, state)
    
    def load_nodes(self) -> Dict[str, Any]:
        """Load narrative nodes from JSON files."""
        if not self.nodes_path.exists():
            raise FileNotFoundError(f"Nodes not found at {self.nodes_path}")
            
        if self.nodes_path.is_file():
            return self._load_json(str(self.nodes_path))
            
        # Recursive load if directory
        nodes = {}
        if self.nodes_path.is_dir():
             for file_path in self.nodes_path.glob("*.json"):
                 try:
                     node_data = self._load_json(str(file_path))
                     nodes.update(node_data)
                 except Exception as e:
                     print(f"[WARN] Failed to load nodes from {file_path}: {e}")
        return nodes
    
    def get_setting(self, *keys: str) -> Any:
        """
        Get a setting from settings.json using dot notation.
        
        Example: get_setting("player", "starting_level") -> 1
        """
        value = self.settings
        for key in keys:
            value = value[key]
        return value


class PlayerState:
    """Wrapper for player state with convenient accessors."""
    
    def __init__(self, state_dict: Dict[str, Any]):
        """Initialize with a state dictionary."""
        self.data = state_dict
    
    @property
    def stats(self) -> Dict[str, int]:
        return self.data["stats"]
    
    @property
    def inventory(self) -> list:
        return self.data["inventory"]
    
    @property
    def flags(self) -> Dict[str, bool]:
        return self.data["flags"]
    
    @property
    def current_node(self) -> str:
        return self.data["current_node"]
    
    def get_stat(self, stat_name: str) -> int:
        """Get a specific stat value."""
        return self.stats.get(stat_name, 0)
    
    def set_stat(self, stat_name: str, value: int) -> None:
        """Set a specific stat value."""
        self.stats[stat_name] = value
    
    def add_stat(self, stat_name: str, value: int) -> None:
        """Add to a stat value."""
        self.stats[stat_name] = self.stats.get(stat_name, 0) + value
    
    def set_flag(self, flag_name: str, value: bool = True) -> None:
        """Set a narrative flag."""
        self.flags[flag_name] = value
    
    def has_flag(self, flag_name: str) -> bool:
        """Check if a flag is set."""
        return self.flags.get(flag_name, False)
    
    def add_item(self, item: Dict[str, Any]) -> None:
        """Add item to inventory."""
        self.inventory.append(item)
    
    def remove_item(self, item_name: str) -> bool:
        """Remove item from inventory by name. Returns True if found and removed."""
        for i, item in enumerate(self.inventory):
            if item.get("name") == item_name:
                self.inventory.pop(i)
                return True
        return False
    
    def has_item(self, item_name: str) -> bool:
        """Check if player has an item."""
        return any(item.get("name") == item_name for item in self.inventory)
    
    def move_to_node(self, node_id: str) -> None:
        """Move player to a different node."""
        self.data["current_node"] = node_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert back to dictionary for saving."""
        return self.data
