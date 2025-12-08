# ⚡ Quick Start Guide - Get Running in 5 Minutes!

## Step 1: Get Replicate API Token (2 minutes)

1. Go to https://replicate.com
2. Click "Sign up" (use GitHub for quick signup)
3. Go to https://replicate.com/account/api-tokens
4. Copy your API token (starts with `r8_...`)
5. **Keep it safe!** You'll need it in Step 3

💵 **Free Credits**: You get $5/month free - enough for 100-500 colorizations!

---

## Step 2: Clone & Install (1 minute)

```bash
# Clone the repository
git clone https://github.com/Lomochenko/photoColorizer.git
cd photoColorizer
```

---

## Step 3: Setup Backend (1 minute)

```bash
# Go to backend folder
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Create .env file with your token
echo "REPLICATE_API_TOKEN=your_token_here" > .env
echo "PORT=8000" >> .env

# Replace 'your_token_here' with your actual token from Step 1!
# You can edit .env with any text editor
```

**For Windows users:**
```bash
echo REPLICATE_API_TOKEN=your_token_here > .env
echo PORT=8000 >> .env
```

---

## Step 4: Setup Frontend (1 minute)

```bash
# Open a NEW terminal/command prompt
cd frontend

# Install Node dependencies
npm install

# Create .env file
cp .env.example .env
# No need to edit this one - it uses localhost by default
```

---

## Step 5: Run Everything! (30 seconds)

### Terminal 1 - Backend:
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

You should see:
```
Nuxt 3.x.x with Nitro 2.x.x
➜ Local:   http://localhost:3000/
```

---

## Step 6: Test It! 🎉

1. Open your browser: http://localhost:3000
2. Drag & drop a black & white photo
3. Click "Colorize Image"
4. Wait 30-60 seconds for AI magic ✨
5. Download your colorized photo!

---

## 🐛 Troubleshooting

### "REPLICATE_API_TOKEN not set"
- Make sure you created the `.env` file in the `backend` folder
- Check that your token starts with `r8_`
- No quotes needed around the token

### Backend won't start
```bash
# Make sure you're in the backend folder
cd backend

# Try installing dependencies again
pip install -r requirements.txt --upgrade
```

### Frontend won't start
```bash
# Make sure you're in the frontend folder
cd frontend

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### "Port already in use"
- Change the port in `backend/.env`: `PORT=8001`
- Or kill the process using that port

### Images not colorizing
- Check backend is running (Terminal 1)
- Check backend logs for errors
- Try a different image (smaller file size)
- Make sure your Replicate API token is valid

---

## 🚀 Next Steps

### Deploy to Production

See [README.md](README.md) for deployment guides:
- Backend: Deploy to Railway.app (5 minutes)
- Frontend: Deploy to Vercel.com (3 minutes)

### Customize

- Change colors in `frontend/tailwind.config.js`
- Modify AI parameters in `backend/main.py`
- Add more features!

---

## 🎓 Learning Resources

- **DeOldify Model**: https://github.com/jantic/DeOldify
- **Replicate API Docs**: https://replicate.com/docs
- **Nuxt 3 Docs**: https://nuxt.com
- **FastAPI Docs**: https://fastapi.tiangolo.com

---

## 👋 Need Help?

Open an issue on GitHub with:
1. Error message
2. What step you're on
3. Your operating system

Happy colorizing! 🎨
