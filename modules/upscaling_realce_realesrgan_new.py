#!/usr/bin/env python3
"""
Upscaling com Real-ESRGAN usando ai-forever/Real-ESRGAN
Este módulo implementa upscaling de imagens usando o modelo Real-ESRGAN oficial.
"""

from PIL import Image, ImageEnhance, ImageOps
import cv2
import numpy as np
import torch
import sys
import os

# Try to import RealESRGAN with error handling
try:
    from RealESRGAN import RealESRGAN
    REALESRGAN_AVAILABLE = True
    print("✅ Real-ESRGAN (ai-forever) carregado com sucesso!")
except ImportError as e:
    print(f"Warning: RealESRGAN not available: {e}")
    REALESRGAN_AVAILABLE = False
    # Create dummy class for fallback
    class RealESRGAN:
        def __init__(self, device, scale=4):
            pass
        def load_weights(self, path, download=True):
            pass
        def predict(self, image):
            return image

# --- Parâmetros Configuráveis ---
MODEL_SCALE = 4  # Escala padrão
BILATERAL_D = 9
BILATERAL_SIGMA_COLOR = 75
BILATERAL_SIGMA_SPACE = 75
SHARPNESS_FACTOR = 1.5

def upscale_and_enhance_realesrgan(input_image, scale=4, apply_post_processing=True):
    """
    Aplica upscaling usando Real-ESRGAN e pós-processamento.
    
    Args:
        input_image: PIL Image object
        scale: int, fator de escala (padrão: 4)
        apply_post_processing: bool, aplicar pós-processamento
        
    Returns:
        PIL Image object processada
    """
    if not REALESRGAN_AVAILABLE:
        print("Real-ESRGAN não disponível. Usando upscaling básico...")
        return fallback_upscale(input_image, scale)
    
    try:
        # Inicializar modelo
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = RealESRGAN(device, scale=scale)
        
        # Carregar pesos do modelo (download automático)
        model.load_weights(f'weights/RealESRGAN_x{scale}.pth', download=True)
        
        # Converter imagem para RGB se necessário
        if input_image.mode != 'RGB':
            input_image = input_image.convert('RGB')
        
        print(f"🔄 Aplicando Real-ESRGAN {scale}x...")
        
        # Aplicar upscaling
        upscaled_image = model.predict(input_image)
        
        # Aplicar pós-processamento se solicitado
        if apply_post_processing:
            upscaled_image = apply_post_processing_filters(upscaled_image)
        
        print("✅ Real-ESRGAN processamento concluído!")
        return upscaled_image
        
    except Exception as e:
        print(f"❌ Erro durante Real-ESRGAN: {e}")
        print("🔄 Usando fallback...")
        return fallback_upscale(input_image, scale)

def fallback_upscale(input_image, scale=4):
    """Upscaling de fallback usando PIL."""
    print(f"🔄 Usando upscaling PIL {scale}x...")
    new_size = (input_image.width * scale, input_image.height * scale)
    upscaled = input_image.resize(new_size, Image.Resampling.LANCZOS)
    return apply_post_processing_filters(upscaled)

def apply_post_processing_filters(image):
    """Aplica filtros de pós-processamento."""
    try:
        # Converter para OpenCV
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Filtro bilateral
        img_bilateral = cv2.bilateralFilter(img_cv, BILATERAL_D, BILATERAL_SIGMA_COLOR, BILATERAL_SIGMA_SPACE)
        
        # Converter de volta para PIL
        img_pil = Image.fromarray(cv2.cvtColor(img_bilateral, cv2.COLOR_BGR2RGB))
        
        # Realce de nitidez
        enhancer = ImageEnhance.Sharpness(img_pil)
        img_final = enhancer.enhance(SHARPNESS_FACTOR)
        
        return img_final
        
    except Exception as e:
        print(f"⚠️ Erro no pós-processamento: {e}")
        return image

# Função de compatibilidade para usar com path de arquivo
def upscale_and_enhance(input_path, output_path):
    """
    Função de compatibilidade que aceita caminhos de arquivo.
    """
    try:
        # Carregar imagem
        input_image = Image.open(input_path).convert('RGB')
        
        # Processar
        result = upscale_and_enhance_realesrgan(input_image)
        
        # Salvar
        result.save(output_path, quality=95)
        print(f"💾 Imagem salva em: {output_path}")
        
        return result
        
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        return None

def test_realesrgan():
    """Testa a disponibilidade do Real-ESRGAN."""
    print("🧪 Testando Real-ESRGAN...")
    
    if REALESRGAN_AVAILABLE:
        try:
            # Criar imagem de teste
            test_image = Image.new('RGB', (100, 100), color='red')
            
            # Testar processamento
            result = upscale_and_enhance_realesrgan(test_image, scale=2, apply_post_processing=False)
            
            if result.size == (200, 200):
                print("✅ Real-ESRGAN funcionando corretamente!")
                return True
            else:
                print("❌ Real-ESRGAN não produziu o resultado esperado")
                return False
                
        except Exception as e:
            print(f"❌ Erro durante teste: {e}")
            return False
    else:
        print("❌ Real-ESRGAN não está disponível")
        return False

if __name__ == "__main__":
    # Teste básico
    test_realesrgan()
    
    # Exemplo de uso
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "output_realesrgan.png"
        
        result = upscale_and_enhance(input_file, output_file)
        if result:
            print("🎉 Processamento concluído com sucesso!")
        else:
            print("💥 Falha no processamento!")
