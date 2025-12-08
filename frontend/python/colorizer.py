import os
import cv2
import numpy as np
import asyncio
from typing import Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class PhotoColorizer:
    """Photo colorization using OpenCV DNN and Caffe model"""
    
    def __init__(self):
        self.net = None
        self.pts_in_hull = None
        self.model_loaded = False
        
        # Model file paths
        self.prototxt_path = "models/colorization_deploy_v2.prototxt"
        self.model_path = "models/colorization_release_v2.caffemodel"
        self.kernel_path = "models/pts_in_hull.npy"
    
    async def load_models(self) -> bool:
        """Load the colorization models"""
        try:
            # Check if model files exist
            if not all(os.path.exists(path) for path in [
                self.prototxt_path, 
                self.model_path, 
                self.kernel_path
            ]):
                logger.error("Model files not found")
                return False
            
            # Load the DNN model
            self.net = cv2.dnn.readNetFromCaffe(self.prototxt_path, self.model_path)
            
            # Load cluster centers
            self.pts_in_hull = np.load(self.kernel_path)
            
            # Configure the model
            self._configure_model()
            
            self.model_loaded = True
            logger.info("Colorization models loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            return False
    
    def _configure_model(self):
        """Configure the colorization model"""
        if self.net is None or self.pts_in_hull is None:
            raise RuntimeError("Models not loaded")
        
        # Populate cluster centers as 1x1 convolutions
        pts_in_hull = self.pts_in_hull.transpose().reshape(2, 313, 1, 1)
        
        # Get layer IDs
        class8_layer_id = self.net.getLayerId("class8_ab")
        conv8_layer_id = self.net.getLayerId("conv8_313_rh")
        
        # Set the layer weights
        self.net.getLayer(class8_layer_id).blobs = [pts_in_hull.astype("float32")]
        self.net.getLayer(conv8_layer_id).blobs = [np.full([1, 313], 2.606, dtype="float32")]
    
    async def colorize(self, input_path: str, output_path: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Colorize a black and white image"""
        
        if not self.model_loaded:
            raise RuntimeError("Models not loaded")
        
        try:
            # Read the input image
            image = cv2.imread(input_path)
            if image is None:
                raise ValueError(f"Cannot read image from {input_path}")
            
            # Get original dimensions
            orig_height, orig_width = image.shape[:2]
            
            # Convert BGR to RGB
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Scale to [0, 1]
            image_rgb = image_rgb.astype("float32") / 255.0
            
            # Convert to Lab color space
            image_lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2Lab)
            
            # Extract L channel
            image_l = image_lab[:, :, 0]
            
            # Resize to network input size (224x224)
            image_rs = cv2.resize(image_rgb, (224, 224))
            image_lab_rs = cv2.cvtColor(image_rs, cv2.COLOR_RGB2Lab)
            image_l_rs = image_lab_rs[:, :, 0]
            
            # Mean subtraction
            image_l_rs -= 50
            
            # Run the model
            self.net.setInput(cv2.dnn.blobFromImage(image_l_rs))
            ab_dec = self.net.forward("class8_ab")[0, :, :, :].transpose((1, 2, 0))
            
            # Resize the predicted 'ab' volume to original size
            ab_dec_us = cv2.resize(ab_dec, (orig_width, orig_height))
            
            # Concatenate with original L channel
            image_lab_out = np.concatenate((image_l[:, :, np.newaxis], ab_dec_us), axis=2)
            
            # Convert back to BGR
            image_bgr_out = cv2.cvtColor(image_lab_out, cv2.COLOR_Lab2BGR)
            image_bgr_out = np.clip(image_bgr_out, 0, 1)
            
            # Apply post-processing parameters
            image_bgr_out = self._apply_post_processing(image_bgr_out, parameters)
            
            # Convert to 8-bit and save
            image_bgr_out = (255 * image_bgr_out).astype("uint8")
            cv2.imwrite(output_path, image_bgr_out)
            
            return {
                "success": True,
                "dimensions": {
                    "width": orig_width,
                    "height": orig_height
                }
            }
            
        except Exception as e:
            logger.error(f"Colorization error: {e}")
            raise RuntimeError(f"Failed to colorize image: {e}")
    
    def _apply_post_processing(self, image: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        """Apply post-processing effects"""
        
        # Convert to HSV for easier manipulation
        image_hsv = cv2.cvtColor(image.astype("float32"), cv2.COLOR_BGR2HSV)
        
        # Apply intensity (brightness)
        intensity_factor = parameters.get('intensity', 100) / 100.0
        image_hsv[:, :, 2] = np.clip(image_hsv[:, :, 2] * intensity_factor, 0, 1)
        
        # Apply saturation
        saturation_factor = parameters.get('saturation', 100) / 100.0
        image_hsv[:, :, 1] = np.clip(image_hsv[:, :, 1] * saturation_factor, 0, 1)
        
        # Apply contrast (using value channel)
        contrast_factor = parameters.get('contrast', 0) / 100.0
        if contrast_factor != 0:
            # Simple contrast adjustment
            image_hsv[:, :, 2] = np.clip(
                image_hsv[:, :, 2] * (1 + contrast_factor), 
                0, 1
            )
        
        # Apply temperature (hue shift)
        temperature_factor = parameters.get('temperature', 0) / 100.0
        if temperature_factor != 0:
            # Shift hue (0.5 corresponds to 180 degrees)
            hue_shift = temperature_factor * 0.1  # Adjust range as needed
            image_hsv[:, :, 0] = (image_hsv[:, :, 0] + hue_shift) % 1.0
        
        # Convert back to BGR
        image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)
        
        return image_bgr
    
    def get_available_models(self) -> list:
        """Get list of available colorization models"""
        return [
            {
                "name": "Caffe Colorization",
                "version": "v2",
                "description": "Original Caffe model for image colorization",
                "loaded": self.model_loaded
            }
        ]
    
    async def cleanup(self):
        """Cleanup resources"""
        self.net = None
        self.pts_in_hull = None
        self.model_loaded = False
        logger.info("Colorizer resources cleaned up")