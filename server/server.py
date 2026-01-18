import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path logic similar to main.py
sys.path.insert(0, str(Path(__file__).parent))

from engine.state_manager import StateManager
from engine.rules import RulesEngine
from engine.node_engine import NodeEngine
from engine.combat_engine import CombatEngine, CombatAction, Enemy

app = FastAPI(title="Minima RPG API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Global Game State (In-Memory for single player demo) ---
# In a real multi-user app, this would be per-session/database backed.
class GameSession:
    def __init__(self):
        self.settings_path = Path(__file__).parent / "config" / "settings.json"
        
        # Initialize Managers
        self.state_manager = StateManager(str(self.settings_path))
        self.rules_engine = RulesEngine(self.state_manager.settings)
        self.node_engine = NodeEngine(self.state_manager.load_nodes(), self.rules_engine)
        self.node_engine = NodeEngine(self.state_manager.load_nodes(), self.rules_engine)
        self.combat_engine = CombatEngine(self.rules_engine, data_dir=str(Path(__file__).parent / "data"))
        
        # Load Player State
        self.player_state = self.state_manager.load_player_state()
        
        # Combat State
        self.current_combat = None
        
        # Verify current node exists, else reset to start
        current_node_id = self.player_state.get("current_node")
        if not self.node_engine.get_node(current_node_id):
            # Fallback for fresh save
            self.player_state["current_node"] = "intro_01" 
            self.state_manager.save_player_state(self.player_state)

    def save(self):
        self.state_manager.save_player_state(self.player_state)

    def get_current_node_data(self):
        node_id = self.player_state.get("current_node")
        node_data = self.node_engine.get_node(node_id)
        if not node_data:
            return None
        
        # Get available choices based on current stats/flags
        # We need to manually construct the choice list compatible with frontend
        _, choices = self.node_engine.get_available_choices(
            self.player_state["stats"],
            self.player_state["flags"],
            self.player_state["inventory"],
            node_id
        )
        
        return {
            "node_id": node_id,
            "text": node_data.get("text", ""),
            "choices": choices,
            # Phase 2: Add combat info here if node type is combat
        }

# Global instance
session = GameSession()

# --- Pydantic Models for Requests ---

class ChoiceRequest(BaseModel):
    choice_index: int

class ResetRequest(BaseModel):
    confirm: bool

class LogRequest(BaseModel):
    level: str
    message: str
    timestamp: str

# --- Endpoints ---

@app.post("/log")
def log_client_message(request: LogRequest):
    """Log a message from the client."""
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "client.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{request.timestamp}] [{request.level.upper()}] {request.message}\n")
    
    return {"status": "ok"}

class AllocateRequest(BaseModel):
    stat_name: str

class CombatActionRequest(BaseModel):
    action: str  # "attack", "defend", "flee"

@app.post("/allocate")
def allocate_stat(request: AllocateRequest):
    """Allocate a free stat point."""
    success = session.rules_engine.allocate_stat_point(
        session.player_state["stats"], 
        request.stat_name
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Cannot allocate point (insufficient points or invalid stat)")
        
    session.save()
    return get_game_state()

    session.save()
    return get_game_state()

class EquipRequest(BaseModel):
    item_index: int

@app.post("/equip")
def equip_item(request: EquipRequest):
    """Equip an item from inventory."""
    inventory = session.player_state["inventory"]
    
    if request.item_index < 0 or request.item_index >= len(inventory):
        raise HTTPException(status_code=400, detail="Invalid item index")
        
    item = inventory[request.item_index]
    item_type = item.get("type") # "weapon", "armor", "accessory"
    
    if item_type not in ["weapon", "armor", "accessory"]:
         raise HTTPException(status_code=400, detail="Item is not equipable")
         
    # Logic: Validate slot, swap if needed
    equipment = session.player_state.get("equipment", {})
    if not equipment:
        session.player_state["equipment"] = {"weapon": None, "armor": None, "accessory": None}
        equipment = session.player_state["equipment"]
        
    current_equipped = equipment.get(item_type)
    
    # Remove new item from inventory
    inventory.pop(request.item_index)
    
    # If something was equipped, add it back to inventory
    if current_equipped:
        inventory.append(current_equipped)
        
    # Equip new item
    equipment[item_type] = item
    
    session.save()
    return get_game_state()

@app.post("/combat/action")
def combat_action(request: CombatActionRequest):
    """Process a combat action."""
    if not session.current_combat or not session.current_combat.is_active:
        raise HTTPException(status_code=400, detail="No active combat")
    
    # Map string to enum
    try:
        action_enum = CombatAction(request.action.lower())
    except ValueError:
         raise HTTPException(status_code=400, detail="Invalid action")

    result = session.combat_engine.process_turn(
        session.current_combat,
        session.player_state["stats"],
        session.player_state["inventory"],
        action_enum,
        session.player_state.get("equipment")
    )
    
    # If combat ended
    if not session.current_combat.is_active:
        if session.current_combat.victory:
            # Maybe move to next node? For now just stay but clear combat
            pass
        else:
            # Player died - redirect to death node
            session.player_state["current_node"] = "death"
            
    session.save()
    return get_game_state()

@app.post("/debug/combat")
def debug_start_combat():
    """Start a debug combat encounter."""
    enemy = Enemy("Shadow Stalker", hp=40, attack_power=8, defence=3, exp_reward=50)
    session.current_combat = session.combat_engine.initialize_combat(enemy)
    return get_game_state()

@app.get("/state")
def get_game_state():
    """Returns the full display state for the UI."""
    node_data = session.get_current_node_data()
    
    # Determine mode
    mode = "STORY"
    combat_data = None
    
    if session.current_combat and session.current_combat.is_active:
        mode = "COMBAT"
        combat_data = {
            "enemy": {
                "name": session.current_combat.enemy.name,
                "hp": session.current_combat.enemy.hp,
                "max_hp": session.current_combat.enemy.max_hp
            },
            "log": session.current_combat.log[-7:] # Tail log
        }
    
    return {
        "mode": mode,
        "player": {
            "stats": session.player_state["stats"],
            "inventory": session.player_state["inventory"],
            "flags": session.player_state["flags"]
        },
        "narrative": node_data,
        "combat": combat_data
    }

@app.post("/choice")
def make_choice(request: ChoiceRequest):
    """Process a player's choice."""
    current_node_id = session.player_state["current_node"]
    
    # Process using existing engine logic
    result = session.node_engine.process_choice(
        session.player_state["stats"],
        session.player_state["flags"],
        session.player_state["inventory"],
        current_node_id,
        request.choice_index
    )
    
    if not result.success:
        raise HTTPException(status_code=400, detail=result.message)
    
    # Update current node if changed
    if result.next_node:
        session.player_state["current_node"] = result.next_node
        
    # Check for combat trigger
    if "combat" in result.effects:
        combat_trigger = result.effects["combat"]
        # If string (enemy ID) or int (difficulty) can be handled,
        # for now let's assume it's an enemy ID or "random"
        if combat_trigger == "random":
             enemy = session.combat_engine.get_random_enemy(difficulty=1)
        else:
             # Find enemy by ID, else random
             enemy_data = next((e for e in session.combat_engine.enemies if e["id"] == combat_trigger), None)
             if enemy_data:
                 enemy = Enemy(
                    name=enemy_data["name"],
                    hp=enemy_data["hp"],
                    attack_power=enemy_data["attack_power"],
                    defence=enemy_data["defence"],
                    exp_reward=enemy_data["exp_reward"],
                    loot=enemy_data.get("loot_table", [])
                 )
             else:
                 enemy = session.combat_engine.get_random_enemy(difficulty=1)
        
        session.current_combat = session.combat_engine.initialize_combat(enemy)
        
    session.save()
    
    return {
        "success": True,
        "message": result.message,
        "effects": result.effects,
        "next_node": result.next_node,
        "new_state": get_game_state()
    }

@app.post("/debug/combat")
def debug_start_combat():
    """Start a debug combat encounter."""
    # Use random level 3 enemy
    enemy = session.combat_engine.get_random_enemy(difficulty=3)
    session.current_combat = session.combat_engine.initialize_combat(enemy)
    return get_game_state()

@app.post("/reset")
def reset_game(request: ResetRequest):
    """Resets the game to initial state - useful for debugging."""
    if not request.confirm:
         raise HTTPException(status_code=400, detail="Must confirm reset")
         
    # Reload from template by deleting current state and reloading
    if session.state_manager.player_state_path.exists():
        session.state_manager.player_state_path.unlink()
        
    session.player_state = session.state_manager.load_player_state()
    session.save()
    
    return get_game_state()

if __name__ == "__main__":
    import uvicorn
    print("Starting Minima RPG Backend on http://localhost:8080")
    uvicorn.run(app, host="0.0.0.0", port=8080)
