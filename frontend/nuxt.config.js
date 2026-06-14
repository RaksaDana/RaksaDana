export default defineNuxtConfig({
  srcDir: '.',
  compatibilityDate: '2024-04-03',
  devtools: { enabled: false },
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: 'https://chelsy12-raksadana-api.hf.space'
    }
  },
  app: {
    head: {
      title: 'RaksaDana - AI Stock Platform',
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/logo.svg' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap' }
      ]
    }
  },
  vite: {
    optimizeDeps: {
      include: [
        'vue3-apexcharts',
        'gsap',
        '@vueuse/core'
      ]
    }
  }
})
