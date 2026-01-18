import React from 'react';

export default function RightPanel({ player, onAllocate, onEquip }) {
  const stats = player?.stats || {};
  const inventory = player?.inventory || [];
  const equipment = player?.equipment || { weapon: null, armor: null, accessory: null };
  const freePoints = stats.free_stat_points || 0;
  
  const displayStats = [
    { label: 'STRENGTH', key: 'strength', val: stats.strength },
    { label: 'DEFENCE', key: 'defence', val: stats.defence },
    { label: 'AGILITY', key: 'agility', val: stats.agility },
    { label: 'WISDOM', key: 'wisdom', val: stats.wisdom },
    { label: 'VITALITY', key: 'vitality', val: stats.vitality },
    { label: 'PERCEPTION', key: 'perception', val: stats.perception },
  ];

  return (
    <div className="w-80 flex flex-col gap-6 p-4 border-l border-dark-border/50 bg-dark-bg/80 backdrop-blur-sm shadow-xl z-20 overflow-y-auto">
      
      {/* Stats List */}
      <div>
        <h3 className="text-gray-400 text-xs font-bold uppercase tracking-[0.2em] border-b border-white/5 pb-4 mb-4 text-center flex justify-between items-center px-2">
           <span>Attributes</span>
           {freePoints > 0 && <span className="text-goblin-400 animate-pulse">+{freePoints} PTS</span>}
        </h3>
        <div className="space-y-3">
          {displayStats.map((s, i) => (
            <div key={i} className="flex justify-between items-center text-sm group hover:bg-white/5 p-1 rounded transition-colors px-2">
               <span className="text-gray-400 font-light tracking-wide group-hover:text-gray-200">{s.label}</span>
               <div className="flex items-center gap-3">
                 <span className="text-goblin-400 font-mono font-bold text-lg">{s.val || 0}</span>
                 {freePoints > 0 && (
                   <button 
                     onClick={() => onAllocate(s.key)}
                     className="w-5 h-5 flex items-center justify-center bg-goblin-500/20 hover:bg-goblin-500 text-goblin-400 hover:text-black rounded text-xs transition-all border border-goblin-500/50"
                   >
                     +
                   </button>
                 )}
               </div>
            </div>
          ))}
        </div>
      </div>

      {/* Equipment Slots */}
      <div>
         <h3 className="text-gray-400 text-xs font-bold uppercase tracking-[0.2em] border-b border-white/5 pb-2 mb-4">Equipment</h3>
         <div className="space-y-2">
            {['Weapon', 'Armor', 'Accessory'].map((slot) => {
                const item = equipment[slot.toLowerCase()];
                return (
                    <div key={slot} className="flex items-center gap-3 p-2 bg-dark-card/30 border border-white/5 rounded">
                        <div className="w-8 h-8 bg-black/50 border border-white/10 rounded flex items-center justify-center text-[10px] text-gray-600 uppercase">
                          {slot[0]}
                        </div>
                        <div className="flex-1">
                            <div className="text-xs text-gray-500 uppercase tracking-wider">{slot}</div>
                            <div className={`text-sm ${item ? 'text-goblin-300' : 'text-gray-600 italic'}`}>
                                {item ? item.name : 'Empty'}
                            </div>
                        </div>
                    </div>
                );
            })}
         </div>
      </div>

      {/* Inventory */}
      <div className="flex-1">
        <h3 className="text-gray-400 text-xs font-bold uppercase tracking-[0.2em] border-b border-white/5 pb-2 mb-4">
           Inventory
        </h3>
        <div className="space-y-2">
          {inventory.map((item, idx) => (
             <div key={idx} className="bg-dark-card/40 p-3 border border-dark-border/50 flex flex-col gap-2 group hover:border-goblin-500/30 transition-colors">
                <div className="flex justify-between items-center">
                    <span className="text-gray-300 text-sm font-medium">{item.name}</span>
                    <span className="text-[10px] text-gray-500 uppercase bg-black/40 px-1 rounded">{item.type}</span>
                </div>
                {/* Equip Action */}
                {['weapon', 'armor', 'accessory'].includes(item.type) && (
                    <button 
                        onClick={() => onEquip(idx)}
                        className="text-xs w-full py-1 bg-goblin-500/10 text-goblin-400 border border-goblin-500/20 hover:bg-goblin-500 hover:text-black transition-colors uppercase tracking-wider font-bold"
                    >
                        Equip
                    </button>
                )}
             </div>
          ))}
          {inventory.length === 0 && (
            <div className="text-gray-600 text-xs italic text-center py-4">Sack is empty...</div>
          )}
        </div>
      </div>

    </div>
  );
}
