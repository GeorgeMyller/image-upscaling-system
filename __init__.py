"""
Sistema de Upscaling de Imagens
==============================

Sistema completo para upscaling e melhoria de qualidade de imagens usando diferentes técnicas.

Módulos principais:
- apps/: Aplicações Streamlit
- modules/: Módulos de upscaling  
- tests/: Scripts de teste
- docs/: Documentação

Uso rápido:
    python run_app.py

Versão: 1.0.0
Data de organização: 24/05/2025
"""

__version__ = "1.0.0"
__author__ = "Sistema Resume Optimizer"
__description__ = "Sistema completo de upscaling de imagens"

from .config import *

# Imports opcionais para evitar erros se módulos não estiverem disponíveis
try:
    from .modules import *
except ImportError:
    pass

try:
    from .apps import *
except ImportError:
    pass
