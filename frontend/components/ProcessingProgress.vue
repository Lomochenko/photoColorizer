<template>
  <div class="processing-overlay">
    <div class="glass-morphism max-w-2xl w-full mx-4 p-8 animate-slide-up">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="w-20 h-20 mx-auto mb-4 relative">
          <!-- Animated Circle -->
          <svg class="w-20 h-20 transform -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="40"
              stroke="currentColor"
              stroke-width="8"
              fill="none"
              class="text-dark-700"
            />
            <circle
              cx="50"
              cy="50"
              r="40"
              stroke="url(#gradient)"
              stroke-width="8"
              fill="none"
              stroke-linecap="round"
              :stroke-dasharray="251.2"
              :stroke-dashoffset="251.2 - (progress / 100) * 251.2"
              class="transition-all duration-500 ease-out"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#3B82F6" />
                <stop offset="100%" style="stop-color:#8B5CF6" />
              </linearGradient>
            </defs>
          </svg>
          
          <!-- Center Icon -->
          <div class="absolute inset-0 flex items-center justify-center">
            <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center animate-pulse-slow">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
          </div>
        </div>

        <h2 class="text-3xl font-bold text-white mb-2">
          Colorizing Your Photo
        </h2>
        <p class="text-dark-300">
          Our AI is analyzing your image and adding vibrant colors
        </p>
      </div>

      <!-- Progress Bar -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-2">
          <span class="text-dark-300 text-sm">Processing Progress</span>
          <span class="text-white font-medium">{{ Math.round(progress) }}%</span>
        </div>
        
        <div class="w-full bg-dark-700 rounded-full h-3 overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-500 ease-out relative"
            :style="{ width: `${progress}%` }"
          >
            <div class="absolute inset-0 bg-white/20 animate-pulse"></div>
          </div>
        </div>
      </div>

      <!-- Status Messages -->
      <div class="space-y-4 mb-8">
        <div class="flex items-center space-x-3">
          <div class="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <span class="text-dark-300">Image uploaded successfully</span>
        </div>

        <div class="flex items-center space-x-3">
          <div 
            class="w-6 h-6 rounded-full flex items-center justify-center"
            :class="progress > 25 ? 'bg-green-500' : 'bg-dark-600 animate-spin'"
          >
            <svg v-if="progress > 25" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <span class="text-dark-300">Analyzing image structure</span>
        </div>

        <div class="flex items-center space-x-3">
          <div 
            class="w-6 h-6 rounded-full flex items-center justify-center"
            :class="progress > 50 ? 'bg-green-500' : 'bg-dark-600 animate-spin'"
          >
            <svg v-if="progress > 50" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <span class="text-dark-300">Applying neural network colorization</span>
        </div>

        <div class="flex items-center space-x-3">
          <div 
            class="w-6 h-6 rounded-full flex items-center justify-center"
            :class="progress > 75 ? 'bg-green-500' : 'bg-dark-600 animate-spin'"
          >
            <svg v-if="progress > 75" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <span class="text-dark-300">Finalizing color adjustments</span>
        </div>
      </div>

      <!-- Current Status -->
      <div class="text-center mb-6">
        <div class="glass-morphism p-4 rounded-xl">
          <p class="text-white font-medium">{{ status }}</p>
          <p class="text-dark-400 text-sm mt-1">
            Estimated time remaining: {{ estimatedTime }}
          </p>
        </div>
      </div>

      <!-- Cancel Button -->
      <div class="flex justify-center">
        <button
          @click="$emit('cancel')"
          class="btn-secondary flex items-center space-x-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
          <span>Cancel Processing</span>
        </button>
      </div>

      <!-- Fun Facts -->
      <div class="mt-8 text-center">
        <p class="text-dark-400 text-sm">
          {{ funFacts[currentFactIndex] }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue'

// Props
defineProps<{
  progress: number
  status: string
}>()

// Emits
const emit = defineEmits<{
  cancel: []
}>()

// State
const currentFactIndex = ref(0)
const factInterval = ref<NodeJS.Timeout | null>(null)

// Fun facts about colorization
const funFacts = [
  'The first color photograph was taken in 1861 by James Clerk Maxwell',
  'Human eyes can distinguish about 10 million different colors',
  'The Lab color space was designed to be perceptually uniform',
  'AI colorization models are trained on millions of color images',
  'Colorization can help preserve historical photographs',
  'The process maintains the original image structure and details'
]

// Computed
const estimatedTime = computed(() => {
  if (progress >= 100) return 'Complete!'
  const remaining = Math.ceil((100 - progress) * 0.1)
  return `${remaining} seconds`
})

// Methods
const startFactRotation = () => {
  factInterval.value = setInterval(() => {
    currentFactIndex.value = (currentFactIndex.value + 1) % funFacts.length
  }, 5000)
}

// Lifecycle
onMounted(() => {
  startFactRotation()
})

onUnmounted(() => {
  if (factInterval.value) {
    clearInterval(factInterval.value)
  }
})
</script>