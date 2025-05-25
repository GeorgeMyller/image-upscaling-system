"""
Exemplo de uso dos módulos de upscaling
======================================

Este script demonstra como usar os diferentes módulos de upscaling disponíveis.
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório atual ao path para imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

def exemplo_basico():
    """Exemplo usando o método básico (Pillow + OpenCV)"""
    print("🔧 Exemplo: Método Básico (Pillow + OpenCV)")
    try:
        from modules.upscaling_realce_pillow_opencv import upscale_and_enhance
        print("✅ Módulo básico carregado com sucesso")
        
        # Exemplo de uso (descomente quando tiver uma imagem para testar)
        # result = upscale_and_enhance("input_image.jpg", "output_basic.jpg")
        # print(f"Resultado: {result}")
        
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo básico: {e}")

def exemplo_realesrgan():
    """Exemplo usando Real-ESRGAN"""
    print("\n🤖 Exemplo: Real-ESRGAN (IA)")
    try:
        from modules.upscaling_realce_realesrgan import upscale_and_enhance_realesrgan
        print("✅ Módulo Real-ESRGAN carregado com sucesso")
        
        # Exemplo de uso (descomente quando tiver uma imagem para testar)
        # from PIL import Image
        # img = Image.open("input_image.jpg")
        # result = upscale_and_enhance_realesrgan(img)
        # print(f"Resultado: {type(result)}")
        
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo Real-ESRGAN: {e}")

def exemplo_unified():
    """Exemplo usando o módulo unificado"""
    print("\n🎯 Exemplo: Módulo Unificado")
    try:
        from modules.upscaling_unified import UnifiedUpscaler
        upscaler = UnifiedUpscaler()
        print("✅ Módulo unificado carregado com sucesso")
        
        # Listar métodos disponíveis
        if hasattr(upscaler, 'available_methods'):
            print(f"Métodos disponíveis: {upscaler.available_methods}")
        
    except ImportError as e:
        print(f"❌ Erro ao carregar módulo unificado: {e}")

def verificar_instalacao():
    """Verifica quais módulos estão disponíveis"""
    print("🔍 Verificando instalação dos módulos...")
    
    modules_to_check = [
        "modules.upscaling_realce_pillow_opencv",
        "modules.upscaling_realce_realesrgan", 
        "modules.upscaling_advanced",
        "modules.upscaling_unified",
        "modules.upscaling_waifu2x",
        "modules.upscaling_realce_huggingface"
    ]
    
    available = []
    unavailable = []
    
    for module in modules_to_check:
        try:
            __import__(module)
            available.append(module.split('.')[-1])
        except ImportError:
            unavailable.append(module.split('.')[-1])
    
    print(f"\n✅ Módulos disponíveis ({len(available)}):")
    for mod in available:
        print(f"  - {mod}")
    
    print(f"\n❌ Módulos indisponíveis ({len(unavailable)}):")
    for mod in unavailable:
        print(f"  - {mod}")

if __name__ == "__main__":
    print("🖼️ Exemplos do Sistema de Upscaling de Imagens")
    print("=" * 50)
    
    # Verificar instalação
    verificar_instalacao()
    
    print("\n" + "=" * 50)
    
    # Executar exemplos
    exemplo_basico()
    exemplo_realesrgan()
    exemplo_unified()
    
    print("\n🎉 Exemplos concluídos!")
    print("\nPara usar com imagens reais:")
    print("1. Execute: python run_app.py")
    print("2. Ou use Streamlit: streamlit run apps/app_final.py")
