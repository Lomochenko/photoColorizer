<template>
  <div class="max-w-4xl mx-auto">
    <!-- Upload Zone -->
    <div 
      class="glass-morphism p-8 mb-8 hover-lift"
      @dragover.prevent
      @drop.prevent="handleDrop"
      @dragenter="isDragging = true"
      @dragleave="isDragging = false"
      :class="{ 'border-blue-500 bg-blue-500/10': isDragging }"
    >
      <div class="text-center">
        <!-- Upload Icon -->
        <div class="w-20 h-20 mx-auto mb-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
          </svg>
        </div>

        <!-- Upload Text -->
        <h2 class="text-2xl font-bold text-white mb-2">
          Upload Your Black & White Photo
        </h2>
        <p class="text-dark-300 mb-6">
          Drag and drop your image here, or click to browse
        </p>

        <!-- File Input -->
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleFileSelect"
        />
        
        <button
          @click="$refs.fileInput.click()"
          class="btn-primary mb-4"
        >
          Choose Image
        </button>

        <!-- Supported Formats -->
        <p class="text-sm text-dark-400">
          Supports JPG, PNG, WEBP • Max size 10MB
        </p>
      </div>
    </div>

    <!-- File Preview -->
    <div v-if="selectedFile" class="glass-morphism p-6 mb-6 animate-slide-up">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-4">
          <div class="w-16 h-16 image-container">
            <img 
              :src="previewUrl" 
              alt="Preview" 
              class="w-full h-full object-cover rounded-lg"
            />
          </div>
          <div>
            <h3 class="text-white font-semibold">{{ selectedFile.name }}</h3>
            <p class="text-dark-400 text-sm">{{ formatFileSize(selectedFile.size) }}</p>
          </div>
        </div>
        <button
          @click="removeFile"
          class="p-2 text-dark-400 hover:text-red-400 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- Processing Parameters -->
      <div class="space-y-6">
        <h4 class="text-lg font-semibold text-white">Colorization Parameters</h4>
        
        <!-- Intensity Slider -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-dark-300">Intensity</label>
            <span class="text-white font-medium">{{ parameters.intensity }}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="100"
            v-model="parameters.intensity"
            class="slider"
          />
          <p class="text-xs text-dark-400 mt-1">Controls the strength of colorization effect</p>
        </div>

        <!-- Contrast Slider -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-dark-300">Contrast</label>
            <span class="text-white font-medium">{{ parameters.contrast }}</span>
          </div>
          <input
            type="range"
            min="-50"
            max="50"
            v-model="parameters.contrast"
            class="slider"
          />
          <p class="text-xs text-dark-400 mt-1">Adjust image contrast after colorization</p>
        </div>

        <!-- Saturation Slider -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-dark-300">Saturation</label>
            <span class="text-white font-medium">{{ parameters.saturation }}%</span>
          </div>
          <input
            type="range"
            min="0"
            max="200"
            v-model="parameters.saturation"
            class="slider"
          />
          <p class="text-xs text-dark-400 mt-1">Adjust color vibrancy</p>
        </div>

        <!-- Temperature Slider -->
        <div>
          <div class="flex items-center justify-between mb-2">
            <label class="text-dark-300">Temperature</label>
            <span class="text-white font-medium">{{ parameters.temperature }}</span>
          </div>
          <input
            type="range"
            min="-100"
            max="100"
            v-model="parameters.temperature"
            class="slider"
          />
          <p class="text-xs text-dark-400 mt-1">Adjust color warmth (negative = cooler, positive = warmer)</p>
        </div>

        <!-- Preset Buttons -->
        <div>
          <label class="text-dark-300 block mb-3">Quick Presets</label>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
            <button
              @click="applyPreset('natural')"
              class="btn-secondary text-sm py-2 px-3"
              :class="{ 'bg-blue-600 border-blue-500': currentPreset === 'natural' }"
            >
              Natural
            </button>
            <button
              @click="applyPreset('vivid')"
              class="btn-secondary text-sm py-2 px-3"
              :class="{ 'bg-blue-600 border-blue-500': currentPreset === 'vivid' }"
            >
              Vivid
            </button>
            <button
              @click="applyPreset('vintage')"
              class="btn-secondary text-sm py-2 px-3"
              :class="{ 'bg-blue-600 border-blue-500': currentPreset === 'vintage' }"
            >
              Vintage
            </button>
            <button
              @click="applyPreset('warm')"
              class="btn-secondary text-sm py-2 px-3"
              :class="{ 'bg-blue-600 border-blue-500': currentPreset === 'warm' }"
            >
              Warm
            </button>
          </div>
        </div>
      </div>

      <!-- Process Button -->
      <div class="mt-6 pt-6 border-t border-dark-700">
        <button
          @click="startProcessing"
          :disabled="isProcessing"
          class="btn-primary w-full flex items-center justify-center space-x-2"
        >
          <svg v-if="!isProcessing" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
          <svg v-else class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
          </svg>
          <span>{{ isProcessing ? 'Processing...' : 'Colorize Image' }}</span>
        </button>
      </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
      <div class="glass-morphism p-6 text-center hover-lift">
        <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <h3 class="text-white font-semibold mb-2">High Quality</h3>
        <p class="text-dark-400 text-sm">
          Advanced neural networks ensure realistic and vibrant colorization results
        </p>
      </div>

      <div class="glass-morphism p-6 text-center hover-lift">
        <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
          </svg>
        </div>
        <h3 class="text-white font-semibold mb-2">Fast Processing</h3>
        <p class="text-dark-400 text-sm">
          Get your colorized photos in seconds with optimized GPU acceleration
        </p>
      </div>

      <div class="glass-morphism p-6 text-center hover-lift">
        <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center mx-auto mb-4">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"/>
          </svg>
        </div>
        <h3 class="text-white font-semibold mb-2">Customizable</h3>
        <p class="text-dark-400 text-sm">
          Fine-tune colorization parameters to achieve your desired artistic effect
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'

// Emits
const emit = defineEmits<{
  'file-selected': [file: File]
  'processing-start': [file: File, parameters: any]
}>()

// State
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const isProcessing = ref(false)
const currentPreset = ref<string>('natural')

// Parameters
const parameters = reactive({
  intensity: 100,
  contrast: 0,
  saturation: 100,
  temperature: 0
})

// Computed
const previewUrl = computed(() => {
  return selectedFile.value ? URL.createObjectURL(selectedFile.value) : ''
})

// Methods
const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    selectFile(target.files[0])
  }
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    selectFile(event.dataTransfer.files[0])
  }
}

const selectFile = (file: File) => {
  // Validate file
  if (!file.type.startsWith('image/')) {
    alert('Please select a valid image file.')
    return
  }
  
  if (file.size > 10 * 1024 * 1024) { // 10MB limit
    alert('File size must be less than 10MB.')
    return
  }
  
  selectedFile.value = file
  emit('file-selected', file)
}

const removeFile = () => {
  selectedFile.value = null
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
}

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const applyPreset = (preset: string) => {
  currentPreset.value = preset
  
  switch (preset) {
    case 'natural':
      Object.assign(parameters, { intensity: 100, contrast: 0, saturation: 100, temperature: 0 })
      break
    case 'vivid':
      Object.assign(parameters, { intensity: 120, contrast: 10, saturation: 150, temperature: 0 })
      break
    case 'vintage':
      Object.assign(parameters, { intensity: 80, contrast: -10, saturation: 80, temperature: 20 })
      break
    case 'warm':
      Object.assign(parameters, { intensity: 100, contrast: 5, saturation: 110, temperature: 30 })
      break
  }
}

const startProcessing = () => {
  if (!selectedFile.value || isProcessing.value) return
  
  isProcessing.value = true
  emit('processing-start', selectedFile.value, { ...parameters })
}

// Imports
import { onUnmounted } from 'vue'

// Cleanup
onUnmounted(() => {
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
  }
})
</script>