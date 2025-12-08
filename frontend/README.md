# PhotoColorizer Web Application

A modern, high-performance web application for AI-powered black and white photo colorization. Built with Nuxt 3 and OpenCV DNN, featuring a beautiful dark theme UI and advanced colorization controls.

## Features

### 🎨 Advanced Colorization
- **AI-Powered**: Uses advanced deep learning models for realistic colorization
- **Customizable Parameters**: Adjust intensity, contrast, saturation, and temperature
- **Quick Presets**: Natural, Vivid, Vintage, and Warm colorization styles
- **High Quality**: Maintains original image structure and details

### 🚀 Modern Web Experience
- **Dark Theme**: Beautiful glass morphism UI with smooth animations
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Real-time Processing**: Live progress updates and status messages
- **Drag & Drop**: Intuitive file upload with preview

### ⚡ Performance & Scalability
- **Fast Processing**: GPU-accelerated colorization with optimized models
- **Batch Processing**: Handle multiple images efficiently
- **Caching System**: Redis integration for improved performance
- **Cloud Ready**: Docker support for easy deployment

## Technology Stack

### Frontend
- **Nuxt 3**: Vue.js framework with SSR/SSG support
- **Tailwind CSS**: Utility-first CSS framework
- **TypeScript**: Type-safe development
- **VueUse**: Composable utilities for Vue

### Backend
- **FastAPI**: Modern Python web framework
- **OpenCV DNN**: Deep learning-based colorization
- **Caffe Model**: Pre-trained colorization model
- **Redis**: Caching and session storage

### Infrastructure
- **Docker**: Containerization for easy deployment
- **Vercel**: Frontend hosting with edge functions
- **GPU Support**: CUDA acceleration for model inference

## Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+ (for local development)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lomochenko/photoColorizer.git
   cd photoColorizer-web
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies**
   ```bash
   cd python
   pip install -r requirements.txt
   cd ..
   ```

4. **Download model files**
   ```bash
   mkdir -p python/models
   cd python/models
   
   # Download Caffe model files
   wget https://github.com/richzhang/colorization/raw/master/models/colorization_deploy_v2.prototxt
   wget https://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel
   wget https://github.com/richzhang/colorization/raw/master/resources/pts_in_hull.npy
   ```

5. **Run development server**
   ```bash
   # Frontend (in one terminal)
   npm run dev
   
   # Backend (in another terminal)
   cd python
   uvicorn main:app --reload --port 8000
   ```

6. **Open your browser**
   Navigate to `http://localhost:3000`

## Usage

### Basic Colorization
1. Upload a black and white image (JPG, PNG, WEBP up to 10MB)
2. Adjust colorization parameters or select a preset
3. Click "Colorize Image" to start processing
4. Download or share your colorized result

### Advanced Parameters
- **Intensity**: Controls overall colorization strength (0-100%)
- **Contrast**: Adjust image contrast after colorization (-50 to +50)
- **Saturation**: Modify color vibrancy (0-200%)
- **Temperature**: Adjust color warmth (-100 cool to +100 warm)

### Presets
- **Natural**: Balanced, realistic colors (100% intensity, 0 contrast, 100% saturation)
- **Vivid**: Enhanced, vibrant colors (120% intensity, +10 contrast, 150% saturation)
- **Vintage**: Muted, vintage feel (80% intensity, -10 contrast, 80% saturation)
- **Warm**: Warm, golden tones (100% intensity, +5 contrast, +30 temperature)

## Deployment

### Docker Deployment (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy to Vercel**
   ```bash
   vercel --prod
   ```

3. **Configure environment variables**
   - `NUXT_PUBLIC_API_BASE`: Your backend API URL
   - `PYTHON_API_URL`: Python backend URL (if separate)

### Production Backend Deployment

For production backend deployment, you can use:
- **AWS EC2** with GPU instances
- **Google Cloud Run** with GPU support
- **Hugging Face Spaces**
- **Heroku** (with buildpacks)

## API Reference

### Colorize Image
```http
POST /api/colorize
Content-Type: multipart/form-data

Body:
- file: Image file (required)
- parameters: JSON string with colorization parameters (optional)
```

**Response:**
```json
{
  "success": true,
  "image": "base64_encoded_image_data",
  "dimensions": {
    "width": 800,
    "height": 600
  },
  "metadata": {
    "processingTime": 2.5,
    "parametersUsed": {
      "intensity": 100,
      "contrast": 0,
      "saturation": 100,
      "temperature": 0
    }
  }
}
```

### Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

## Development

### Project Structure
```
photoColorizer-web/
├── components/          # Vue components
│   ├── ImageUpload.vue
│   ├── ResultsViewer.vue
│   ├── ProcessingProgress.vue
│   └── Layout/
│       ├── AppHeader.vue
│       └── AppFooter.vue
├── composables/         # Vue composables
│   └── useColorization.ts
├── server/              # Nuxt server API
│   └── api/
│       └── colorize.post.ts
├── python/              # Python backend
│   ├── main.py
│   ├── colorizer.py
│   ├── utils.py
│   └── requirements.txt
├── assets/              # Static assets
│   └── css/
│       └── main.css
├── public/              # Public files
├── nuxt.config.ts       # Nuxt configuration
├── tailwind.config.js   # Tailwind CSS config
├── docker-compose.yml   # Docker configuration
└── README.md
```

### Adding New Features

1. **Frontend Components**: Add new Vue components in `components/`
2. **API Endpoints**: Create new files in `server/api/`
3. **Python Backend**: Modify `python/colorizer.py` for model improvements
4. **Styling**: Update `assets/css/main.css` for custom styles

### Testing

```bash
# Frontend tests
npm run test

# Backend tests
cd python
pytest
```

## Model Details

The application uses the **Colorful Image Colorization** model by Richard Zhang et al.:
- **Architecture**: Convolutional Neural Network (CNN)
- **Framework**: Caffe (converted to OpenCV DNN)
- **Training Dataset**: ImageNet
- **Color Space**: Lab color space for better perceptual uniformity

### Model Files
- `colorization_deploy_v2.prototxt`: Network architecture definition
- `colorization_release_v2.caffemodel`: Trained model weights
- `pts_in_hull.npy`: Color cluster centers for quantization

## Performance Optimization

### Frontend
- **Image Optimization**: Automatic compression and format selection
- **Lazy Loading**: Progressive image loading
- **CDN Integration**: Static asset optimization
- **Service Worker**: Offline support and caching

### Backend
- **GPU Acceleration**: CUDA support for model inference
- **Batch Processing**: Handle multiple images efficiently
- **Redis Caching**: Cache processed results
- **Connection Pooling**: Database connection optimization

## Troubleshooting

### Common Issues

1. **Model files not found**
   - Ensure all model files are in `python/models/`
   - Check file permissions

2. **GPU not available**
   - Install CUDA and cuDNN
   - Use CPU fallback mode

3. **Memory issues**
   - Reduce batch size
   - Use smaller images
   - Increase system memory

4. **CORS errors**
   - Check API endpoint configuration
   - Verify CORS headers in production

### Debug Mode

Enable debug logging:
```bash
# Frontend
DEBUG=true npm run dev

# Backend
python -m uvicorn main:app --reload --log-level debug
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Richard Zhang** et al. for the Colorful Image Colorization research
- **OpenCV** team for the DNN module
- **Nuxt.js** and **Vue.js** communities
- All contributors and supporters

## Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check the `/docs` endpoint for API docs
- **Discord**: Join our community server
- **Email**: support@photocolorizer.com

---

**Built with ❤️ using modern web technologies and advanced AI**