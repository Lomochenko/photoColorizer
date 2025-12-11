# 🎨 Photo Colorizer - Simple Frontend

A clean, minimal Nuxt 3 frontend that connects to the DeOldify Hugging Face Space for AI-powered photo colorization.

## ✨ Features

- 📸 Drag & drop or click to upload
- 🎯 Adjustable render quality slider
- ⚡ Fast processing (30-60 seconds)
- 🔄 Side-by-side comparison
- 💾 Download colorized images
- 📱 Fully responsive design
- 🎨 Beautiful gradient UI

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend-simple
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

### 3. Open Browser

Visit `http://localhost:3000`

## 🔧 How It Works

This frontend connects to the **leonelhs/deoldify** Hugging Face Space:
- Backend URL: `https://leonelhs-deoldify.hf.space`
- Uses Gradio API for colorization
- No backend setup required!

## 🌐 Deploy

### Deploy to Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

### Deploy to Netlify

1. Connect your GitHub repo
2. Set build command: `npm run generate`
3. Set publish directory: `.output/public`
4. Deploy!

## 📝 File Structure

```
frontend-simple/
├── app.vue           # Main app component (all-in-one)
├── nuxt.config.ts    # Nuxt configuration
├── package.json      # Dependencies
└── README.md         # This file
```

## 🎮 Usage

1. **Upload** a black & white photo
2. **Adjust** the render quality (10-45)
   - Lower = Faster (10-20)
   - Higher = Better Quality (35-45)
3. **Click** "Colorize"
4. **Wait** 30-60 seconds
5. **Download** your colorized photo!

## ⚙️ Customization

### Change Backend URL

Edit `app.vue` line ~139:

```javascript
const response = await fetch('YOUR_BACKEND_URL/api/predict', {
```

### Adjust Colors/Theme

Edit the Tailwind classes in `app.vue`:
- Gradients: `from-purple-600 to-pink-600`
- Background: `from-indigo-100 via-purple-50 to-pink-100`

### Change Render Quality Range

Edit `app.vue` line ~58:

```html
<input v-model.number="renderFactor" type="range" min="10" max="45" />
```

## 🐛 Troubleshooting

### Images not colorizing?

- Check if the Hugging Face Space is running: `https://leonelhs-deoldify.hf.space`
- Try a smaller image (< 5MB)
- Lower the render quality slider

### CORS errors?

- The Hugging Face Gradio API supports CORS by default
- If issues persist, you may need to deploy your own Space

### Slow processing?

- Lower the render quality (10-20 for faster results)
- The Space may be under heavy load - try again later

## 🔗 Links

- Hugging Face Space: https://huggingface.co/spaces/leonelhs/deoldify
- DeOldify Project: https://github.com/jantic/DeOldify
- Nuxt 3 Docs: https://nuxt.com

## 📝 License

MIT License - Feel free to use and modify!

---

Made with ❤️ using Nuxt 3 + Tailwind CSS + Hugging Face
