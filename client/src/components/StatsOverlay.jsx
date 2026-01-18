import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Shield, Backpack, ChevronUp, ChevronDown, Activity, Zap } from 'lucide-react';

export default function StatsOverlay({ stats, inventory }) {
  const [isOpen, setIsOpen] = useState(false);

  // Core stats to always show
  const hp = stats?.hp || 0;
  const mp = stats?.mp || 0;
  const hpMax = 50 + ((stats?.vitality || 5) - 5) * 5;
  const mpMax = 25 + ((stats?.wisdom || 5) - 5) * 5;

  return (
    <>
      {/* Top Bar - Minimal */}
      <div className="fixed top-0 left-0 right-0 bg-dark-bg/90 backdrop-blur-sm border-b border-dark-border p-3 z-50 flex justify-between items-center px-4 md:px-8">
        <div className="flex items-center gap-6 font-mono text-sm">
          {/* Simple Bars */}
          <div className="flex items-center gap-3">
            <Activity size={16} className="text-red-400" />
            <div className="flex flex-col gap-0.5 w-32">
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-red-500 transition-all duration-500" 
                  style={{ width: `${Math.min(100, (hp / hpMax) * 100)}%` }}
                />
              </div>
            </div>
            <span className="text-gray-400 text-xs hidden sm:block">{hp}/{hpMax}</span>
          </div>

          <div className="flex items-center gap-3">
            <Zap size={16} className="text-blue-400" />
            <div className="flex flex-col gap-0.5 w-32">
              <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-blue-500 transition-all duration-500" 
                  style={{ width: `${Math.min(100, (mp / mpMax) * 100)}%` }} 
                />
              </div>
            </div>
            <span className="text-gray-400 text-xs hidden sm:block">{mp}/{mpMax}</span>
          </div>
        </div>

        <button 
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-sm uppercase tracking-wider font-semibold"
        >
          {isOpen ? 'Close Menu' : 'Character'}
          {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </button>
      </div>

      {/* Expanded Drawer */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ y: '-100%' }}
            animate={{ y: '60px' }} // Below top bar
            exit={{ y: '-100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed top-0 left-0 right-0 bg-dark-surface/95 backdrop-blur-xl border-b border-goblin-500/20 z-40 shadow-2xl overflow-hidden"
          >
            <div className="max-w-4xl mx-auto p-8 grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
              
              {/* Stats Column */}
              <div>
                <h3 className="flex items-center gap-2 text-goblin-400 font-bold mb-4 uppercase tracking-wider text-sm">
                  <Shield size={18} /> Attributes
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  {Object.entries(stats || {}).map(([key, value]) => {
                    if (['hp', 'mp', 'experience', 'level', 'free_stat_points'].includes(key)) return null;
                    return (
                      <div key={key} className="flex justify-between items-center bg-dark-bg/50 p-2 rounded border border-dark-border">
                        <span className="text-gray-400 capitalize text-sm">{key}</span>
                        <span className="text-white font-mono font-bold text-lg">{value}</span>
                      </div>
                    );
                  })}
                </div>
                
                <div className="mt-6 flex gap-4">
                  <div className="bg-dark-bg/50 p-3 rounded border border-dark-border flex-1">
                    <span className="block text-gray-500 text-xs uppercase">Level</span>
                    <span className="text-2xl font-bold text-white">{stats?.level || 1}</span>
                  </div>
                  <div className="bg-dark-bg/50 p-3 rounded border border-dark-border flex-1">
                    <span className="block text-gray-500 text-xs uppercase">XP</span>
                    <span className="text-xl font-bold text-gray-300">{stats?.experience || 0}</span>
                  </div>
                </div>
              </div>

              {/* Inventory Column */}
              <div>
                <h3 className="flex items-center gap-2 text-yellow-400 font-bold mb-4 uppercase tracking-wider text-sm">
                  <Backpack size={18} /> Inventory
                </h3>
                {inventory && inventory.length > 0 ? (
                  <ul className="space-y-2 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                    {inventory.map((item, i) => (
                      <li key={i} className="flex justify-between items-center bg-dark-bg/30 p-3 rounded hover:bg-dark-bg/50 transition-colors border border-transparent hover:border-dark-border">
                        <span className="text-gray-200">{item.name}</span>
                        <span className="text-xs text-gray-500 bg-dark-bg px-2 py-1 rounded-full">{item.type}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <div className="text-gray-600 italic p-4 border border-dashed border-dark-border rounded text-center">
                    Your bag is empty...
                  </div>
                )}
              </div>

            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
