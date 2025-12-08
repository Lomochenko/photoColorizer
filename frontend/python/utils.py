import os
import uuid
import time
from typing import Optional
from pathlib import Path
from fastapi import UploadFile, HTTPException
import aiofiles

# Constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
UPLOAD_DIR = "uploads"

def ensure_upload_dir():
    """Ensure upload directory exists"""
    Path(UPLOAD_DIR).mkdir(exist_ok=True)

async def validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file"""
    
    # Check if file is provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file size
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413, 
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Check MIME type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an image file."
        )

async def save_upload_file(file: UploadFile, prefix: str = "input") -> str:
    """Save uploaded file and return file path"""
    
    ensure_upload_dir()
    
    # Generate unique filename
    file_id = uuid.uuid4().hex
    file_ext = Path(file.filename).suffix.lower()
    filename = f"{prefix}_{file_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return file_path

async def cleanup_file(file_path: str) -> None:
    """Clean up temporary file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Failed to cleanup file {file_path}: {e}")

def get_file_size(file_path: str) -> int:
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0

def is_valid_image_path(file_path: str) -> bool:
    """Check if path is a valid image file"""
    try:
        if not os.path.exists(file_path):
            return False
        
        file_ext = Path(file_path).suffix.lower()
        return file_ext in ALLOWED_EXTENSIONS
    except Exception:
        return False

async def cleanup_old_files(directory: str = UPLOAD_DIR, max_age_hours: int = 24) -> int:
    """Clean up old files in directory"""
    
    cleaned_count = 0
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                file_age = current_time - os.path.getmtime(file_path)
                
                if file_age > max_age_seconds:
                    await cleanup_file(file_path)
                    cleaned_count += 1
                    
    except Exception as e:
        print(f"Error during cleanup: {e}")
    
    return cleaned_count

# Export functions
__all__ = [
    'validate_image_file',
    'save_upload_file', 
    'cleanup_file',
    'get_file_size',
    'is_valid_image_path',
    'cleanup_old_files',
    'MAX_FILE_SIZE',
    'ALLOWED_EXTENSIONS'
]