# Echo Chronicles (formerly Minima RPG)

**A Stats-Driven Narrative RPG with a Modern Web Interface.**

Echo Chronicles is a choice-driven, diverging-path RPG where your stats (Strength, Wisdom, Perception, etc.) determine your story. Originally a terminal-only game, it has evolved into a full-stack web application featuring a rich narrative, interactive combat, and atmospheric "Dark Glassmorphism" UI.

## 🌟 Current Phase: Phase 2.5 (World Expansion)
The game has successfully transitioned from a text adventure to a graphical web RPG.

### Features
*   **Web Interface**: React + Vite frontend with TailwindCSS.
*   **Backend API**: Python FastAPI server managing game state and logic.
*   **Interactive Combat**: Turn-based battles with visual HP bars, combat logs, and inventory integration.
*   **World Expansion**: Multi-zone system (Manor, Garden, Village) with distinct themes.
*   **Perception System**: "Sanity" mechanics that reveal hidden truths/glitches in the world based on stats.
*   **Equipment**: Weapon and armor slots that directly affect combat stats.

## 🚀 Quick Start

You need **two** terminals running simultaneously (one for logic, one for UI).

### 1. Start the Backend (Game Engine)
This runs the Python server on port `8080`.
```powershell
# In the root directory
# (Create venv if you haven't: python -m venv .venv)
.venv\Scripts\activate
pip install -r server/requirements_web.txt
python server/server.py
```

### 2. Start the Frontend (Web UI)
This runs the React client on port `5173`.
```powershell
# Open a NEW terminal
cd client
npm install
npm run dev
```

**Play the game at:** `http://localhost:5173`

## 🛠️ Modding & Development

### Architecture
*   **`server/`**: The brain. Contains `CombatEngine`, `NodeEngine`, and JSON data.
*   **`client/`**: The face. React components in `src/components`.

### Editing Content
The game is data-driven. You can expand the world without writing code.

*   **Story Nodes**: `server/data/nodes/*.json` (Add new files here!)
*   **Items**: `server/data/items.json`
*   **Enemies**: `server/data/enemies.json`

### Creating a New Zone
1.  Create `server/data/nodes/zone_myzone.json`.
2.  Add nodes in the standard JSON format.
3.  Link to it from an existing node using `"next": "myzone_entry_node"`.
4.  (Optional) Add `restart_server` to load the new file.

## 🤝 Hosting / Sharing
To let friends play your local version, use `ngrok`.
See `hosting_guide.md` (Artifact) or `minima_ngrok.yml` for configuration.

## 📜 License
MIT License.
