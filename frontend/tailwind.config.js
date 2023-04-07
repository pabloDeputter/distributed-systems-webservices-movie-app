// tailwind.config.js
module.exports = {
  purge: [],
  purge: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  darkMode: true, // or 'media' or 'class'
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  daisyui: {
    themes: [
      {
        mytheme: {
          primary: "#7b5af4",

          secondary: "#08ced8",

          accent: "#99c60f",

          neutral: "#292438",

          "base-100": "#2E353D",

          info: "#1F62E0",

          success: "#41D8A8",

          warning: "#EEAB59",

          error: "#E75A68",
        },
      },
    ],
  },
  plugins: [require("daisyui")],
};
