const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

class LoggerService {
  constructor() {
    this.originalConsoleError = console.error;
    this.originalConsoleLog = console.log;
    
    // Override console methods to capture logs
    console.error = (...args) => {
      this.originalConsoleError(...args);
      this.log('error', args.map(String).join(' '));
    };

    console.log = (...args) => {
      this.originalConsoleLog(...args);
      // Optional: don't send all info logs to avoid spam, or filter them
      // this.log('info', args.map(String).join(' '));
    };
    
    // Global Error Handler
    window.onerror = (message, source, lineno, colno, error) => {
      this.log('fatal', `${message} at ${source}:${lineno}:${colno}`);
    };

    // Unhandled Promise Rejection
    window.onunhandledrejection = (event) => {
      this.log('fatal', `Unhandled Promise Rejection: ${event.reason}`);
    };
  }

  async log(level, message) {
    try {
      if (typeof message !== 'string') {
        message = JSON.stringify(message);
      }
      
      const timestamp = new Date().toISOString();
      
      // Fire and forget - don't await to avoid blocking UI
      fetch(`${API_URL}/log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ level, message, timestamp }),
      }).catch(err => {
        // Fallback to original console if server is unreachable to avoid infinite loop
        this.originalConsoleError('Failed to send log to server:', err);
      });
      
    } catch (e) {
      this.originalConsoleError('Logger internal error:', e);
    }
  }
}

export const logger = new LoggerService();
