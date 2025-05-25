#!/usr/bin/env python3
"""
Script de diagnóstico para o sistema de upscaling
Verifica dependências, módulos e configurações
"""

import sys
import os
import importlib
from pathlib import Path

def check_python_version():
    """Verifica a versão do Python"""
    print("🐍 Python Version Check")
    print(f"Versão: {sys.version}")
    
    if sys.version_info < (3, 8):
        print("⚠️  Aviso: Python 3.8+ recomendado")
    else:
        print("✅ Versão do Python OK")
    print()

def check_basic_dependencies():
    """Verifica dependências básicas"""
    print("📦 Basic Dependencies Check")
    
    basic_deps = [
        ("streamlit", "Streamlit"),
        ("PIL", "Pillow"),
        ("cv2", "OpenCV"),
        ("numpy", "NumPy")
    ]
    
    for module, name in basic_deps:
        try:
            importlib.import_module(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - FALTANDO")
    print()

def check_ai_dependencies():
    """Verifica dependências de IA (opcionais)"""
    print("🤖 AI Dependencies Check (Opcionais)")
    
    ai_deps = [
        ("torch", "PyTorch"),
        ("torchvision", "TorchVision"),
        ("transformers", "Transformers"),
        ("diffusers", "Diffusers")
    ]
    
    for module, name in ai_deps:
        try:
            importlib.import_module(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"⚪ {name} - não instalado (opcional)")
    print()

def check_project_structure():
    """Verifica a estrutura do projeto"""
    print("📁 Project Structure Check")
    
    expected_dirs = ["apps", "modules", "tests", "docs", "examples"]
    expected_files = ["README.md", "run_app.py", "config.py", "__init__.py"]
    
    project_root = Path(__file__).parent
    
    print("Diretórios:")
    for dir_name in expected_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ - FALTANDO")
    
    print("\nArquivos:")
    for file_name in expected_files:
        file_path = project_root / file_name
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - FALTANDO")
    print()

def check_upscaling_modules():
    """Verifica módulos de upscaling"""
    print("🔧 Upscaling Modules Check")
    
    # Adicionar diretório atual ao path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    modules = [
        ("modules.upscaling_realce_pillow_opencv", "Básico (Pillow+OpenCV)"),
        ("modules.upscaling_realce_realesrgan", "Real-ESRGAN"),
        ("modules.upscaling_advanced", "Avançado"),
        ("modules.upscaling_unified", "Unificado"),
        ("modules.upscaling_waifu2x", "Waifu2x"),
        ("modules.upscaling_realce_huggingface", "Hugging Face")
    ]
    
    for module, name in modules:
        try:
            importlib.import_module(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name} - Erro: {e}")
    print()

def check_streamlit_apps():
    """Verifica aplicações Streamlit"""
    print("🖥️  Streamlit Apps Check")
    
    apps_dir = Path(__file__).parent / "apps"
    
    if not apps_dir.exists():
        print("❌ Diretório apps/ não encontrado")
        return
    
    app_files = list(apps_dir.glob("app_*.py"))
    
    if app_files:
        print(f"Encontradas {len(app_files)} aplicações:")
        for app in app_files:
            print(f"✅ {app.name}")
    else:
        print("❌ Nenhuma aplicação encontrada")
    print()

def generate_summary():
    """Gera resumo do diagnóstico"""
    print("📋 RESUMO DO DIAGNÓSTICO")
    print("=" * 50)
    print("Para instalar dependências básicas:")
    print("  uv add streamlit pillow opencv-python numpy")
    print()
    print("Para instalar dependências de IA (opcional):")
    print("  uv add py-real-esrgan torch torchvision")
    print()
    print("Para executar o sistema:")
    print("  python run_app.py")
    print()

def main():
    """Função principal"""
    print("🖼️ DIAGNÓSTICO DO SISTEMA DE UPSCALING")
    print("=" * 50)
    print()
    
    check_python_version()
    check_basic_dependencies()
    check_ai_dependencies()
    check_project_structure()
    check_upscaling_modules()
    check_streamlit_apps()
    generate_summary()

if __name__ == "__main__":
    main()
