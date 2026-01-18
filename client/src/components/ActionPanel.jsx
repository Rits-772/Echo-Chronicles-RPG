import React from 'react';
import { motion } from 'framer-motion';

export default function ActionPanel({ choices, onChoose }) {
  if (!choices || choices.length === 0) return null;

  return (
    <div className="max-w-2xl mx-auto space-y-3">
      {choices.map((choice, index) => (
        <motion.button
          key={index}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: index * 0.1 }}
          onClick={() => onChoose(choice._index)} // Note: We use the index added by backend
          className="w-full text-left bg-dark-surface/80 hover:bg-goblin-900/30 border border-dark-border hover:border-goblin-500/50 p-4 rounded-lg transition-all duration-300 group flex items-baseline gap-3 relative overflow-hidden"
        >
          {/* Hover highlight effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-goblin-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
          
          <span className="font-mono text-goblin-400 font-bold min-w-[1.5rem] opacity-70 group-hover:opacity-100">
            {index + 1}.
          </span>
          <span className="text-gray-300 group-hover:text-white font-medium tracking-wide">
            {choice.label}
          </span>
        </motion.button>
      ))}
    </div>
  );
}
