"""
Script de teste para verificar a funcionalidade dos modelos de upscaling
"""

import sys
import os
from PIL import Image
import tempfile

# Testar importações
print("🔍 Testando importações dos modelos...")

# 1. Classic PIL + OpenCV
try:
    from upscaling_realce_pillow_opencv import upscale_and_enhance_pil
    print("✅ Classic PIL + OpenCV: Disponível")
    classic_available = True
except ImportError as e:
    print(f"❌ Classic PIL + OpenCV: {e}")
    classic_available = False

# 2. Smart Upscaling
try:
    from upscaling_smart import upscale_and_enhance_smart, is_enhanced_upscaling_available
    smart_available = is_enhanced_upscaling_available()
    print(f"✅ Smart Upscaling: {'Disponível' if smart_available else 'Parcialmente disponível'}")
except ImportError as e:
    print(f"❌ Smart Upscaling: {e}")
    smart_available = False

# 3. Waifu2x
try:
    from upscaling_waifu2x import upscale_and_enhance_waifu2x, is_waifu2x_available
    waifu2x_available = is_waifu2x_available()
    print(f"✅ Waifu2x: {'Disponível' if waifu2x_available else 'Não disponível'}")
except ImportError as e:
    print(f"❌ Waifu2x: {e}")
    waifu2x_available = False

# 4. Real-ESRGAN Original
try:
    from upscaling_realce_realesrgan import upscale_and_enhance_realesrgan, is_realesrgan_available
    realesrgan_original_available = is_realesrgan_available()
    print(f"✅ Real-ESRGAN Original: {'Disponível' if realesrgan_original_available else 'Não disponível'}")
except ImportError as e:
    print(f"❌ Real-ESRGAN Original: {e}")
    realesrgan_original_available = False

# 5. Real-ESRGAN New
try:
    from upscaling_realce_realesrgan_new import upscale_and_enhance_realesrgan as realesrgan_new
    print("✅ Real-ESRGAN New: Disponível")
    realesrgan_new_available = True
except ImportError as e:
    print(f"❌ Real-ESRGAN New: {e}")
    realesrgan_new_available = False

# 6. HuggingFace Real-ESRGAN
try:
    from upscaling_realce_huggingface import upscale_and_enhance_realesrgan as realesrgan_hf
    print("✅ Real-ESRGAN HuggingFace: Disponível")
    realesrgan_hf_available = True
except ImportError as e:
    print(f"❌ Real-ESRGAN HuggingFace: {e}")
    realesrgan_hf_available = False

print("\n" + "="*50)
print("📊 RESUMO DOS MODELOS DISPONÍVEIS:")
print("="*50)

available_count = 0
total_count = 6

if classic_available:
    print("✅ Classic PIL + OpenCV")
    available_count += 1
else:
    print("❌ Classic PIL + OpenCV")

if smart_available:
    print("✅ Smart Upscaling")
    available_count += 1
else:
    print("❌ Smart Upscaling")

if waifu2x_available:
    print("✅ Waifu2x")
    available_count += 1
else:
    print("❌ Waifu2x")

if realesrgan_original_available:
    print("✅ Real-ESRGAN Original")
    available_count += 1
else:
    print("❌ Real-ESRGAN Original")

if realesrgan_new_available:
    print("✅ Real-ESRGAN New")
    available_count += 1
else:
    print("❌ Real-ESRGAN New")

if realesrgan_hf_available:
    print("✅ Real-ESRGAN HuggingFace")
    available_count += 1
else:
    print("❌ Real-ESRGAN HuggingFace")

print(f"\n🎯 {available_count}/{total_count} modelos disponíveis")

# Teste rápido com o método classic se disponível
if classic_available:
    print("\n🧪 Testando método Classic com imagem de teste...")
    try:
        # Criar imagem de teste
        test_image = Image.new('RGB', (50, 50), color='red')
        
        # Testar upscaling
        result = upscale_and_enhance_pil(test_image, scale_factor=2)
        
        print(f"✅ Teste bem-sucedido! Tamanho original: {test_image.size}, Upscaled: {result.size}")
        
    except Exception as e:
        print(f"❌ Teste falhou: {e}")

print("\n🚀 Para executar o app Streamlit unificado:")
print("streamlit run app_upscaling_unified.py")
