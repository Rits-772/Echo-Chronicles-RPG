"""
Game Loop: Controls main game progression, handles player input, and manages game state.
"""

import sys
from typing import Dict, Any, Optional
from engine.state_manager import StateManager, PlayerState
from engine.rules import RulesEngine
from engine.node_engine import NodeEngine


class GameLoop:
    """Main game loop controller."""
    
    def __init__(self, state_manager: StateManager):
        """
        Initialize GameLoop with necessary managers.
        
        Args:
            state_manager: StateManager instance
        """
        self.state_manager = state_manager
        
        # Load settings and engines
        settings = state_manager.settings
        self.rules_engine = RulesEngine(settings)
        
        nodes_data = state_manager.load_nodes()
        self.node_engine = NodeEngine(nodes_data, self.rules_engine)
        
        # Load player state
        player_data = state_manager.load_player_state()
        self.player = PlayerState(player_data)
        
        # Game state
        self.running = True
        self.game_over = False
        self.victory = False
    
    def save_game(self) -> None:
        """Save current game state."""
        self.state_manager.save_player_state(self.player.to_dict())
    
    def display_stats(self) -> None:
        """Display player stats."""
        stats = self.player.stats
        print("\n" + "="*50)
        print("PLAYER STATS")
        print("="*50)
        print(f"Level: {stats['level']} | EXP: {stats['experience']}")
        print(f"Free Stat Points: {stats['free_stat_points']}")
        print("-"*50)
        print(f"HP: {stats['hp']}")
        print(f"MP: {stats['mp']}")
        print(f"Lifeforce: {stats['lifeforce']}")
        print("-"*50)
        print(f"Strength:   {stats['strength']}")
        print(f"Defence:    {stats['defence']}")
        print(f"Agility:    {stats['agility']}")
        print(f"Vitality:   {stats['vitality']}")
        print(f"Wisdom:     {stats['wisdom']}")
        print(f"Perception: {stats['perception']}")
        print("="*50 + "\n")
    
    def display_inventory(self) -> None:
        """Display player inventory."""
        print("\n" + "="*50)
        print("INVENTORY")
        print("="*50)
        if not self.player.inventory:
            print("Empty")
        else:
            for i, item in enumerate(self.player.inventory, 1):
                item_type = item.get("type", "unknown")
                print(f"{i}. {item['name']} ({item_type})")
        print("="*50 + "\n")
    
    def display_node(self) -> None:
        """Display current node text and available choices."""
        node_id = self.player.current_node
        node_text = self.node_engine.render_node_text(node_id)
        node, choices = self.node_engine.get_available_choices(
            self.player.stats,
            self.player.flags,
            self.player.inventory,
            node_id
        )
        
        print("\n" + "="*50)
        print(node_text)
        print("="*50)
        
        if choices:
            print("\nChoices:")
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice['label']}")
        else:
            print("\nNo choices available.")
        print()
    
    def process_choice(self, choice_index: int) -> bool:
        """
        Process a player choice.
        
        Returns True if action was successful, False otherwise.
        """
        node_id = self.player.current_node
        node, choices = self.node_engine.get_available_choices(
            self.player.stats,
            self.player.flags,
            self.player.inventory,
            node_id
        )
        
        if choice_index < 1 or choice_index > len(choices):
            print("Invalid choice.")
            return False
        
        # Convert to 0-indexed
        actual_index = choices[choice_index - 1]["_index"]
        
        result = self.node_engine.process_choice(
            self.player.stats,
            self.player.flags,
            self.player.inventory,
            node_id,
            actual_index
        )
        
        if result.success:
            if result.next_node:
                self.player.move_to_node(result.next_node)
            print(f"\n> {result.message}")
            return True
        else:
            print(f"Error: {result.message}")
            return False
    
    def use_consumable(self, item_name: str) -> bool:
        """
        Use a consumable item.
        
        Returns True if successful, False otherwise.
        """
        if not self.player.has_item(item_name):
            print(f"You don't have {item_name}.")
            return False
        
        # Find the item
        item = None
        for inv_item in self.player.inventory:
            if inv_item.get("name") == item_name:
                item = inv_item
                break
        
        if not item:
            return False
        
        # Check if it's a consumable
        if item.get("type") != "consumable":
            print(f"{item_name} is not consumable.")
            return False
        
        # Apply effects
        effects = item.get("effect", {})
        if "hp" in effects:
            self.rules_engine.heal(self.player.stats, effects["hp"])
            print(f"Used {item_name}! Healed for {effects['hp']} HP.")
        if "mp" in effects:
            self.rules_engine.restore_mana(self.player.stats, effects["mp"])
            print(f"Mana restored by {effects['mp']}.")
        for stat in ["strength", "defence", "agility", "vitality", "wisdom", "perception"]:
            if stat in effects:
                self.player.add_stat(stat, effects[stat])
                print(f"{stat.capitalize()} increased by {effects[stat]}!")
        
        # Remove item
        self.player.remove_item(item_name)
        return True
    
    def allocate_stat_point(self, stat_name: str) -> bool:
        """
        Allocate a free stat point.
        
        Returns True if successful, False otherwise.
        """
        if self.rules_engine.allocate_stat_point(self.player.stats, stat_name):
            print(f"Allocated stat point to {stat_name}!")
            return True
        else:
            print(f"Cannot allocate point to {stat_name}. Invalid stat or no free points.")
            return False
    
    def handle_command(self, command: str) -> None:
        """
        Handle player commands.
        
        Commands:
            stats - display current stats
            inventory - display inventory
            levelup - allocate stat point
            use <item> - consume item
            choose <n> - make a choice
            move <node> - move to node (debug)
            save - save game
            exit - save and quit
        """
        parts = command.strip().lower().split(maxsplit=1)
        if not parts:
            return
        
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""
        
        if cmd == "stats":
            self.display_stats()
        
        elif cmd == "inventory":
            self.display_inventory()
        
        elif cmd == "levelup":
            if self.player.stats["free_stat_points"] <= 0:
                print("No free stat points available.")
                return
            print("\nAvailable stats to allocate:")
            stats = ["hp", "mp", "strength", "defence", "agility", "vitality", "wisdom", "perception"]
            for i, stat in enumerate(stats, 1):
                print(f"{i}. {stat}")
            try:
                choice = int(input("Choose stat (1-8): "))
                if 1 <= choice <= len(stats):
                    self.allocate_stat_point(stats[choice - 1])
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
        
        elif cmd == "use":
            if not arg:
                print("Usage: use <item_name>")
                return
            self.use_consumable(arg)
        
        elif cmd == "choose":
            try:
                choice_num = int(arg)
                self.process_choice(choice_num)
            except ValueError:
                print("Usage: choose <number>")
        
        elif cmd == "move":
            if not arg:
                print("Usage: move <node_id>")
                return
            self.player.move_to_node(arg)
            print(f"Moved to {arg}")
        
        elif cmd == "save":
            self.save_game()
            print("Game saved.")
        
        elif cmd == "exit":
            self.save_game()
            print("Game saved. Goodbye!")
            self.running = False
        
        else:
            print("Unknown command. Try: stats, inventory, levelup, use, choose, move, save, exit")
    
    def run(self) -> None:
        """Run the main game loop."""
        print(f"\nWelcome to {self.state_manager.get_setting('game', 'title')}!")
        print(f"v{self.state_manager.get_setting('game', 'version')}")
        print("Type 'help' for commands or just type a choice number.\n")
        
        while self.running:
            # Check if player is alive
            if not self.rules_engine.is_alive(self.player.stats):
                print("\nYou have died. Game Over.")
                self.game_over = True
                self.running = False
                break
            
            # Display current node
            self.display_node()
            
            # Get player input
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            # Try to parse as choice number first
            try:
                choice_num = int(user_input)
                self.process_choice(choice_num)
                continue
            except ValueError:
                pass
            
            # Handle as command
            self.handle_command(user_input)
        
        self.save_game()
