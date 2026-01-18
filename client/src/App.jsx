import React, { useState, useEffect } from 'react';
import GameLayout from './components/GameLayout';
import LeftPanel from './components/LeftPanel';
import CenterPanel from './components/CenterPanel';
import RightPanel from './components/RightPanel';
import { fetchGameState, makeChoice, allocateStat, resetGame, sendCombatAction, debugStartCombat, equipItem } from './services/api.js';

function App() {
  const [gameState, setGameState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initial load
  useEffect(() => {
    loadGame();
  }, []);

  const loadGame = async () => {
    try {
      setLoading(true);
      const data = await fetchGameState();
      setGameState(data);
    } catch (err) {
      console.error(err);
      setError("Failed to connect to the game server. Is it running?");
    } finally {
      setLoading(false);
    }
  };

  const handleChoice = async (choiceIndex) => {
    try {
      const result = await makeChoice(choiceIndex);
      setGameState(result.new_state);
    } catch (err) {
      console.error(err);
    }
  };

  const handleAllocate = async (statName) => {
    try {
      const newState = await allocateStat(statName);
      setGameState(newState);
    } catch (err) {
      console.error(err);
    }
  };

  const handleReset = async () => {
    if(!confirm("Are you sure you want to restart? Progress will be lost.")) return;
    try {
      const newState = await resetGame();
      setGameState(newState);
    } catch (err) {
      console.error(err);
    }
  };

  const handleCombatAction = async (action) => {
    try {
      const newState = await sendCombatAction(action);
      setGameState(newState);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDebugCombat = async () => {
    try {
      const newState = await debugStartCombat();
      if (newState) setGameState(newState);
    } catch (err) {
      console.error(err);
    }
  };

  const handleEquip = async (itemIndex) => {
    try {
      const newState = await equipItem(itemIndex);
      setGameState(newState);
    } catch (err) {
      console.error(err);
    }
  };

  if (loading && !gameState) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center text-goblin-500 font-mono animate-pulse">
        Initializing Neural Link...
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center text-red-500 font-mono gap-4 p-4 text-center">
        <p className="text-xl">CONNECTION ERROR</p>
        <p className="text-gray-500 text-sm">{error}</p>
        <button onClick={loadGame} className="px-4 py-2 border border-red-500/50 hover:bg-red-500/10 rounded">
          RETRY CONNECTION
        </button>
      </div>
    );
  }

  return (
    <GameLayout>
      {/* Top Header Bar */}
      <div className="fixed top-0 left-0 right-0 h-16 bg-dark-bg border-b border-dark-border z-50 flex justify-between items-center px-8">
         <h1 className="text-goblin-500 font-serif tracking-[0.2em] text-lg uppercase">Chronicles Of The Echoes</h1>
         <div className="flex gap-6 text-xs text-gray-400 font-bold tracking-widest">
            <span className="hover:text-white cursor-pointer flex items-center gap-2"><div className="w-4 h-4 border border-gray-600 rounded-full" /> STATS</span>
            <button onClick={handleReset} className="hover:text-red-400 cursor-pointer flex items-center gap-2 transition-colors">
              <div className="w-4 h-4 border border-red-900/50 rounded bg-red-900/20" /> RESET
            </button>
         </div>
      </div>

      {/* Main 3-Column Grid */}
      <div className="flex h-screen pt-16 overflow-hidden">
         {/* Left Sidebar */}
         <LeftPanel player={gameState?.player} />

         {/* Center Content */}
         <CenterPanel 
            narrative={gameState?.narrative}
            mode={gameState?.mode}
            combat={gameState?.combat}
            onChoice={handleChoice}
            onCombatAction={handleCombatAction}
            onDebugCombat={handleDebugCombat}
         />

         {/* Right Sidebar */}
         <RightPanel 
            player={gameState?.player} 
            onAllocate={handleAllocate}
            onEquip={handleEquip}
         />
      </div>

    </GameLayout>
  );
}

export default App;
