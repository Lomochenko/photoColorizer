import os
import time
import asyncio
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from colorizer import PhotoColorizer
from utils import save_upload_file, cleanup_file, validate_image_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global colorizer instance
colorizer: Optional[PhotoColorizer] = None

# Pydantic models
class ColorizationRequest(BaseModel):
    intensity: float = 100.0
    contrast: float = 0.0
    saturation: float = 100.0
    temperature: float = 0.0

class ColorizationResponse(BaseModel):
    success: bool
    image: Optional[str] = None
    error: Optional[str] = None
    dimensions: Optional[Dict[str, int]] = None
    processing_time: Optional[float] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global colorizer
    
    # Startup
    logger.info("Starting PhotoColorizer API...")
    try:
        colorizer = PhotoColorizer()
        await colorizer.load_models()
        logger.info("Models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load models: {e}")
        colorizer = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down PhotoColorizer API...")
    if colorizer:
        await colorizer.cleanup()

# Create FastAPI app
app = FastAPI(
    title="PhotoColorizer API",
    description="AI-powered black and white photo colorization",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_loaded=colorizer is not None,
        version="1.0.0"
    )

@app.post("/colorize", response_model=ColorizationResponse)
async def colorize_photo(
    file: UploadFile = File(...),
    intensity: float = Form(100.0),
    contrast: float = Form(0.0),
    saturation: float = Form(100.0),
    temperature: float = Form(0.0)
):
    """Colorize a black and white photo"""
    
    if not colorizer:
        raise HTTPException(
            status_code=503,
            detail="Colorization model not available"
        )
    
    start_time = time.time()
    temp_input_path = None
    temp_output_path = None
    
    try:
        # Validate input file
        await validate_image_file(file)
        
        # Save uploaded file
        temp_input_path = await save_upload_file(file)
        temp_output_path = temp_input_path.replace('.jpg', '_colorized.jpg')
        
        # Prepare parameters
        params = {
            'intensity': intensity,
            'contrast': contrast,
            'saturation': saturation,
            'temperature': temperature
        }
        
        # Process image
        result = await colorizer.colorize(temp_input_path, temp_output_path, params)
        
        # Read result image
        with open(temp_output_path, 'rb') as f:
            image_data = f.read()
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Convert to base64
        import base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        return ColorizationResponse(
            success=True,
            image=image_base64,
            dimensions=result['dimensions'],
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Colorization error: {e}")
        return ColorizationResponse(
            success=False,
            error=str(e)
        )
        
    finally:
        # Cleanup temporary files
        if temp_input_path:
            await cleanup_file(temp_input_path)
        if temp_output_path:
            await cleanup_file(temp_output_path)

@app.get("/models")
async def list_models():
    """List available colorization models"""
    if not colorizer:
        raise HTTPException(
            status_code=503,
            detail="Colorization model not available"
        )
    
    return {
        "models": colorizer.get_available_models()
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PhotoColorizer API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=4
    )