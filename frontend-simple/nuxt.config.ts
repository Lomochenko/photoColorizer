export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@nuxtjs/tailwindcss',
  ],

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

  tailwindcss: {
    viewer: false
  }
})
