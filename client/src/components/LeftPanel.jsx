import React from 'react';
import { motion } from 'framer-motion';

export default function LeftPanel({ player }) {
  const hp = player?.stats?.hp || 0;
  const hpMax = 50 + ((player?.stats?.vitality || 5) - 5) * 5;
  const mp = player?.stats?.mp || 0;
  const mpMax = 25 + ((player?.stats?.wisdom || 5) - 5) * 5;
  
  return (
    <div className="w-80 flex flex-col gap-6 p-4 border-r border-dark-border/50 bg-dark-bg/80 backdrop-blur-sm">
      
      {/* Level / Status Block */}
      <div className="space-y-4">
         <h2 className="text-3xl font-light text-white tracking-widest">
           LEVEL: <span className="text-goblin-400 font-bold">{player?.stats?.level || 1}</span>
         </h2>
         
         {/* HP Bar */}
         <div className="space-y-1">
           <div className="flex justify-between text-xs text-red-200/70 tracking-wider">
             <span>HEALTH</span>
             <span>{hp}/{hpMax}</span>
           </div>
           <div className="h-4 bg-dark-card border border-dark-border/30 skew-x-[-10deg]">
             <motion.div 
               className="h-full bg-gradient-to-r from-red-900 to-red-600"
               initial={{ width: 0 }}
               animate={{ width: `${(hp/hpMax)*100}%` }}
             />
           </div>
         </div>

         {/* MP Bar */}
         <div className="space-y-1">
           <div className="flex justify-between text-xs text-blue-200/70 tracking-wider">
             <span>MANA</span>
             <span>{mp}/{mpMax}</span>
           </div>
            <div className="h-2 bg-dark-card border border-dark-border/30 skew-x-[-10deg] mt-2">
             <motion.div 
               className="h-full bg-gradient-to-r from-blue-900 to-blue-600"
               initial={{ width: 0 }}
               animate={{ width: `${(mp/mpMax)*100}%` }}
             />
           </div>
         </div>
         
          <div className="flex justify-between text-[10px] text-gray-500 mt-1 uppercase tracking-widest">
            <span>XP: {player?.stats?.experience || 0}</span>
          </div>

      </div>

      <div className="h-px bg-gradient-to-r from-transparent via-goblin-500/20 to-transparent my-2" />

      {/* Quest Items / Important Flags */}
      <div className="flex-1 space-y-4">
        <h3 className="text-goblin-500 text-xs font-bold uppercase tracking-[0.2em] border-b border-white/5 pb-2">
           Quest Items
        </h3>
        {/* We filter inventory for key items later, currently showing placeholder or filtered list */}
        <div className="space-y-2">
          {player?.inventory?.filter(i => i.type === 'key_item' || i.type === 'weapon').map((item, idx) => (
             <div key={idx} className="bg-dark-card/40 p-3 border border-dark-border/50 flex items-center justify-between group hover:border-goblin-500/30 transition-colors cursor-default">
                <span className="text-gray-300 text-sm font-medium">{item.name}</span>
                <div className="w-2 h-2 rounded-full bg-goblin-500/0 group-hover:bg-goblin-500 transition-colors shadow-[0_0_10px_rgba(180,211,69,0.5)]" />
             </div>
          ))}
          {(!player?.inventory || player?.inventory.length === 0) && (
            <div className="text-gray-600 text-xs italic">No quest items...</div>
          )}
        </div>
      </div>

       <div className="p-4 bg-dark-card/30 border border-red-900/20 rounded text-xs text-red-500/60 font-mono text-center">
         <span className="block mb-1">⚠️ STATUS</span>
         Requires Strength 15
       </div>

    </div>
  );
}
