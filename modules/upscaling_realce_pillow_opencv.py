# Enhanced upscaling and image quality improvement using Pillow and OpenCV
# Salve este arquivo como upscaling_realce_pillow_opencv.py

from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import cv2
import numpy as np
import sys
import os

def upscale_and_enhance(input_path, output_path, scale_factor=4, denoise_size=10, bilateral_d=20, clahe_clip=8.0, saturation_factor=1.2, brightness_factor=1.1):
    """
    Enhanced image upscaling and quality improvement
    
    Args:
        input_path: Path to input image
        output_path: Path to save enhanced image
        scale_factor: Upscaling factor (default: 4)
        denoise_size: Median filter size before upscaling (default: 10)
        bilateral_d: Bilateral filter diameter (default: 20)
        clahe_clip: CLAHE clip limit (default: 8.0)
        saturation_factor: Saturation adjustment factor (default: 1.2)
        brightness_factor: Brightness adjustment factor (default: 1.1)
    """
    
    # Verificar se o arquivo existe
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    # Carregar imagem
    img = Image.open(input_path)
    print(f"Original size: {img.size}")
    
    # Converter para RGB se necessário
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 1. Aplicar filtro de redução de ruído antes do upscaling
    # Ensure denoise_size is odd (MedianFilter requires odd numbers)
    if denoise_size % 2 == 0:
        denoise_size += 1
    img_denoised = img.filter(ImageFilter.MedianFilter(size=denoise_size))
    
    # 2. Upscaling com método mais suave
    new_size = (img.width * scale_factor, img.height * scale_factor)
    img_up = img_denoised.resize(new_size, Image.Resampling.LANCZOS)
    
    # 3. Converter para OpenCV para processamentos avançados
    img_cv = cv2.cvtColor(np.array(img_up), cv2.COLOR_RGB2BGR)
    
    # 4. Aplicar filtro bilateral para reduzir ruído preservando bordas
    img_bilateral = cv2.bilateralFilter(img_cv, bilateral_d, 75, 75)
    
    # 5. Realce de contraste adaptativo (CLAHE)
    lab = cv2.cvtColor(img_bilateral, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Aplicar CLAHE apenas no canal L (luminância)
    clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=(10,10))
    l = clahe.apply(l)
    
    # Recombinar canais
    enhanced_lab = cv2.merge([l, a, b])
    img_enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 6. Aplicar filtro unsharp mask para realce de nitidez
    img_enhanced = apply_unsharp_mask(img_enhanced)
    
    # 7. Ajuste final de saturação e brilho
    img_final = adjust_saturation_brightness(img_enhanced, saturation_factor, brightness_factor)
    
    # Salvar resultado
    cv2.imwrite(output_path, img_final, [cv2.IMWRITE_JPEG_QUALITY, 99])
    print(f"Enhanced image saved: {output_path}")
    print(f"Final size: {img_final.shape[1]}x{img_final.shape[0]}")

def apply_unsharp_mask(image, kernel_size=(1, 1), sigma=2.0, amount=2.5, threshold=0):
    """Aplicar filtro unsharp mask para realce de nitidez"""
    # Criar versão borrada
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    
    # Calcular a máscara unsharp
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    
    # Aplicar threshold se especificado
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    
    return sharpened

def adjust_saturation_brightness(image, saturation_factor=1.2, brightness_factor=1.1):
    """Ajustar saturação e brilho da imagem"""
    # Converter para HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    
    # Ajustar saturação (canal S)
    hsv[:, :, 1] = hsv[:, :, 1] * saturation_factor
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    
    # Ajustar brilho (canal V)
    hsv[:, :, 2] = hsv[:, :, 2] * brightness_factor
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
    
    # Converter de volta para BGR
    enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
    return enhanced

def enhance_with_ai_upscaling(input_path, output_path):
    """
    Versão alternativa usando técnicas mais avançadas
    Requer instalação de opencv-contrib-python para EDSR
    """
    try:
        # Carregar modelo EDSR (requer opencv-contrib-python)
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        
        # Você pode baixar modelos pré-treinados de:
        # https://github.com/Saafke/EDSR_Tensorflow/tree/master/models
        model_path = "EDSR_x4.pb"  # Baixe este modelo
        
        if os.path.exists(model_path):
            sr.readModel(model_path)
            sr.setModel("edsr", 4)
            
            # Carregar e processar imagem
            img = cv2.imread(input_path)
            result = sr.upsample(img)
            
            # Aplicar realces adicionais
            result = apply_unsharp_mask(result)
            result = adjust_saturation_brightness(result)
            
            cv2.imwrite(output_path, result, [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"AI-enhanced image saved: {output_path}")
            return True
        else:
            print("AI model not found, using traditional method")
            return False
            
    except Exception as e:
        print(f"AI enhancement failed: {e}")
        return False

def upscale_and_enhance_pil(input_image, scale_factor=4, denoise_size=10, bilateral_d=20, clahe_clip=8.0, saturation_factor=1.2, brightness_factor=1.1):
    """
    Enhanced image upscaling and quality improvement for PIL Images
    
    Args:
        input_image: PIL Image object
        scale_factor: Upscaling factor (default: 4)
        denoise_size: Median filter size before upscaling (default: 10)
        bilateral_d: Bilateral filter diameter (default: 20)
        clahe_clip: CLAHE clip limit (default: 8.0)
        saturation_factor: Saturation adjustment factor (default: 1.2)
        brightness_factor: Brightness adjustment factor (default: 1.1)
    
    Returns:
        PIL Image object with enhancements applied
    """
    try:
        img = input_image.copy()
        print(f"Original size: {img.size}")
        
        # Converter para RGB se necessário
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 1. Aplicar filtro de redução de ruído antes do upscaling
        # Ensure denoise_size is odd (MedianFilter requires odd numbers)
        if denoise_size % 2 == 0:
            denoise_size += 1
        img_denoised = img.filter(ImageFilter.MedianFilter(size=denoise_size))
        
        # 2. Upscaling com método mais suave
        new_size = (img.width * scale_factor, img.height * scale_factor)
        img_up = img_denoised.resize(new_size, Image.Resampling.LANCZOS)
        
        # 3. Converter para OpenCV para processamentos avançados
        img_cv = cv2.cvtColor(np.array(img_up), cv2.COLOR_RGB2BGR)
        
        # 4. Aplicar filtro bilateral para reduzir ruído preservando bordas
        img_bilateral = cv2.bilateralFilter(img_cv, bilateral_d, 80, 80)
        
        # 5. Converter de volta para PIL para ajustes de cor
        img_pil = Image.fromarray(cv2.cvtColor(img_bilateral, cv2.COLOR_BGR2RGB))
        
        # 6. Aplicar CLAHE (Contrast Limited Adaptive Histogram Equalization)
        img_cv_clahe = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(img_cv_clahe)
        clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=(8,8))
        l = clahe.apply(l)
        img_cv_clahe = cv2.merge([l, a, b])
        img_clahe = Image.fromarray(cv2.cvtColor(img_cv_clahe, cv2.COLOR_LAB2RGB))
        
        # 7. Ajustar saturação
        enhancer = ImageEnhance.Color(img_clahe)
        img_saturated = enhancer.enhance(saturation_factor)
        
        # 8. Ajustar brilho
        enhancer = ImageEnhance.Brightness(img_saturated)
        img_bright = enhancer.enhance(brightness_factor)
        
        # 9. Aplicar nitidez moderada
        enhancer = ImageEnhance.Sharpness(img_bright)
        img_final = enhancer.enhance(1.3)
        
        print(f"Enhanced size: {img_final.size}")
        return img_final
        
    except Exception as e:
        print(f"Error in upscale_and_enhance_pil: {e}")
        return input_image  # Return original on error

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python upscaling_realce_pillow_opencv.py <input.jpg> <output.jpg> [scale_factor]")
        print("Exemplo: python upscaling_realce_pillow_opencv.py input.jpg output.jpg 4")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    scale = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    
    try:
        # Tentar método com AI primeiro
        if not enhance_with_ai_upscaling(input_file, output_file):
            # Fallback para método tradicional melhorado
            upscale_and_enhance(input_file, output_file, scale)
            
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
