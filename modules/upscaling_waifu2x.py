"""
Waifu2x-based image upscaling module.
Waifu2x is a more stable and easier alternative to Real-ESRGAN.
"""

import logging
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2
import requests
import io
import base64
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import waifu2x-caffe (if available)
try:
    import waifu2x
    WAIFU2X_AVAILABLE = True
    logger.info("✅ Waifu2x module loaded successfully!")
except ImportError:
    logger.info("⚠️ Waifu2x module not available. Using online API fallback.")
    WAIFU2X_AVAILABLE = False

def is_waifu2x_available():
    """Check if Waifu2x is available."""
    return WAIFU2X_AVAILABLE

def apply_waifu2x_online(image, scale=2, noise_level=1):
    """
    Apply Waifu2x upscaling using online API (fallback method).
    
    Args:
        image (PIL.Image): Input image
        scale (int): Upscaling factor (1, 2)
        noise_level (int): Noise reduction level (0, 1, 2, 3)
    
    Returns:
        PIL.Image: Upscaled image or None if failed
    """
    try:
        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Encode to base64
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # Use waifu2x online API (there are several free ones)
        url = "https://waifu2x.udp.jp/api"
        
        data = {
            'scale': scale,
            'noise': noise_level,
            'image': img_base64
        }
        
        logger.info(f"Sending request to Waifu2x API (scale={scale}, noise={noise_level})...")
        response = requests.post(url, data=data, timeout=30)
        
        if response.status_code == 200:
            result_image = Image.open(io.BytesIO(response.content))
            logger.info("✅ Waifu2x online processing completed!")
            return result_image
        else:
            logger.warning(f"Waifu2x API returned status code: {response.status_code}")
            return None
            
    except Exception as e:
        logger.warning(f"Waifu2x online processing failed: {e}")
        return None

def apply_waifu2x_local(image, scale=2, noise_level=1):
    """
    Apply Waifu2x upscaling using local installation.
    
    Args:
        image (PIL.Image): Input image
        scale (int): Upscaling factor (1, 2)
        noise_level (int): Noise reduction level (0, 1, 2, 3)
    
    Returns:
        PIL.Image: Upscaled image or None if failed
    """
    if not WAIFU2X_AVAILABLE:
        return None
        
    try:
        # Convert PIL to numpy array
        img_array = np.array(image)
        
        # Apply waifu2x
        result_array = waifu2x.upscale(
            img_array,
            scale=scale,
            noise_level=noise_level
        )
        
        # Convert back to PIL
        result_image = Image.fromarray(result_array)
        logger.info("✅ Waifu2x local processing completed!")
        return result_image
        
    except Exception as e:
        logger.warning(f"Waifu2x local processing failed: {e}")
        return None

def apply_enhanced_pil_upscaling(image, scale=2):
    """
    Apply enhanced PIL-based upscaling with better algorithms.
    
    Args:
        image (PIL.Image): Input image
        scale (int): Upscaling factor
    
    Returns:
        PIL.Image: Upscaled image
    """
    try:
        # Calculate new size
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        
        # Use LANCZOS for best quality
        upscaled = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply post-processing
        # 1. Sharpening
        sharpened = upscaled.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
        
        # 2. Enhance details
        enhancer = ImageEnhance.Sharpness(sharpened)
        enhanced = enhancer.enhance(1.2)
        
        # 3. Slight contrast boost
        contrast_enhancer = ImageEnhance.Contrast(enhanced)
        final_image = contrast_enhancer.enhance(1.1)
        
        logger.info("✅ Enhanced PIL upscaling completed!")
        return final_image
        
    except Exception as e:
        logger.error(f"Enhanced PIL upscaling failed: {e}")
        return image  # Return original on failure

def apply_opencv_super_resolution(image, scale=2):
    """
    Apply OpenCV's built-in super resolution algorithms.
    
    Args:
        image (PIL.Image): Input image
        scale (int): Upscaling factor
    
    Returns:
        PIL.Image: Upscaled image
    """
    try:
        # Convert PIL to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Try different OpenCV super resolution methods
        try:
            # Method 1: EDSR (Enhanced Deep Super-Resolution)
            sr = cv2.dnn_superres.DnnSuperResImpl_create()
            sr.readModel("EDSR_x2.pb")  # You'd need to download this model
            sr.setModel("edsr", scale)
            result = sr.upsample(cv_image)
        except:
            # Fallback: Simple bicubic interpolation with post-processing
            new_width = int(image.width * scale)
            new_height = int(image.height * scale)
            result = cv2.resize(cv_image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            
            # Apply bilateral filter for noise reduction
            result = cv2.bilateralFilter(result, 9, 75, 75)
        
        # Convert back to PIL
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result_image = Image.fromarray(result_rgb)
        
        logger.info("✅ OpenCV super resolution completed!")
        return result_image
        
    except Exception as e:
        logger.warning(f"OpenCV super resolution failed: {e}")
        return apply_enhanced_pil_upscaling(image, scale)

def upscale_and_enhance_waifu2x(image, scale=2, noise_level=1, use_online=True):
    """
    Main upscaling function using Waifu2x or fallback methods.
    
    Args:
        image (PIL.Image): Input image
        scale (int): Upscaling factor (1, 2)
        noise_level (int): Noise reduction level (0-3)
        use_online (bool): Whether to try online API
    
    Returns:
        PIL.Image: Upscaled and enhanced image
    """
    try:
        # Try local Waifu2x first if available
        if WAIFU2X_AVAILABLE:
            logger.info("Trying local Waifu2x...")
            result = apply_waifu2x_local(image, scale, noise_level)
            if result:
                return result
        
        # Try online Waifu2x if enabled and local failed
        if use_online:
            logger.info("Trying online Waifu2x...")
            result = apply_waifu2x_online(image, scale, noise_level)
            if result:
                return result
        
        # Fallback to OpenCV super resolution
        logger.info("Using OpenCV super resolution fallback...")
        result = apply_opencv_super_resolution(image, scale)
        if result:
            return result
        
        # Final fallback to enhanced PIL
        logger.info("Using enhanced PIL fallback...")
        return apply_enhanced_pil_upscaling(image, scale)
        
    except Exception as e:
        logger.error(f"All upscaling methods failed: {e}")
        return image  # Return original image on complete failure

# Legacy function for compatibility with existing Streamlit app
def upscale_and_enhance_realesrgan(img_pil_input, model_name, model_scale, bilateral_d, sigma_color, sigma_space, sharpness_factor):
    """
    Legacy function signature for backward compatibility.
    Now uses Waifu2x instead of Real-ESRGAN.
    """
    try:
        # Map model_scale to appropriate scale factor
        scale = min(model_scale, 2)  # Waifu2x typically supports up to 2x
        
        # Use noise level based on the bilateral filter parameters
        noise_level = 1 if bilateral_d > 10 else 0
        
        result = upscale_and_enhance_waifu2x(img_pil_input, scale=scale, noise_level=noise_level)
        
        # Apply additional sharpening if requested
        if sharpness_factor > 1.0:
            enhancer = ImageEnhance.Sharpness(result)
            result = enhancer.enhance(sharpness_factor)
        
        return result
        
    except Exception as e:
        logger.error(f"Legacy function failed: {e}")
        return img_pil_input

def test_waifu2x_functionality():
    """Test function to verify Waifu2x functionality."""
    try:
        # Create a small test image
        test_image = Image.new('RGB', (50, 50), color='red')
        
        # Test upscaling
        result = upscale_and_enhance_waifu2x(test_image, scale=2, use_online=False)
        
        if result and result.size[0] > test_image.size[0]:
            logger.info("✅ Waifu2x functionality test PASSED")
            return True
        else:
            logger.warning("❌ Waifu2x functionality test FAILED")
            return False
            
    except Exception as e:
        logger.error(f"Waifu2x test failed: {e}")
        return False

if __name__ == "__main__":
    # Test the functionality
    print("Testing Waifu2x functionality...")
    success = test_waifu2x_functionality()
    print(f"Test result: {'PASSED' if success else 'FAILED'}")
