export const useColorizer = () => {
  const config = useRuntimeConfig()
  const apiUrl = config.public.apiUrl || 'http://localhost:8000'

  const colorizeImage = async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${apiUrl}/colorize`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Colorization failed')
      }

      const data = await response.json()
      return data.colorized_image
    } catch (error) {
      console.error('Error colorizing image:', error)
      throw error
    }
  }

  const checkHealth = async () => {
    try {
      const response = await fetch(`${apiUrl}/health`)
      return await response.json()
    } catch (error) {
      console.error('Health check failed:', error)
      return { status: 'error' }
    }
  }

  return {
    colorizeImage,
    checkHealth
  }
}
