/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                serif: ['"Playfair Display"', 'serif'],
            },
            colors: {
                background: "#050505",
                foreground: "#ffffff",
                primary: {
                    DEFAULT: "#ffffff",
                    foreground: "#000000",
                },
                accent: {
                    DEFAULT: "#d4af37", // Gold
                    foreground: "#000000",
                },
                muted: {
                    DEFAULT: "#1a1a1a",
                    foreground: "#a1a1aa",
                },
            },
            animation: {
                marquee: 'marquee 25s linear infinite',
            },
            keyframes: {
                marquee: {
                    '0%': { transform: 'translateX(0%)' },
                    '100%': { transform: 'translateX(-100%)' },
                },
            },
        },
    },
    plugins: [],
}
