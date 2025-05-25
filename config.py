"""
Configurações centralizadas para o sistema de upscaling
"""

import os
from pathlib import Path

# Diretórios do projeto
PROJECT_ROOT = Path(__file__).parent
APPS_DIR = PROJECT_ROOT / "apps"
MODULES_DIR = PROJECT_ROOT / "modules" 
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"
EXAMPLES_DIR = PROJECT_ROOT / "examples"

# Configurações de upscaling
DEFAULT_SCALE_FACTOR = 2
MAX_IMAGE_SIZE = 4096  # pixels
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']

# Configurações do Streamlit
STREAMLIT_CONFIG = {
    'port': 8501,
    'host': 'localhost',
    'theme': 'light'
}

# Modelos disponíveis
AVAILABLE_METHODS = {
    'basic': 'Pillow + OpenCV (Básico)',
    'realesrgan': 'Real-ESRGAN (IA)',
    'waifu2x': 'Waifu2x (Anime/Art)',
    'huggingface': 'Hugging Face Models',
    'advanced': 'Métodos Avançados',
    'unified': 'Unificado (Auto-detect)'
}

# Status dos módulos
MODULE_STATUS = {
    'upscaling_realce_pillow_opencv.py': 'stable',
    'upscaling_realce_realesrgan.py': 'stable', 
    'upscaling_advanced.py': 'stable',
    'upscaling_unified.py': 'stable',
    'upscaling_waifu2x.py': 'experimental',
    'upscaling_realce_huggingface.py': 'experimental'
}
