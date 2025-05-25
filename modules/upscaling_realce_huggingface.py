#!/usr/bin/env python3
"""
Upscaling com Real-ESRGAN usando ai-forever/Real-ESRGAN
Este módulo implementa upscaling de imagens usando o modelo Real-ESRGAN do repositório ai-forever.
Repositório: https://github.com/ai-forever/Real-ESRGAN
"""

import os
import sys
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageOps
from pathlib import Path
import torch

# Configurações
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Variável global para controlar disponibilidade
REALESRGAN_HF_AVAILABLE = False
model = None

def initialize_realesrgan():
    """Inicializa o modelo Real-ESRGAN do ai-forever."""
    global REALESRGAN_HF_AVAILABLE, model
    
    try:
        from RealESRGAN import RealESRGAN
        print(f"🚀 Inicializando Real-ESRGAN (ai-forever) no dispositivo: {DEVICE}")
        
        # Inicializar modelo Real-ESRGAN
        model = RealESRGAN(DEVICE, scale=4)
        
        # Carregar pesos do modelo (será baixado automaticamente se necessário)
        print("📥 Carregando pesos do modelo...")
        model.load_weights('weights/RealESRGAN_x4.pth', download=True)
        
        REALESRGAN_HF_AVAILABLE = True
        print("✅ Real-ESRGAN (ai-forever) inicializado com sucesso!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar RealESRGAN: {e}")
        print("💡 Execute: uv add git+https://github.com/ai-forever/Real-ESRGAN.git")
        REALESRGAN_HF_AVAILABLE = False
        return False
    except Exception as e:
        print(f"❌ Erro ao inicializar Real-ESRGAN: {e}")
        REALESRGAN_HF_AVAILABLE = False
        return False

def upscale_with_realesrgan_hf(input_image):
    """
    Aplica upscaling usando Real-ESRGAN do ai-forever.
    
    Args:
        input_image: PIL Image object
        
    Returns:
        PIL Image object com upscaling aplicado
    """
    global model
    
    if not REALESRGAN_HF_AVAILABLE or model is None:
        raise RuntimeError("Real-ESRGAN não está disponível")
    
    try:
        print("🔄 Aplicando Real-ESRGAN...")
        
        # Converter imagem para formato adequado se necessário
        if input_image.mode != 'RGB':
            input_image = input_image.convert('RGB')
        
        # Aplicar Real-ESRGAN usando o método predict
        upscaled_image = model.predict(input_image)
        
        print("✅ Real-ESRGAN aplicado com sucesso!")
        return upscaled_image
        
    except Exception as e:
        print(f"❌ Erro durante upscaling: {e}")
        raise

def apply_post_processing(image, enhance_contrast=True, enhance_sharpness=True, bilateral_filter=True):
    """
    Aplica pós-processamento para melhorar a qualidade da imagem.
    
    Args:
        image: PIL Image object
        enhance_contrast: bool, aplicar realce de contraste
        enhance_sharpness: bool, aplicar realce de nitidez
        bilateral_filter: bool, aplicar filtro bilateral
        
    Returns:
        PIL Image object processada
    """
    try:
        print("🎨 Aplicando pós-processamento...")
        
        # Converter para numpy para processamento OpenCV
        img_array = np.array(image)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Aplicar filtro bilateral para reduzir ruído preservando bordas
        if bilateral_filter:
            print("   - Aplicando filtro bilateral...")
            img_cv = cv2.bilateralFilter(img_cv, 9, 75, 75)
        
        # Converter de volta para PIL para realces
        img_cv_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_cv_rgb)
        
        # Realce de contraste
        if enhance_contrast:
            print("   - Melhorando contraste...")
            enhancer = ImageEnhance.Contrast(img_pil)
            img_pil = enhancer.enhance(1.1)  # Aumento sutil de contraste
        
        # Realce de nitidez
        if enhance_sharpness:
            print("   - Melhorando nitidez...")
            enhancer = ImageEnhance.Sharpness(img_pil)
            img_pil = enhancer.enhance(1.2)  # Aumento sutil de nitidez
        
        print("✅ Pós-processamento concluído!")
        return img_pil
        
    except Exception as e:
        print(f"❌ Erro durante pós-processamento: {e}")
        return image  # Retorna imagem original em caso de erro

def upscale_and_enhance_realesrgan(input_path, output_path=None, apply_postprocessing=True):
    """
    Função principal para upscaling e melhoramento de imagem.
    
    Args:
        input_path: str, caminho para imagem de entrada
        output_path: str, caminho para salvar resultado (opcional)
        apply_postprocessing: bool, aplicar pós-processamento
        
    Returns:
        PIL Image object ou None em caso de erro
    """
    try:
        print(f"🖼️  Carregando imagem: {input_path}")
        
        # Verificar se arquivo existe
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {input_path}")
        
        # Carregar imagem
        input_image = Image.open(input_path)
        original_size = input_image.size
        print(f"📏 Tamanho original: {original_size[0]}x{original_size[1]}")
        
        # Inicializar modelo se necessário
        if not REALESRGAN_HF_AVAILABLE:
            print("⚠️  Inicializando Real-ESRGAN...")
            if not initialize_realesrgan():
                return fallback_upscaling(input_image, apply_postprocessing)
        
        # Aplicar Real-ESRGAN
        upscaled_image = upscale_with_realesrgan_hf(input_image)
        new_size = upscaled_image.size
        print(f"📈 Novo tamanho: {new_size[0]}x{new_size[1]}")
        
        # Aplicar pós-processamento se solicitado
        if apply_postprocessing:
            upscaled_image = apply_post_processing(upscaled_image)
        
        # Salvar resultado se caminho fornecido
        if output_path:
            upscaled_image.save(output_path, "PNG", quality=95)
            print(f"💾 Imagem salva em: {output_path}")
        
        return upscaled_image
        
    except Exception as e:
        print(f"❌ Erro durante processamento: {e}")
        return None

def fallback_upscaling(input_image, apply_postprocessing=True):
    """
    Upscaling de fallback usando PIL quando Real-ESRGAN não está disponível.
    
    Args:
        input_image: PIL Image object
        apply_postprocessing: bool, aplicar pós-processamento
        
    Returns:
        PIL Image object
    """
    print("🔄 Usando upscaling de fallback (PIL)...")
    
    try:
        # Upscaling 4x usando LANCZOS
        new_size = (input_image.width * 4, input_image.height * 4)
        upscaled_image = input_image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Aplicar pós-processamento se solicitado
        if apply_postprocessing:
            upscaled_image = apply_post_processing(upscaled_image)
        
        print("✅ Fallback upscaling concluído!")
        return upscaled_image
        
    except Exception as e:
        print(f"❌ Erro durante fallback: {e}")
        return input_image

def test_realesrgan_hf():
    """Testa a disponibilidade e funcionamento do Real-ESRGAN ai-forever."""
    print("🧪 Testando Real-ESRGAN (ai-forever)...")
    
    # Testar inicialização
    success = initialize_realesrgan()
    
    if success:
        print("✅ Real-ESRGAN (ai-forever) está funcionando!")
        return True
    else:
        print("❌ Real-ESRGAN (ai-forever) não está disponível")
        return False

if __name__ == "__main__":
    # Teste básico
    test_realesrgan_hf()
    
    # Exemplo de uso
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "output_realesrgan_hf.png"
        
        result = upscale_and_enhance_realesrgan(input_file, output_file)
        if result:
            print("🎉 Processamento concluído com sucesso!")
        else:
            print("💥 Falha no processamento!")
