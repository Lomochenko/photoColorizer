<template>
  <div>
    <ImageColorizer />
  </div>
</template>

<script setup lang="ts">
// Head metadata
useHead({
  title: 'AI Photo Colorizer - Transform B&W Photos into Color',
  meta: [
    { 
      name: 'description', 
      content: 'Transform your black and white photos into vibrant, colorized images using advanced AI technology. Fast, easy, and free.' 
    },
    { 
      name: 'keywords', 
      content: 'photo colorization, AI image processing, black and white photos, colorize photos, image enhancement, DeOldify' 
    },
    {
      property: 'og:title',
      content: 'AI Photo Colorizer'
    },
    {
      property: 'og:description',
      content: 'Transform black & white photos into color using AI'
    },
    {
      property: 'og:type',
      content: 'website'
    }
  ],
  link: [
    {
      rel: 'icon',
      type: 'image/png',
      href: '/favicon.png'
    }
  ]
})
</script>
