# 🎨 AI Photo Colorizer

Transform your black & white photos into vibrant color images using AI-powered deep learning!

![Photo Colorizer Demo](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- 🤖 **AI-Powered Colorization** - Uses state-of-the-art deep learning models
- ⚡ **Fast Processing** - Cloud GPU acceleration via Replicate.com
- 🎯 **Easy to Use** - Simple drag & drop interface
- 📱 **Responsive Design** - Works on desktop and mobile
- 💾 **Download Results** - Save your colorized photos instantly
- 🔒 **Privacy First** - Images processed securely

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- Replicate.com API token (free tier available)

### 1. Get Replicate API Token

1. Go to [Replicate.com](https://replicate.com)
2. Sign up for a free account
3. Navigate to [Account Settings](https://replicate.com/account/api-tokens)
4. Copy your API token
5. First $5/month in credits are FREE!

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your Replicate API token
# REPLICATE_API_TOKEN=your_token_here

# Run the backend server
python main.py
```

The backend will start at `http://localhost:8000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run the development server
npm run dev
```

The frontend will start at `http://localhost:3000`

### 4. Open Your Browser

Visit `http://localhost:3000` and start colorizing photos! 🎉

## 📁 Project Structure

```
photoColorizer/
├── backend/              # FastAPI backend
│   ├── main.py          # Main API server
│   ├── requirements.txt # Python dependencies
│   ├── .env.example     # Environment variables template
│   └── README.md        # Backend documentation
│
├── frontend/            # Nuxt 3 frontend
│   ├── components/      # Vue components
│   │   └── ImageColorizer.vue
│   ├── composables/     # Composable functions
│   │   └── useColorizer.ts
│   ├── app.vue          # Main app component
│   ├── nuxt.config.ts   # Nuxt configuration
│   └── package.json     # Node dependencies
│
└── ImageColorizerColab.ipynb  # Original Colab notebook (reference)
```

## 🌐 Deployment

### Deploy Backend (Railway.app - Recommended)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Set root directory to `backend`
6. Add environment variable: `REPLICATE_API_TOKEN`
7. Deploy! ✅

### Deploy Frontend (Vercel - Recommended)

1. Go to [Vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Add environment variable:
   - `NUXT_PUBLIC_API_URL=https://your-backend-url.railway.app`
5. Deploy! ✅

## 💰 Cost Breakdown

### Replicate.com Pricing
- **Free tier**: $5/month in credits
- **Per image**: ~$0.01-0.05 per colorization
- **Estimate**: ~100-500 images free per month

### Hosting
- **Railway.app**: Free tier available ($5/month for more usage)
- **Vercel.com**: Free tier for frontend (generous limits)

**Total Cost for Small Projects**: $0-10/month 💵

## 🛠️ How It Works

1. **Upload**: User uploads a black & white photo
2. **API Call**: Frontend sends image to backend
3. **AI Processing**: Backend calls Replicate.com API with DeOldify model
4. **Response**: Colorized image returned as base64
5. **Display**: Frontend shows before/after comparison
6. **Download**: User can save the colorized image

## 🔧 API Endpoints

### POST /colorize
Colorize an uploaded image.

**Request:**
```bash
curl -X POST http://localhost:8000/colorize \
  -F "file=@your-image.jpg"
```

**Response:**
```json
{
  "success": true,
  "colorized_image": "data:image/jpeg;base64,...",
  "message": "Image colorized successfully"
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "replicate_configured": true,
  "model": "deoldify"
}
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [DeOldify](https://github.com/jantic/DeOldify) - The amazing colorization model
- [Replicate.com](https://replicate.com) - Easy AI model deployment
- [Nuxt 3](https://nuxt.com) - The intuitive Vue framework
- [FastAPI](https://fastapi.tiangolo.com) - Modern Python web framework

## 📧 Contact

If you have any questions or suggestions, feel free to open an issue!

---

Made with ❤️ and AI
