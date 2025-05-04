import colors from "tailwindcss/colors";

/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/web/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        // App-level backgrounds
        background: {
          DEFAULT: colors.slate[500], // Main app background
          card: colors.white, // Card background
          cardBackground: colors.gray[100], // Card background
        },
        // Text colors
        text: {
          onBackground: colors.white, // Text on app background
          onCard: colors.slate[800], // Text on card
        },
        // Primary/action colors
        primary: {
          DEFAULT: colors.sky[700], // Main action color
          focus: colors.sky[600], // Focus/hover state
        },
        border: {
          DEFAULT: colors.slate[300], // Main border color
        },
      },
    },
  },
  plugins: [],
};
