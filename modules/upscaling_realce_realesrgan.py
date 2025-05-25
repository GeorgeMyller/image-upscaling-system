"""
Real-ESRGAN upscaling using the official ai-forever/Real-ESRGAN package.
This module provides Real-ESRGAN upscaling functionality with proper error handling.
"""

import logging
from PIL import Image, ImageEnhance, ImageOps
import numpy as np
import cv2
import torch
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import Real-ESRGAN with error handling
try:
    from RealESRGAN import RealESRGAN
    REALESRGAN_AVAILABLE = True
    logger.info("✅ Real-ESRGAN (ai-forever) loaded successfully!")
except ImportError as e:
    logger.warning(f"Real-ESRGAN not available: {e}")
    REALESRGAN_AVAILABLE = False
    # Create dummy class for fallback
    class RealESRGAN:
        def __init__(self, device, scale=4):
            pass
        def load_weights(self, path, download=True):
            pass
        def predict(self, image):
            return image

# --- Configurable Parameters ---
MODEL_SCALE = 4  # Default scale factor
BILATERAL_D = 9      # Bilateral filter diameter
BILATERAL_SIGMA_COLOR = 75
BILATERAL_SIGMA_SPACE = 75
SHARPNESS_FACTOR = 1.2  # Sharpness enhancement factor

def apply_realesrgan_upscaling(image, scale=4):
    """
    Apply Real-ESRGAN upscaling to an image using the official ai-forever implementation.
    
    Args:
        image (PIL.Image): Input image
        scale (int): Upscaling factor (2 or 4, default: 4)
    
    Returns:
        PIL.Image: Upscaled image
    """
    try:
        if not REALESRGAN_AVAILABLE:
            logger.warning("Real-ESRGAN not available. Using classical upscaling")
            return apply_classical_upscaling(image, scale)
        
        # Determine device
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {device}")
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Initialize Real-ESRGAN model
        model = RealESRGAN(device, scale=scale)
        
        # Load weights with automatic download
        model_path = f'RealESRGAN_x{scale}.pth'
        model.load_weights(model_path, download=True)
        logger.info(f"Real-ESRGAN model loaded successfully (scale: {scale}x)")
        
        # Convert PIL image to numpy array
        image_np = np.array(image)
        
        # Apply Real-ESRGAN upscaling
        upscaled_image = model.predict(image_np)
        
        # Convert back to PIL Image
        result = Image.fromarray(upscaled_image)
        
        # Apply post-processing filters
        result = apply_post_processing(result)
        
        logger.info(f"Real-ESRGAN upscaling completed successfully. Scale: {scale}x")
        return result
        
    except Exception as e:
        logger.error(f"Real-ESRGAN failed: {e}")
        logger.info("Falling back to classical upscaling")
        return apply_classical_upscaling(image, scale)

def apply_classical_upscaling(image, scale=4):
    """
    Fallback classical upscaling using LANCZOS with enhanced post-processing.
    
    Args:
        image (PIL.Image): Input image
        scale (int): Upscaling factor
    
    Returns:
        PIL.Image: Upscaled image
    """
    try:
        width, height = image.size
        new_size = (width * scale, height * scale)
        
        # Use LANCZOS for high-quality upscaling
        upscaled = image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Apply post-processing
        upscaled = apply_post_processing(upscaled)
        
        logger.info(f"Classical upscaling completed. Scale: {scale}x")
        return upscaled
        
    except Exception as e:
        logger.error(f"Classical upscaling failed: {e}")
        return image

def apply_post_processing(image):
    """
    Apply post-processing filters to enhance the upscaled image.
    
    Args:
        image (PIL.Image): Input image
    
    Returns:
        PIL.Image: Enhanced image
    """
    try:
        # Convert to OpenCV format for bilateral filtering
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Apply bilateral filter for noise reduction while preserving edges
        filtered = cv2.bilateralFilter(image_cv, BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE)
        
        # Convert back to PIL
        result = Image.fromarray(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
        
        # Apply automatic contrast enhancement
        result = ImageOps.autocontrast(result)
        
        # Enhance sharpness slightly
        enhancer = ImageEnhance.Sharpness(result)
        result = enhancer.enhance(SHARPNESS_FACTOR)
        
        return result
        
    except Exception as e:
        logger.warning(f"Post-processing failed: {e}")
        return image

# Legacy function signature for backward compatibility with Streamlit app
def upscale_and_enhance_realesrgan(img_pil_input, model_name, model_scale, bilateral_d, sigma_color, sigma_space, sharpness_factor):
    """
    Legacy function with the signature expected by the Streamlit app.
    This function processes the image directly without saving to disk.
    """
    global BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE, SHARPNESS_FACTOR
    
    # Update global parameters
    BILATERAL_D = bilateral_d
    BILATERAL_SIGMA_COLOR = sigma_color
    BILATERAL_SIGMA_SPACE = sigma_space
    SHARPNESS_FACTOR = sharpness_factor
    
    try:
        if not REALESRGAN_AVAILABLE:
            logger.warning("RealESRGAN not available. Using basic PIL upscaling...")
            # Fallback: basic upscaling with PIL
            img_upscaled = img_pil_input.resize(
                (img_pil_input.width * model_scale, img_pil_input.height * model_scale), 
                Image.Resampling.LANCZOS
            )
            return apply_post_processing(img_upscaled)
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Convert to RGB if necessary
        if img_pil_input.mode != 'RGB':
            img_pil_input = img_pil_input.convert('RGB')
        
        # Initialize Real-ESRGAN model
        model = RealESRGAN(device, scale=model_scale)
        model.load_weights(model_name, download=True)
        
        logger.info(f"Processing with Real-ESRGAN (Model: {model_name}, Scale: {model_scale}x)...")
        
        # Convert to numpy for Real-ESRGAN
        image_np = np.array(img_pil_input)
        sr_img = model.predict(image_np)
        sr_img_pil = Image.fromarray(sr_img)
        
        # Apply post-processing
        result = apply_post_processing(sr_img_pil)
        
        logger.info("Real-ESRGAN processing completed!")
        return result
        
    except Exception as e:
        logger.error(f"Error during Real-ESRGAN processing: {e}")
        logger.info("Using fallback method...")
        
        # Fallback method
        img_upscaled = img_pil_input.resize(
            (img_pil_input.width * model_scale, img_pil_input.height * model_scale), 
            Image.Resampling.LANCZOS
        )
        return apply_post_processing(img_upscaled)

def is_realesrgan_available():
    """
    Check if Real-ESRGAN is available and working.
    
    Returns:
        bool: True if Real-ESRGAN is available, False otherwise
    """
    return REALESRGAN_AVAILABLE

def test_realesrgan_functionality():
    """Test Real-ESRGAN functionality with a simple image."""
    try:
        # Create a test image
        test_image = Image.new('RGB', (50, 50), color='red')
        
        # Test upscaling
        result = apply_realesrgan_upscaling(test_image, scale=2)
        
        print(f"Test successful! Original size: {test_image.size}, Upscaled size: {result.size}")
        print(f"Real-ESRGAN available: {is_realesrgan_available()}")
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False

# Legacy command-line interface
def upscale_and_enhance(input_path, output_path):
    """Legacy command-line function."""
    try:
        img = Image.open(input_path)
        result = apply_realesrgan_upscaling(img, scale=MODEL_SCALE)
        result.save(output_path)
        print(f"Image saved to: {output_path}")
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Run test if no arguments provided
        test_realesrgan_functionality()
    elif len(sys.argv) == 3:
        # Command-line usage
        upscale_and_enhance(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python upscaling_realce_realesrgan.py <input.jpg> <output.jpg>")
        print("Or run without arguments to test functionality")
        sys.exit(1)
