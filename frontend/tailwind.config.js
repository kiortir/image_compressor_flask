module.exports = {
  content: [
    "../backend/web_compressor/web/templates/index.j2",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Gilroy',],
      },
      colors: {
        unirock: '#ff1c2e',
        unirock_dark: '#323338',
        primary: '#409eff',
        'light-blue': '#9cc0fa'
      }
    },
  },
  plugins: [],
}
