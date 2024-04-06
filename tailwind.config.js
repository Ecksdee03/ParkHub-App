/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html', // Include HTML files in the 'templates' directory and its subdirectories
    './components/**/*.html', // Include HTML files in the 'components' directory and its subdirectories
    './src/**/*.html', // Include JavaScript files in the 'src' directory and its subdirectories
    './static/**/*.js', // Include JavaScript files in the 'static' directory and its subdirectories
    './cdn/**/*.html', // Include JavaScript files in the 'cdn' directory and its subdirectories
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

