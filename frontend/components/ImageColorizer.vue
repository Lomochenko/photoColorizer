<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 py-12 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold text-gray-800 mb-4">
          🎨 Photo Colorizer
        </h1>
        <p class="text-xl text-gray-600">
          Transform your black & white photos into vibrant color images using AI
        </p>
      </div>

      <!-- Main Card -->
      <div class="bg-white rounded-2xl shadow-2xl p-8 md:p-12">
        <!-- Upload Section -->
        <div class="mb-8">
          <label class="block text-lg font-semibold text-gray-700 mb-3">
            Upload Your Image
          </label>
          <div
            class="border-3 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-500 transition-colors cursor-pointer"
            @dragover.prevent="isDragging = true"
            @dragleave.prevent="isDragging = false"
            @drop.prevent="handleDrop"
            :class="{ 'border-blue-500 bg-blue-50': isDragging }"
          >
            <input
              ref="fileInput"
              type="file"
              @change="handleFileSelect"
              accept="image/*"
              class="hidden"
            />
            <div @click="$refs.fileInput.click()">
              <svg
                class="mx-auto h-16 w-16 text-gray-400 mb-4"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              <p class="text-lg text-gray-600 mb-2">
                Click to upload or drag and drop
              </p>
              <p class="text-sm text-gray-500">PNG, JPG, GIF up to 10MB</p>
            </div>
          </div>
        </div>

        <!-- Colorize Button -->
        <button
          v-if="selectedFile && !loading"
          @click="colorize"
          class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-xl font-bold text-lg hover:from-blue-700 hover:to-purple-700 transition-all transform hover:scale-105 shadow-lg"
        >
          ✨ Colorize Image
        </button>

        <!-- Loading State -->
        <div v-if="loading" class="mt-8">
          <div class="flex items-center justify-center mb-4">
            <div class="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600"></div>
          </div>
          <p class="text-center text-gray-600 font-medium">
            🧠 AI is working its magic... This may take 30-60 seconds
          </p>
          <div class="mt-4 bg-blue-50 rounded-lg p-4">
            <div class="h-2 bg-blue-200 rounded-full overflow-hidden">
              <div class="h-full bg-blue-600 rounded-full animate-pulse" style="width: 70%"></div>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-6 p-4 bg-red-50 border-l-4 border-red-500 rounded">
          <div class="flex items-center">
            <svg class="h-5 w-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
            <p class="text-red-700 font-medium">{{ error }}</p>
          </div>
        </div>

        <!-- Results Grid -->
        <div v-if="originalPreview || colorizedImage" class="mt-12">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">
            Results
          </h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <!-- Original Image -->
            <div v-if="originalPreview" class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-700 flex items-center">
                <span class="mr-2">📷</span> Original
              </h3>
              <div class="relative rounded-xl overflow-hidden shadow-xl">
                <img
                  :src="originalPreview"
                  alt="Original"
                  class="w-full h-auto"
                />
              </div>
            </div>

            <!-- Colorized Image -->
            <div v-if="colorizedImage" class="space-y-3">
              <h3 class="text-lg font-semibold text-gray-700 flex items-center">
                <span class="mr-2">🌈</span> Colorized
              </h3>
              <div class="relative rounded-xl overflow-hidden shadow-xl">
                <img
                  :src="colorizedImage"
                  alt="Colorized"
                  class="w-full h-auto"
                />
              </div>
              <a
                :href="colorizedImage"
                download="colorized-photo.jpg"
                class="block w-full bg-green-600 text-white py-3 rounded-lg font-semibold text-center hover:bg-green-700 transition-colors"
              >
                ⬇️ Download Colorized Image
              </a>
            </div>
          </div>
        </div>
      </div>

      <!-- Info Section -->
      <div class="mt-12 bg-white rounded-xl shadow-lg p-8">
        <h3 class="text-2xl font-bold text-gray-800 mb-4">💡 How it works</h3>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-4xl mb-3">📎</div>
            <h4 class="font-semibold text-gray-700 mb-2">1. Upload</h4>
            <p class="text-gray-600 text-sm">Choose your black & white photo</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">🧠</div>
            <h4 class="font-semibold text-gray-700 mb-2">2. AI Processing</h4>
            <p class="text-gray-600 text-sm">Our AI analyzes and colorizes</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">✨</div>
            <h4 class="font-semibold text-gray-700 mb-2">3. Download</h4>
            <p class="text-gray-600 text-sm">Get your colorized photo!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { colorizeImage } = useColorizer()

const fileInput = ref(null)
const selectedFile = ref<File | null>(null)
const originalPreview = ref<string>('')
const colorizedImage = ref<string>('')
const loading = ref(false)
const error = ref('')
const isDragging = ref(false)

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  processFile(file)
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  const file = event.dataTransfer?.files[0]
  processFile(file)
}

const processFile = (file: File | undefined) => {
  if (!file) return

  // Validate file type
  if (!file.type.startsWith('image/')) {
    error.value = 'Please upload an image file'
    return
  }

  // Validate file size (10MB max)
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'File size must be less than 10MB'
    return
  }

  selectedFile.value = file
  originalPreview.value = URL.createObjectURL(file)
  colorizedImage.value = ''
  error.value = ''
}

const colorize = async () => {
  if (!selectedFile.value) return

  loading.value = true
  error.value = ''
  colorizedImage.value = ''

  try {
    const result = await colorizeImage(selectedFile.value)
    colorizedImage.value = result
    
    // Confetti animation on success
    if (import.meta.client && window.confetti) {
      window.confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      })
    }
  } catch (e: any) {
    error.value = e.message || 'Failed to colorize image. Please try again.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

// Cleanup on unmount
onUnmounted(() => {
  if (originalPreview.value) URL.revokeObjectURL(originalPreview.value)
})
</script>
