import React from 'react';
import { motion } from 'framer-motion';

export default function NarrativePanel({ text }) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-3xl mx-auto mb-8 font-sans"
    >
      <div className="bg-dark-card/60 backdrop-blur-md p-8 rounded-xl border border-dark-border shadow-2xl relative overflow-hidden group">
        
        {/* Decorative corner accents */}
        <div className="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-goblin-500 opacity-30 group-hover:opacity-100 transition-opacity" />
        <div className="absolute top-0 right-0 w-2 h-2 border-t-2 border-r-2 border-goblin-500 opacity-30 group-hover:opacity-100 transition-opacity" />
        <div className="absolute bottom-0 left-0 w-2 h-2 border-b-2 border-l-2 border-goblin-500 opacity-30 group-hover:opacity-100 transition-opacity" />
        <div className="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-goblin-500 opacity-30 group-hover:opacity-100 transition-opacity" />
        
        {/* Main Text with improved breathing room */}
        <p className="text-gray-100 text-lg leading-loose whitespace-pre-wrap tracking-wide font-light">
          {text || "..."}
        </p>
      </div>
    </motion.div>
  );
}
