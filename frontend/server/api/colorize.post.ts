export default defineEventHandler(async (event) => {
  try {
    // Parse multipart form data
    const form = await readMultipartFormData(event)
    
    if (!form) {
      throw createError({
        statusCode: 400,
        statusMessage: 'No form data provided'
      })
    }
    
    // Find file and parameters
    const file = form.find(item => item.name === 'file')
    const paramsField = form.find(item => item.name === 'parameters')
    
    if (!file) {
      throw createError({
        statusCode: 400,
        statusMessage: 'No image file provided'
      })
    }
    
    // Validate file type
    if (!file.type?.startsWith('image/')) {
      throw createError({
        statusCode: 400,
        statusMessage: 'Invalid file type. Please provide an image file.'
      })
    }
    
    // Parse parameters
    let parameters = {
      intensity: 100,
      contrast: 0,
      saturation: 100,
      temperature: 0
    }
    
    if (paramsField?.data) {
      try {
        const parsed = JSON.parse(paramsField.data.toString())
        parameters = { ...parameters, ...parsed }
      } catch (error) {
        console.warn('Failed to parse parameters, using defaults')
      }
    }
    
    // Convert file data to FormData for backend API
    const formData = new FormData()
    const blob = new Blob([file.data], { type: file.type })
    formData.append('file', blob, file.filename)
    
    // Get backend API URL from config
    const config = useRuntimeConfig()
    const apiUrl = config.public.apiUrl || 'http://localhost:8000'
    
    try {
      // Forward request to Python backend
      const backendResponse = await fetch(`${apiUrl}/colorize`, {
        method: 'POST',
        body: formData
      })
      
      if (!backendResponse.ok) {
        const error = await backendResponse.json()
        throw new Error(error.detail || 'Backend colorization failed')
      }
      
      const result = await backendResponse.json()
      
      // Return success response with colorized image from backend
      return {
        success: true,
        image: result.colorized_image,
        metadata: {
          parametersUsed: parameters,
          message: result.message
        }
      }
      
    } catch (backendError: any) {
      console.error('Backend API error:', backendError)
      throw createError({
        statusCode: 500,
        statusMessage: `Backend error: ${backendError.message}`
      })
    }
    
  } catch (error: any) {
    console.error('Colorization API error:', error)
    
    throw createError({
      statusCode: error.statusCode || 500,
      statusMessage: error.statusMessage || error.message || 'Failed to process image'
    })
  }
})