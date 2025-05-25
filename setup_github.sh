#!/bin/bash

# Script para configurar o repositório Git e preparar para GitHub
echo "🚀 Configurando repositório Git para GitHub..."

# Inicializar repositório Git
git init

# Adicionar todos os arquivos
git add .

# Fazer primeiro commit
git commit -m "🎉 Initial commit: Sistema de Upscaling de Imagens

- Sistema completo de upscaling com 6 técnicas diferentes
- Interface Streamlit amigável
- Arquitetura modular e extensível
- Documentação completa
- Testes automatizados
- Configurações modernas (pyproject.toml)
- Sistema de diagnóstico automático"

# Configurar branch principal
git branch -M main

echo "✅ Repositório Git configurado!"
echo ""
echo "📋 Próximos passos:"
echo "1. Crie um repositório no GitHub: https://github.com/new"
echo "2. Nome sugerido: image-upscaling-system"
echo "3. Execute: git remote add origin https://github.com/GeorgeMyller/image-upscaling-system.git"
echo "4. Execute: git push -u origin main"
echo ""
echo "🎯 Seu projeto está pronto para o GitHub!"
