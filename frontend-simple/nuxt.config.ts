export default defineNuxtConfig({
  compatibilityDate: '2025-12-11',
  devtools: { enabled: true },

  app: {
    head: {
      title: 'Photo Colorizer - AI Powered',
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      meta: [
        { name: 'description', content: 'Transform black & white photos into vibrant colors using AI' }
      ]
    }
  },

  vite: {
    css: {
      postcss: {
        plugins: {
          tailwindcss: {},
          autoprefixer: {},
        },
      },
    },
  },
})
