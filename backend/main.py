from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import replicate
import os
import base64
import requests
from io import BytesIO
from PIL import Image
import tempfile

app = FastAPI(title="Photo Colorizer API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check for Replicate API token
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    print("WARNING: REPLICATE_API_TOKEN not set!")

@app.get("/")
async def root():
    return {
        "message": "Photo Colorizer API",
        "status": "running",
        "endpoints": {
            "/colorize": "POST - Upload image to colorize",
            "/health": "GET - Health check"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "replicate_configured": bool(REPLICATE_API_TOKEN),
        "model": "deoldify"
    }

@app.post("/colorize")
async def colorize_image(file: UploadFile = File(...)):
    """
    Colorize an uploaded black and white image using Replicate's DeOldify model
    """
    try:
        # Validate API token
        if not REPLICATE_API_TOKEN:
            raise HTTPException(
                status_code=500,
                detail="Replicate API token not configured. Please set REPLICATE_API_TOKEN environment variable."
            )
        
        # Read and validate image
        contents = await file.read()
        
        # Validate image format
        try:
            image = Image.open(BytesIO(contents))
            image.verify()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
        
        # Convert image to base64
        image = Image.open(BytesIO(contents))
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
            image.save(tmp.name, format='JPEG')
            tmp_path = tmp.name
        
        # Read as bytes for base64 encoding
        with open(tmp_path, 'rb') as f:
            image_bytes = f.read()
        
        # Encode to base64
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{image_data}"
        
        # Clean up temp file
        os.unlink(tmp_path)
        
        # Run the model on Replicate
        output = replicate.run(
            "nightmareai/real-esrgan:42fd1c5bb58de8b7b09695a283f4f9ee58dcfc580d51dcc6a1e3423e89e55ee8",
            input={
                "image": image_uri,
                "scale": 2,
                "face_enhance": False
            }
        )
        
        # Alternative: Use DeOldify model directly
        # output = replicate.run(
        #     "cjwbw/deoldify:7045c2d9e1caf35f38d8a4a9a4d8aabecd3e2ef5f0e1e3c2fb2c8e4a4a4a4a4",
        #     input={"image": image_uri}
        # )
        
        # Get the output image URL
        if isinstance(output, str):
            output_url = output
        elif isinstance(output, list) and len(output) > 0:
            output_url = output[0]
        else:
            raise HTTPException(status_code=500, detail="Unexpected output format from model")
        
        # Download the colorized image
        response = requests.get(output_url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to download colorized image")
        
        # Convert to base64 for response
        colorized_base64 = base64.b64encode(response.content).decode('utf-8')
        
        return JSONResponse(content={
            "success": True,
            "colorized_image": f"data:image/jpeg;base64,{colorized_base64}",
            "message": "Image colorized successfully"
        })
        
    except replicate.exceptions.ReplicateError as e:
        raise HTTPException(status_code=500, detail=f"Replicate API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)