/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        goblin: {
          50: '#fcfdf5',
          100: '#f7fae6',
          200: '#edf5cc',
          300: '#deeda3',
          400: '#cbe273',
          500: '#b4d345',
          600: '#8ba629',
          700: '#697e23',
          800: '#546321',
          900: '#465320',
        },
        dark: {
          bg: '#0a0a0a',
          surface: '#121212',
          card: '#1e1e1e',
          border: '#2e2e2e'
        }
      },
      fontFamily: {
        mono: ['"Fira Code"', 'monospace'],
        sans: ['Lato', 'Inter', 'system-ui', 'sans-serif'],
        serif: ['Cinzel', 'serif'],
      }
    },
  },
  plugins: [],
}
