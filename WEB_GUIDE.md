# Minima RPG - Web Edition

The game has been upgraded with a modern Web UI!

## Prerequisites
- Node.js (v18+)
- Python (v3.10+)

## Quick Start

### 1. Start the Backend Server
This runs the Game Engine API.
```bash
# In the root directory (Minima RPG)
.venv\Scripts\python.exe server\server.py
```
*Server runs at: http://localhost:8080*

### 2. Start the Frontend Client
This launches the Game UI.
```bash
# In the client directory (Minima RPG/client)
npm install  # (Only first time)
npm run dev
```
*Client runs at: http://localhost:5173*

## Features Implemented
- **Modern UI**: Dark glassmorphism aesthetic using React + Tailwind.
- **Improved Typography**: Narrative text is spaced for readability.
- **Dynamic HUD**: Stats are collapsible to reduce clutter.
- **Visual Feedback**: Smooth fade-in animations for new story nodes.
- **Architecture**: Separated Frontend (Client) and Backend (Server) logic.

## Modifying the Game
- **Story**: Edit `server/data/nodes/nodes.json`
- **Stats**: Edit `server/config/settings.json`
- **UI**: Edit files in `client/src/components/`
