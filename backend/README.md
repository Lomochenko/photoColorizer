# Photo Colorizer Backend

FastAPI backend that uses Replicate.com to colorize images using AI models.

## Setup

### 1. Get Replicate API Token

1. Go to [Replicate.com](https://replicate.com)
2. Sign up for a free account
3. Go to [Account Settings](https://replicate.com/account/api-tokens)
4. Copy your API token

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Replicate API token
```

### 4. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /colorize

Colorize a black and white image.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: `file` (image file)

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

## Deployment

### Deploy to Railway.app (Recommended)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variable: `REPLICATE_API_TOKEN`
6. Railway will auto-deploy!

### Deploy to Render.com

1. Go to [Render.com](https://render.com)
2. Create new Web Service
3. Connect your GitHub repository
4. Set:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && python main.py`
5. Add environment variable: `REPLICATE_API_TOKEN`

## Cost

Replicate charges per API call:
- First $5/month free credits
- ~$0.01-0.05 per image colorization
- Perfect for development and small projects