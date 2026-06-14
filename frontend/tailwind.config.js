/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue"
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#080C14',
          surface: '#0F1923',
          card: '#131D2B',
          elevated: '#1A2535',
          border: '#1E2D42',
          text: '#F0F4FF',
          muted: '#6B7A99'
        },
        light: {
          bg: '#F0F4FF',
          surface: '#FFFFFF',
          card: '#FFFFFF',
          elevated: '#F8FAFF',
          border: '#E2E8F4',
          text: '#0A1628',
          muted: '#4A5568'
        },
        primary: '#3B82F6',
        success: '#10B981',
        danger: '#F43F5E',
        warning: '#F59E0B',
        purple: '#8B5CF6'
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
