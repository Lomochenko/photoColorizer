interface ColorizationParameters {
  intensity: number
  contrast: number
  saturation: number
  temperature: number
}

interface ColorizationMetadata {
  processingTime: number
  parametersUsed: ColorizationParameters
  dimensions: {
    width: number
    height: number
  }
}

interface ColorizationResult {
  image: string
  metadata: ColorizationMetadata
}

export function useColorization() {
  const runtimeConfig = useRuntimeConfig()
  
  const colorizeImage = async (
    file: File, 
    parameters: ColorizationParameters,
    onProgress?: (progress: number, status: string) => void
  ): Promise<ColorizationResult> => {
    
    // Start timing
    const startTime = Date.now()
    
    try {
      // Simulate progress updates
      if (onProgress) {
        onProgress(10, 'Uploading image...')
        await new Promise(resolve => setTimeout(resolve, 500))
        
        onProgress(30, 'Preprocessing image...')
        await new Promise(resolve => setTimeout(resolve, 800))
        
        onProgress(60, 'Running neural network...')
        await new Promise(resolve => setTimeout(resolve, 1200))
        
        onProgress(85, 'Applying color adjustments...')
        await new Promise(resolve => setTimeout(resolve, 600))
        
        onProgress(95, 'Finalizing result...')
        await new Promise(resolve => setTimeout(resolve, 400))
      }
      
      // Create form data
      const formData = new FormData()
      formData.append('file', file)
      formData.append('parameters', JSON.stringify(parameters))
      
      // Make API call to colorization endpoint
      const response = await $fetch('/api/colorize', {
        method: 'POST',
        body: formData
      })
      
      if (!response.success) {
        throw new Error(response.error || 'Colorization failed')
      }
      
      // Calculate processing time
      const processingTime = (Date.now() - startTime) / 1000
      
      // Return result with metadata
      return {
        image: response.image,
        metadata: {
          processingTime: Math.round(processingTime * 10) / 10,
          parametersUsed: parameters,
          dimensions: response.dimensions || { width: 0, height: 0 }
        }
      }
      
    } catch (error: any) {
      console.error('Colorization error:', error)
      throw new Error(error.message || 'Failed to colorize image')
    }
  }
  
  const validateImage = (file: File): { valid: boolean; error?: string } => {
    // Check file type
    if (!file.type.startsWith('image/')) {
      return { valid: false, error: 'Please select a valid image file' }
    }
    
    // Check file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      return { valid: false, error: 'File size must be less than 10MB' }
    }
    
    // Check supported formats
    const supportedTypes = ['image/jpeg', 'image/png', 'image/webp']
    if (!supportedTypes.includes(file.type)) {
      return { valid: false, error: 'Supported formats: JPG, PNG, WEBP' }
    }
    
    return { valid: true }
  }
  
  const getImageDimensions = (file: File): Promise<{ width: number; height: number }> => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = () => {
        resolve({ width: img.width, height: img.height })
      }
      img.onerror = reject
      img.src = URL.createObjectURL(file)
    })
  }
  
  const createThumbnail = (imageData: string, maxWidth: number = 300): Promise<string> => {
    return new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        const ctx = canvas.getContext('2d')!
        
        // Calculate dimensions while maintaining aspect ratio
        const ratio = Math.min(maxWidth / img.width, maxWidth / img.height)
        canvas.width = img.width * ratio
        canvas.height = img.height * ratio
        
        // Draw image
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height)
        
        // Convert to data URL
        resolve(canvas.toDataURL('image/jpeg', 0.8))
      }
      img.onerror = reject
      img.src = imageData
    })
  }
  
  return {
    colorizeImage,
    validateImage,
    getImageDimensions,
    createThumbnail
  }
}