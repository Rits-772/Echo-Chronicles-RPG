import React from 'react';

export default function GameLayout({ children }) {
  return (
    <div className="min-h-screen bg-dark-bg text-gray-100 font-sans selection:bg-goblin-500/30">
      
      {/* Background Ambience */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-900/10 rounded-full blur-3xl opacity-30 animate-pulse" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-goblin-900/10 rounded-full blur-3xl opacity-30 animate-pulse" style={{ animationDelay: '2s' }} />
        
        {/* Scanline/Grid Effect */}
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-[0.03] bg-repeat" />
      </div>

      {/* Main Content Area */}
      <main className="relative z-10 min-h-screen">
        {children}
      </main>
      
    </div>
  );
}
