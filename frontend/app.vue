<template>
  <div class="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
    <!-- Header -->
    <AppHeader />
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Upload Section -->
      <section v-if="currentStep === 'upload'" class="animate-fade-in">
        <div class="text-center mb-12">
          <h1 class="text-5xl font-bold gradient-text mb-4">
            AI Photo Colorizer
          </h1>
          <p class="text-xl text-dark-300 max-w-2xl mx-auto">
            Transform your black and white photos into vibrant, colorized memories using advanced deep learning
          </p>
        </div>
        
        <ImageUpload 
          @file-selected="handleFileSelected"
          @processing-start="handleProcessingStart"
        />
      </section>

      <!-- Processing Section -->
      <section v-else-if="currentStep === 'processing'" class="animate-fade-in">
        <ProcessingProgress 
          :progress="processingProgress"
          :status="processingStatus"
          @cancel="handleCancelProcessing"
        />
      </section>

      <!-- Results Section -->
      <section v-else-if="currentStep === 'results'" class="animate-fade-in">
        <ResultsViewer 
          :original-image="originalImage"
          :colorized-image="colorizedImage"
          :metadata="processingMetadata"
          @try-another="handleTryAnother"
          @download="handleDownload"
        />
      </section>
    </main>

    <!-- Footer -->
    <AppFooter />

    <!-- Error Modal -->
    <Transition name="fade">
      <div v-if="showError" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
        <div class="glass-morphism max-w-md w-full p-6 animate-slide-up">
          <div class="flex items-center mb-4">
            <div class="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center mr-4">
              <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"/>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-white">Processing Error</h3>
          </div>
          <p class="text-dark-300 mb-6">{{ errorMessage }}</p>
          <div class="flex gap-3">
            <button @click="handleTryAnother" class="btn-primary flex-1">
              Try Another Image
            </button>
            <button @click="showError = false" class="btn-secondary flex-1">
              Close
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useColorization } from '~/composables/useColorization'
import canvasConfetti from 'canvas-confetti'

// State
const currentStep = ref<'upload' | 'processing' | 'results'>('upload')
const originalImage = ref<string>('')
const colorizedImage = ref<string>('')
const processingProgress = ref(0)
const processingStatus = ref('')
const showError = ref(false)
const errorMessage = ref('')
const processingMetadata = reactive({
  processingTime: 0,
  parametersUsed: {},
  dimensions: { width: 0, height: 0 }
})

// Composables
const { colorizeImage } = useColorization()

// Handlers
const handleFileSelected = (file: File) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    originalImage.value = e.target?.result as string
  }
  reader.readAsDataURL(file)
}

const handleProcessingStart = async (file: File, parameters: any) => {
  try {
    currentStep.value = 'processing'
    processingProgress.value = 0
    processingStatus.value = 'Uploading image...'
    
    // Simulate progress updates
    const progressInterval = setInterval(() => {
      processingProgress.value += Math.random() * 10
      if (processingProgress.value >= 90) {
        clearInterval(progressInterval)
      }
    }, 200)
    
    processingStatus.value = 'Colorizing with AI...'
    
    const result = await colorizeImage(file, parameters, (progress, status) => {
      processingProgress.value = progress
      processingStatus.value = status
    })
    
    clearInterval(progressInterval)
    processingProgress.value = 100
    processingStatus.value = 'Complete!'
    
    // Update results
    colorizedImage.value = result.image
    processingMetadata.processingTime = result.metadata.processingTime
    processingMetadata.parametersUsed = result.metadata.parametersUsed
    processingMetadata.dimensions = result.metadata.dimensions
    
    // Show success animation
    canvasConfetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 }
    })
    
    setTimeout(() => {
      currentStep.value = 'results'
    }, 1000)
    
  } catch (error: any) {
    console.error('Colorization error:', error)
    errorMessage.value = error.message || 'Failed to colorize image. Please try again.'
    showError.value = true
    currentStep.value = 'upload'
  }
}

const handleCancelProcessing = () => {
  currentStep.value = 'upload'
  processingProgress.value = 0
  processingStatus.value = ''
}

const handleTryAnother = () => {
  currentStep.value = 'upload'
  originalImage.value = ''
  colorizedImage.value = ''
  showError.value = false
  errorMessage.value = ''
}

const handleDownload = (imageData: string, filename: string) => {
  const link = document.createElement('a')
  link.href = imageData
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

// Head
useHead({
  title: 'AI Photo Colorizer - Transform B&W Photos',
  meta: [
    { name: 'description', content: 'Transform your black and white photos into vibrant, colorized memories using advanced deep learning technology.' },
    { name: 'keywords', content: 'photo colorization, AI image processing, black and white photos, deep learning, image enhancement' }
  ]
})
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>