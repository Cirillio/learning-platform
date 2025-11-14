import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@nuxt/image", "@nuxt/ui", "@pinia/nuxt", "@nuxtjs/google-fonts"],
  vite: { plugins: [tailwindcss()] },
  css: ["./app/assets/css/main.css"],

  googleFonts: {
    families: {
      Mulish: [300, 400, 500, 600, 700, 800, 900],
    },
    display: "swap",
    download: true,
    inject: true,
  },

  // Runtime config для API URL
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000/api",
    },
  },

  // Настройки рендеринга страниц
  routeRules: {
    // Главная страница - пререндеринг для лучшего SEO и производительности
    "/": { prerender: true },

    // Страницы аутентификации - SPA режим для лучшей интерактивности форм
    "/auth/**": { ssr: false },

    // Страницы курсов - SSR для динамического контента
    "/courses/**": { ssr: true },

    // Личный кабинет - SPA режим для богатого пользовательского интерфейса
    "/dashboard/**": { ssr: false },

    // API роуты - серверный рендеринг
    "/api/**": { ssr: true },
  },

  // Настройки Nitro для оптимизации
  nitro: {
    // Пререндеринг для статических страниц
    prerender: {
      routes: ["/"],
    },

    // Оптимизация для production
    compressPublicAssets: true,
  },

  // Настройки SSR
  ssr: true, // Включаем SSR по умолчанию

  // Оптимизация загрузки
  experimental: {
    payloadExtraction: false, // Отключаем для лучшей производительности
  },
});
