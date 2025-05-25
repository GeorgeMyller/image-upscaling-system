"""
Unified Image Upscaling with Multiple AI Models
Provides a simple interface for various upscaling methods
"""

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnifiedUpscaler:
    """Unified interface for multiple upscaling methods"""
    
    def __init__(self):
        self.available_methods = self._check_available_methods()
        logger.info(f"Available upscaling methods: {list(self.available_methods.keys())}")
    
    def _check_available_methods(self):
        """Check which upscaling methods are available"""
        methods = {}
        
        # Check upscalers package
        try:
            import upscalers
            methods['upscalers'] = upscalers
            logger.info("✅ upscalers package available")
        except ImportError:
            logger.warning("❌ upscalers package not available")
        
        # Check opencv for classical methods
        try:
            import cv2
            methods['opencv'] = cv2
            logger.info("✅ OpenCV available")
        except ImportError:
            logger.warning("❌ OpenCV not available")
        
        # Check PIL (always available)
        methods['pil'] = Image
        logger.info("✅ PIL available")
        
        # Check tensorflow for AI methods
        try:
            import tensorflow as tf
            methods['tensorflow'] = tf
            logger.info("✅ TensorFlow available")
        except ImportError:
            logger.warning("❌ TensorFlow not available")
        
        return methods
    
    def list_available_models(self):
        """List all available upscaling models"""
        models = {}
        
        if 'upscalers' in self.available_methods:
            try:
                import upscalers
                models['AI Models (upscalers)'] = upscalers.list_upscalers()
            except Exception as e:
                logger.error(f"Error listing upscalers models: {e}")
        
        if 'opencv' in self.available_methods:
            models['Classical (OpenCV)'] = ['LANCZOS', 'CUBIC', 'LINEAR', 'AREA', 'INTER_NEAREST']
        
        models['Classical (PIL)'] = ['LANCZOS', 'BICUBIC', 'BILINEAR', 'NEAREST']
        
        return models
    
    def upscale_with_ai(self, image, scale_factor=2.0, model_name=None):
        """Upscale using AI models from upscalers package"""
        if 'upscalers' not in self.available_methods:
            raise ValueError("upscalers package not available")
        
        try:
            import upscalers
            
            # Get available models if none specified
            if model_name is None:
                available_models = upscalers.list_upscalers()
                if not available_models:
                    raise ValueError("No upscaling models available")
                
                # Prefer R-ESRGAN or ESRGAN models
                preferred_models = [m for m in available_models if 'ESRGAN' in m.upper()]
                if preferred_models:
                    model_name = preferred_models[0]
                else:
                    model_name = available_models[0]
            
            logger.info(f"Using AI model: {model_name}")
            result = upscalers.upscale(model_name, image, scale_factor)
            
            return result, f"AI upscaling with {model_name}"
            
        except Exception as e:
            logger.error(f"AI upscaling failed: {e}")
            raise
    
    def upscale_with_opencv(self, image, scale_factor=2.0, method='LANCZOS'):
        """Upscale using OpenCV interpolation methods"""
        if 'opencv' not in self.available_methods:
            raise ValueError("OpenCV not available")
        
        try:
            import cv2
            
            # Convert PIL to OpenCV format
            if isinstance(image, Image.Image):
                image_array = np.array(image)
            else:
                image_array = image
            
            # Get new dimensions
            height, width = image_array.shape[:2]
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            # Choose interpolation method
            interpolation_methods = {
                'LANCZOS': cv2.INTER_LANCZOS4,
                'CUBIC': cv2.INTER_CUBIC,
                'LINEAR': cv2.INTER_LINEAR,
                'AREA': cv2.INTER_AREA,
                'INTER_NEAREST': cv2.INTER_NEAREST
            }
            
            interp = interpolation_methods.get(method, cv2.INTER_LANCZOS4)
            
            # Upscale
            upscaled = cv2.resize(image_array, (new_width, new_height), interpolation=interp)
            
            # Convert back to PIL
            result = Image.fromarray(upscaled)
            
            # Apply post-processing
            result = self._post_process_image(result)
            
            return result, f"OpenCV upscaling with {method}"
            
        except Exception as e:
            logger.error(f"OpenCV upscaling failed: {e}")
            raise
    
    def upscale_with_pil(self, image, scale_factor=2.0, method='LANCZOS'):
        """Upscale using PIL resampling methods"""
        try:
            # Get new dimensions
            width, height = image.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            
            # Choose resampling method
            resampling_methods = {
                'LANCZOS': Image.LANCZOS,
                'BICUBIC': Image.BICUBIC,
                'BILINEAR': Image.BILINEAR,
                'NEAREST': Image.NEAREST
            }
            
            resample = resampling_methods.get(method, Image.LANCZOS)
            
            # Upscale
            result = image.resize((new_width, new_height), resample)
            
            # Apply post-processing
            result = self._post_process_image(result)
            
            return result, f"PIL upscaling with {method}"
            
        except Exception as e:
            logger.error(f"PIL upscaling failed: {e}")
            raise
    
    def _post_process_image(self, image):
        """Apply post-processing to enhance image quality"""
        try:
            # Apply slight sharpening
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            # Apply slight contrast enhancement
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.05)
            
            return image
        except Exception as e:
            logger.warning(f"Post-processing failed: {e}")
            return image
    
    def upscale_smart(self, image, scale_factor=2.0, method='auto'):
        """Smart upscaling that tries the best available method"""
        methods_to_try = []
        
        if method == 'auto':
            # Try methods in order of preference
            if 'upscalers' in self.available_methods:
                methods_to_try.append(('ai', None))
            if 'opencv' in self.available_methods:
                methods_to_try.append(('opencv', 'LANCZOS'))
            methods_to_try.append(('pil', 'LANCZOS'))
        else:
            methods_to_try.append((method, None))
        
        last_error = None
        
        for method_type, method_param in methods_to_try:
            try:
                if method_type == 'ai':
                    return self.upscale_with_ai(image, scale_factor, method_param)
                elif method_type == 'opencv':
                    return self.upscale_with_opencv(image, scale_factor, method_param or 'LANCZOS')
                elif method_type == 'pil':
                    return self.upscale_with_pil(image, scale_factor, method_param or 'LANCZOS')
            except Exception as e:
                last_error = e
                logger.warning(f"Method {method_type} failed: {e}")
                continue
        
        raise Exception(f"All upscaling methods failed. Last error: {last_error}")

# Legacy function for compatibility
def upscale_image(image_path, output_path=None, scale_factor=2.0, method='auto'):
    """Legacy function for backward compatibility"""
    upscaler = UnifiedUpscaler()
    
    # Load image
    if isinstance(image_path, str):
        image = Image.open(image_path)
    else:
        image = image_path
    
    # Upscale
    result, method_used = upscaler.upscale_smart(image, scale_factor, method)
    
    # Save if output path provided
    if output_path:
        result.save(output_path)
        logger.info(f"Upscaled image saved to: {output_path}")
    
    return result, method_used

def test_all_methods():
    """Test all available upscaling methods"""
    logger.info("Testing all upscaling methods...")
    
    # Create a test image
    test_image = Image.new('RGB', (100, 100), color='red')
    
    upscaler = UnifiedUpscaler()
    
    # Test available models
    logger.info("Available models:")
    models = upscaler.list_available_models()
    for category, model_list in models.items():
        logger.info(f"  {category}: {model_list}")
    
    # Test smart upscaling
    try:
        result, method = upscaler.upscale_smart(test_image, 2.0)
        logger.info(f"✅ Smart upscaling successful: {method}")
        logger.info(f"  Original size: {test_image.size}")
        logger.info(f"  Upscaled size: {result.size}")
    except Exception as e:
        logger.error(f"❌ Smart upscaling failed: {e}")

if __name__ == "__main__":
    test_all_methods()
