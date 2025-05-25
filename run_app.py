#!/usr/bin/env python3
"""
Script para executar as aplicações de upscaling de forma mais fácil
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Mudar para o diretório do script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🖼️  Sistema de Upscaling de Imagens")
    print("=" * 50)
    print("Aplicações disponíveis:")
    print("1. App Final (Recomendado)")
   
    
    try:
        choice = input("\nEscolha uma opção (1): ").strip()

        apps = {
            '1': 'apps/app_final.py',
            
        }
        
        if choice in apps:
            app_path = apps[choice]
            print(f"\n🚀 Iniciando {app_path}...")
            print("Abra seu navegador em: http://localhost:8501")
            print("Para parar, pressione Ctrl+C")
            
            # Executar streamlit
            subprocess.run([
                sys.executable, '-m', 'streamlit', 'run', app_path
            ])
        else:
            print("❌ Opção inválida!")
            
    except KeyboardInterrupt:
        print("\n👋 Até logo!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
