<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-50 to-pink-100 py-12 px-4">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-10">
        <h1 class="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600 mb-4">
          🎨 Photo Colorizer
        </h1>
        <p class="text-xl text-gray-700">
          Transform black & white photos into vibrant colors using AI
        </p>
      </div>

      <!-- Main Card -->
      <div class="bg-white rounded-3xl shadow-2xl p-8 md:p-12">
        <!-- Upload Area -->
        <div v-if="!selectedImage" class="border-4 border-dashed border-gray-300 rounded-2xl p-12 text-center hover:border-purple-400 transition-colors cursor-pointer" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
          <input ref="fileInput" type="file" accept="image/*" @change="handleFileSelect" class="hidden" />
          <svg class="mx-auto h-20 w-20 text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          <p class="text-xl font-semibold text-gray-700 mb-2">
            Click to upload or drag & drop
          </p>
          <p class="text-sm text-gray-500">PNG, JPG, GIF up to 10MB</p>
        </div>

        <!-- Preview & Controls -->
        <div v-if="selectedImage">
          <div class="mb-6">
            <img :src="selectedImage" alt="Selected" class="w-full rounded-xl shadow-lg" />
          </div>

          <!-- Quality Slider -->
          <div class="mb-6">
            <label class="block text-sm font-semibold text-gray-700 mb-2">
              Render Quality: {{ renderFactor }}
            </label>
            <input v-model.number="renderFactor" type="range" min="10" max="45" class="w-full h-3 bg-gray-200 rounded-lg appearance-none cursor-pointer" />
            <div class="flex justify-between text-xs text-gray-500 mt-1">
              <span>Fast</span>
              <span>Best Quality</span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-4">
            <button @click="colorizeImage" :disabled="loading" class="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 rounded-xl font-bold text-lg hover:from-purple-700 hover:to-pink-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 shadow-lg">
              {{ loading ? 'Processing...' : '✨ Colorize' }}
            </button>
            <button @click="reset" class="px-6 py-4 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-colors">
              Reset
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="mt-8 text-center">
          <div class="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-purple-600 mb-4"></div>
          <p class="text-gray-600 font-medium">AI is colorizing your photo...</p>
          <p class="text-sm text-gray-500 mt-2">This may take 30-90 seconds. First time may take longer as the Space wakes up.</p>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-6 bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <p class="text-red-700 font-medium">{{ error }}</p>
          <p class="text-sm text-red-600 mt-2">Try visiting <a href="https://jaysadatay-deoldify.hf.space" target="_blank" class="underline">the Space</a> directly first to wake it up, then try again.</p>
        </div>

        <!-- Results -->
        <div v-if="colorizedImage" class="mt-8">
          <h2 class="text-2xl font-bold text-gray-800 mb-4 text-center">✨ Result</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Original -->
            <div>
              <h3 class="text-sm font-semibold text-gray-600 mb-2">Original</h3>
              <img :src="selectedImage" alt="Original" class="w-full rounded-xl shadow-lg" />
            </div>
            <!-- Colorized -->
            <div>
              <h3 class="text-sm font-semibold text-gray-600 mb-2">Colorized</h3>
              <img :src="colorizedImage" alt="Colorized" class="w-full rounded-xl shadow-lg" />
            </div>
          </div>
          <div class="text-center mt-6">
            <a :href="colorizedImage" download="colorized.jpg" class="inline-block bg-green-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-green-700 transition-colors shadow-lg">
              ⬇️ Download Result
            </a>
          </div>
        </div>
      </div>

      <!-- Footer Info -->
      <div class="mt-8 text-center text-gray-600 text-sm">
        <p>Powered by DeOldify AI Model via Hugging Face 🤗</p>
        <p class="mt-2 text-xs">Using Space: <a href="https://huggingface.co/spaces/jaysadatay/deoldify" target="_blank" class="text-purple-600 hover:underline">jaysadatay/deoldify</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import '~/assets/css/main.css'

const fileInput = ref(null)
const selectedImage = ref(null)
const selectedFile = ref(null)
const colorizedImage = ref(null)
const renderFactor = ref(35)
const loading = ref(false)
const error = ref('')

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) processFile(file)
}

const handleDrop = (event) => {
  const file = event.dataTransfer?.files[0]
  if (file) processFile(file)
}

const processFile = (file) => {
  if (!file.type.startsWith('image/')) {
    error.value = 'Please upload an image file'
    return
  }
  if (file.size > 10 * 1024 * 1024) {
    error.value = 'File size must be less than 10MB'
    return
  }
  selectedFile.value = file
  selectedImage.value = URL.createObjectURL(file)
  colorizedImage.value = null
  error.value = ''
}

const colorizeImage = async () => {
  if (!selectedFile.value) return

  loading.value = true
  error.value = ''

  try {
    // Use Gradio client library approach
    const formData = new FormData()
    formData.append('files', selectedFile.value)
    
    // First, upload the file
    const uploadResponse = await fetch('https://jaysadatay-deoldify.hf.space/upload', {
      method: 'POST',
      body: formData
    })

    if (!uploadResponse.ok) {
      throw new Error(`Upload failed: ${uploadResponse.status}. The Space may be sleeping.`)
    }

    const uploadData = await uploadResponse.json()
    const fileUrl = uploadData[0]

    // Then, call the predict endpoint
    const predictResponse = await fetch('https://jaysadatay-deoldify.hf.space/call/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        data: [
          { path: fileUrl },
          renderFactor.value
        ]
      })
    })

    if (!predictResponse.ok) {
      throw new Error(`Prediction failed: ${predictResponse.status}`)
    }

    const predictData = await predictResponse.json()
    const eventId = predictData.event_id

    // Poll for results
    const result = await pollForResult(eventId)
    
    if (result && result.data && result.data[0]) {
      const resultPath = result.data[0].path || result.data[0]
      colorizedImage.value = `https://jaysadatay-deoldify.hf.space/file=${resultPath}`
    } else {
      throw new Error('No colorized image in response')
    }
  } catch (e) {
    error.value = e.message || 'Failed to colorize. The Hugging Face Space might be sleeping or unavailable.'
    console.error('Colorization error:', e)
  } finally {
    loading.value = false
  }
}

const pollForResult = async (eventId, maxAttempts = 60) => {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const response = await fetch(`https://jaysadatay-deoldify.hf.space/call/predict/${eventId}`)
      if (!response.ok) {
        await new Promise(resolve => setTimeout(resolve, 1000))
        continue
      }
      
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              if (data.msg === 'process_completed') {
                return data.output
              }
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
      }
    } catch (e) {
      console.error('Polling error:', e)
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000))
  }
  
  throw new Error('Timeout waiting for colorization')
}

const reset = () => {
  selectedImage.value = null
  selectedFile.value = null
  colorizedImage.value = null
  error.value = ''
  if (fileInput.value) fileInput.value.value = ''
}

onUnmounted(() => {
  if (selectedImage.value) URL.revokeObjectURL(selectedImage.value)
})
</script>
