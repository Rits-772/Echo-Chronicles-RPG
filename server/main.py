"""
XP Minima RPG - Main Entry Point

Terminal-first, stats-driven narrative RPG.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from engine.state_manager import StateManager
from engine.game_loop import GameLoop


def main():
    """Main entry point."""
    try:
        # Initialize state manager with settings
        settings_path = Path(__file__).parent / "config" / "settings.json"
        state_manager = StateManager(str(settings_path))
        
        # Create and run game loop
        game = GameLoop(state_manager)
        game.run()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure config/settings.json and data files exist.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
