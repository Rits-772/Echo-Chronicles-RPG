import React from 'react';
import { motion } from 'framer-motion';

export default function CenterPanel({ narrative, onChoice, mode, combat, onCombatAction, onDebugCombat }) {
  const isCombat = mode === 'COMBAT';
  
  // Use real data if available, else defaults
  const enemy = combat?.enemy || { name: 'Unknown', hp: 0, max_hp: 100 };
  const combatLog = combat?.log || [];

  return (
    <div className="flex-1 flex flex-col gap-4 p-4 min-w-[300px] max-w-5xl mx-auto w-full relative">
      
      {/* Top Combat Bar (Conditional) */}
      {isCombat && (
      <div className="bg-dark-card/80 border border-dark-border/50 p-4 rounded-sm flex flex-col gap-2 animate-in fade-in slide-in-from-top-4 duration-500">
        <div className="text-center text-xs text-gray-400 tracking-widest uppercase mb-1 flex justify-between px-4">
           <span>PLAYER</span>
           <span className="text-red-500 font-bold">VS</span>
           <span>{enemy.name}</span>
        </div>
        <div className="flex gap-4 items-center">
           {/* Player HP (Visual only for now, can be passed ref later) */}
           <div className="flex-1 h-3 bg-gray-900 rounded-sm overflow-hidden border border-white/10">
              <div className="h-full bg-red-600 animate-pulse" style={{width: '100%'}} /> 
           </div>
           
           {/* Enemy HP */}
           <div className="flex-1 h-3 bg-gray-900 rounded-sm overflow-hidden border border-white/10 relative">
              <motion.div 
                 className="h-full bg-green-700 absolute left-0 top-0 bottom-0"
                 initial={{ width: '100%' }}
                 animate={{ width: `${(enemy.hp / enemy.max_hp) * 100}%` }}
                 transition={{ duration: 0.3 }}
              />
           </div>
        </div>
        <div className="text-right text-[10px] text-gray-500 font-mono">
            {enemy.hp} / {enemy.max_hp} HP
        </div>
      </div>
      )}

      {/* Main Narrative Area */}
      <div className="flex-1 bg-dark-card/40 border border-dark-border/50 p-8 md:p-12 rounded-sm relative overflow-hidden flex flex-col justify-center min-h-[300px] shadow-2xl">
        {/* Background glow */}
        <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[60%] h-[60%] ${isCombat ? 'bg-red-900/10' : 'bg-goblin-900/5'} blur-[120px] pointer-events-none transition-colors duration-1000`} />
        
        {!isCombat ? (
            <motion.div
            key={narrative?.text}
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, ease: "easeOut" }}
            className="relative z-10"
            >
            <p className="text-gray-200 text-lg md:text-xl leading-loose text-center font-serif tracking-wide drop-shadow-lg">
                {narrative?.text || "..."}
            </p>
            </motion.div>
        ) : (
            <div className="relative z-10 text-center">
                <p className="text-red-400 text-xl font-serif tracking-widest animate-pulse">COMBAT ENGAGED</p>
                <div className="mt-8 flex justify-center gap-4">
                     <button onClick={() => onCombatAction('attack')} className="px-8 py-3 bg-red-900/20 border border-red-500/50 text-red-400 hover:bg-red-500 hover:text-white transition-all rounded uppercase tracking-widest font-bold">
                        ATTACK
                     </button>
                     <button onClick={() => onCombatAction('defend')} className="px-8 py-3 bg-blue-900/20 border border-blue-500/50 text-blue-400 hover:bg-blue-500 hover:text-white transition-all rounded uppercase tracking-widest font-bold">
                        DEFEND
                     </button>
                </div>
            </div>
        )}
        

      </div>

      {/* Choice Area (Story Mode) */}
      {!isCombat && (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
         {narrative?.choices?.length > 0 && narrative.choices.map((choice, i) => (
           <button
             key={i}
             onClick={() => onChoice(choice._index)}
             className="col-span-1 md:col-span-2 text-left p-4 border border-dark-border bg-dark-card/60 hover:bg-goblin-500/10 hover:border-goblin-500/50 transition-all text-base text-gray-300 font-medium group relative overflow-hidden rounded-sm"
           >
             <div className="absolute left-0 top-0 bottom-0 w-1 bg-goblin-500/0 group-hover:bg-goblin-500 transition-colors duration-300" />
             <span className="text-goblin-500 mr-3 opacity-50 font-mono group-hover:opacity-100">{i+1}.</span>
             {choice.label}
           </button>
        ))}
      </div>
      )}

      {/* Combat Log (Conditional) */}
      {isCombat && (
      <div className="h-40 bg-black/60 border border-dark-border/30 p-4 font-mono text-xs text-gray-500 overflow-y-auto custom-scrollbar rounded-sm flex flex-col-reverse">
         <div className="space-y-1 opacity-80">
            {combatLog.map((entry, i) => (
                <p key={i} className="border-b border-white/5 pb-1 mb-1 last:border-0">{entry}</p>
            ))}
         </div>
         <div className="text-gray-600 mb-2 border-b border-white/5 pb-1 uppercase tracking-wider text-[10px] sticky top-0 bg-black/80">COMBAT LOG</div>
      </div>
      )}

    </div>
  );
}
