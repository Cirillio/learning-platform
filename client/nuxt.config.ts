import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: [
    "@nuxt/image",
    "@nuxt/ui",
    "@pinia/nuxt",
    "@nuxtjs/google-fonts",
    "@vueuse/nuxt",
  ],
  vite: { plugins: [tailwindcss()] },
  ui: {
    theme: {
      colors: [
        "primary",
        "secondary",
        "accent",
        "neutral",
        "info",
        "success",
        "warning",
        "error",
      ],
    },
  },
  css: ["./app/assets/css/main.css"],

  googleFonts: {
    families: {
      Mulish: [300, 400, 500, 600, 700, 800, 900],
    },
    display: "swap",
    download: true,
    inject: true,
  },

  devServer: {
    port: 3001,
  },
  // Runtime config для API URL
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000/api",
    },
  },

  routeRules: {
    "/": { ssr: true },
    "/auth/**": { ssr: true },
    "/dashboard/**": { ssr: true },
    "/courses/**": { ssr: true },
  },

  // Настройки SSR
  ssr: true, // Включаем SSR по умолчанию

  // Оптимизация загрузки
  experimental: {
    payloadExtraction: true, // Отключаем для лучшей производительности
  },
});
