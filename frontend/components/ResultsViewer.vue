<template>
  <div class="max-w-6xl mx-auto">
    <!-- Header -->
    <div class="text-center mb-8">
      <h1 class="text-4xl font-bold gradient-text mb-4">
        Colorization Complete!
      </h1>
      <p class="text-xl text-dark-300">
        Your black and white photo has been transformed
      </p>
    </div>

    <!-- Results Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Original Image -->
      <div class="glass-morphism p-6">
        <h3 class="text-xl font-semibold text-white mb-4 text-center">
          Original (B&W)
        </h3>
        <div class="image-container aspect-square">
          <img 
            :src="originalImage" 
            alt="Original black and white image"
            class="w-full h-full object-cover rounded-xl"
          />
        </div>
      </div>

      <!-- Colorized Image -->
      <div class="glass-morphism p-6">
        <h3 class="text-xl font-semibold text-white mb-4 text-center">
          Colorized Result
        </h3>
        <div class="image-container aspect-square">
          <img 
            :src="colorizedImage" 
            alt="Colorized image result"
            class="w-full h-full object-cover rounded-xl"
          />
        </div>
      </div>
    </div>

    <!-- Comparison Slider (Mobile) -->
    <div class="lg:hidden glass-morphism p-6 mb-8">
      <h3 class="text-lg font-semibold text-white mb-4 text-center">
        Before & After Comparison
      </h3>
      <div class="relative aspect-square rounded-xl overflow-hidden">
        <img 
          :src="originalImage" 
          alt="Original"
          class="absolute inset-0 w-full h-full object-cover"
        />
        <div 
          class="absolute inset-0 overflow-hidden"
          :style="{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }"
        >
          <img 
            :src="colorizedImage" 
            alt="Colorized"
            class="w-full h-full object-cover"
          />
        </div>
        
        <!-- Slider Control -->
        <div 
          class="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize"
          :style="{ left: `${sliderPosition}%`, transform: 'translateX(-50%)' }"
          @mousedown="startDragging"
          @touchstart="startDragging"
        >
          <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-dark-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l4-4 4 4m0 6l-4 4-4-4"/>
            </svg>
          </div>
        </div>
      </div>
      <p class="text-center text-dark-400 text-sm mt-2">
        Drag the slider to compare
      </p>
    </div>

    <!-- Metadata & Actions -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Processing Info -->
      <div class="glass-morphism p-6">
        <h4 class="text-lg font-semibold text-white mb-4">Processing Details</h4>
        <div class="space-y-3">
          <div class="flex justify-between">
            <span class="text-dark-300">Processing Time:</span>
            <span class="text-white">{{ metadata.processingTime }}s</span>
          </div>
          <div class="flex justify-between">
            <span class="text-dark-300">Dimensions:</span>
            <span class="text-white">{{ metadata.dimensions.width }} × {{ metadata.dimensions.height }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-dark-300">Intensity:</span>
            <span class="text-white">{{ metadata.parametersUsed.intensity }}%</span>
          </div>
          <div class="flex justify-between">
            <span class="text-dark-300">Saturation:</span>
            <span class="text-white">{{ metadata.parametersUsed.saturation }}%</span>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="glass-morphism p-6">
        <h4 class="text-lg font-semibold text-white mb-4">Quick Actions</h4>
        <div class="space-y-3">
          <button
            @click="downloadImage"
            class="btn-primary w-full flex items-center justify-center space-x-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <span>Download Result</span>
          </button>
          
          <button
            @click="shareResult"
            class="btn-secondary w-full flex items-center justify-center space-x-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"/>
            </svg>
            <span>Share Result</span>
          </button>
          
          <button
            @click="$emit('try-another')"
            class="btn-secondary w-full flex items-center justify-center space-x-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            <span>Try Another</span>
          </button>
        </div>
      </div>

      <!-- Tips & Info -->
      <div class="glass-morphism p-6">
        <h4 class="text-lg font-semibold text-white mb-4">Tips & Info</h4>
        <div class="space-y-3 text-sm">
          <div class="flex items-start space-x-2">
            <div class="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
            <p class="text-dark-300">
              The colorization maintains the original image structure and details
            </p>
          </div>
          <div class="flex items-start space-x-2">
            <div class="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
            <p class="text-dark-300">
              Colors are predicted based on learned patterns from millions of images
            </p>
          </div>
          <div class="flex items-start space-x-2">
            <div class="w-2 h-2 bg-purple-500 rounded-full mt-2 flex-shrink-0"></div>
            <p class="text-dark-300">
              You can adjust parameters and try again for different results
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Animation -->
    <div class="text-center mt-8">
      <div class="inline-flex items-center space-x-2 text-green-400">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span class="font-semibold">Colorization completed successfully!</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Props
const props = defineProps<{
  originalImage: string
  colorizedImage: string
  metadata: {
    processingTime: number
    parametersUsed: any
    dimensions: {
      width: number
      height: number
    }
  }
}>()

// Emits
const emit = defineEmits<{
  'try-another': []
  'download': [imageData: string, filename: string]
}>()

// State
const sliderPosition = ref(50)
const isDragging = ref(false)

// Methods
const downloadImage = () => {
  const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-')
  emit('download', props.colorizedImage, `colorized-photo-${timestamp}.jpg`)
}

const shareResult = async () => {
  try {
    if (navigator.share && navigator.canShare) {
      const response = await fetch(props.colorizedImage)
      const blob = await response.blob()
      const file = new File([blob], 'colorized-photo.jpg', { type: 'image/jpeg' })
      
      await navigator.share({
        title: 'Check out my colorized photo!',
        text: 'I used AI to colorize this black and white photo.',
        files: [file]
      })
    } else {
      // Fallback: copy image to clipboard
      await navigator.clipboard.writeText(window.location.href)
      alert('Image URL copied to clipboard!')
    }
  } catch (error) {
    console.error('Share failed:', error)
    alert('Sharing failed. Please download the image instead.')
  }
}

const startDragging = (event: MouseEvent | TouchEvent) => {
  isDragging.value = true
  updateSliderPosition(event)
  
  const moveHandler = (e: MouseEvent | TouchEvent) => {
    if (isDragging.value) {
      updateSliderPosition(e)
    }
  }
  
  const upHandler = () => {
    isDragging.value = false
    document.removeEventListener('mousemove', moveHandler)
    document.removeEventListener('mouseup', upHandler)
    document.removeEventListener('touchmove', moveHandler)
    document.removeEventListener('touchend', upHandler)
  }
  
  document.addEventListener('mousemove', moveHandler)
  document.addEventListener('mouseup', upHandler)
  document.addEventListener('touchmove', moveHandler)
  document.addEventListener('touchend', upHandler)
}

const updateSliderPosition = (event: MouseEvent | TouchEvent) => {
  const rect = (event.target as HTMLElement).closest('.relative')?.getBoundingClientRect()
  if (!rect) return
  
  const clientX = 'touches' in event ? event.touches[0].clientX : event.clientX
  const position = ((clientX - rect.left) / rect.width) * 100
  sliderPosition.value = Math.max(0, Math.min(100, position))
}
</script>