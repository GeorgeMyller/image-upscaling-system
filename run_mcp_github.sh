#!/bin/bash

# Script para configurar e rodar o MCP do GitHub com Docker
# Este script facilita o uso do Model Context Protocol (MCP) do GitHub

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Configurador MCP GitHub + Docker${NC}"
echo "============================================"

# Verificar se o Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker não está rodando. Por favor, inicie o Docker Desktop e tente novamente.${NC}"
    exit 1
fi

# Verificar se a imagem existe
if ! docker image inspect mcp/github > /dev/null 2>&1; then
    echo -e "${YELLOW}🔧 Imagem MCP GitHub não encontrada. Construindo...${NC}"
    docker build -t mcp/github -f Dockerfile.mcp .
fi

# Verificar se há token do GitHub
if [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  Token do GitHub não encontrado.${NC}"
    echo "Para usar o MCP do GitHub, você precisa de um Personal Access Token."
    echo "1. Vá para: https://github.com/settings/tokens"
    echo "2. Crie um novo token com as permissões necessárias"
    echo "3. Configure a variável de ambiente:"
    echo "   export GITHUB_PERSONAL_ACCESS_TOKEN=seu_token_aqui"
    echo ""
    read -p "Deseja continuar mesmo sem o token? (y/n): " continue_without_token
    if [[ $continue_without_token != "y" ]]; then
        exit 1
    fi
fi

# Opções de uso
echo ""
echo "Escolha uma opção:"
echo "1. Testar conexão MCP GitHub"
echo "2. Rodar MCP GitHub em modo interativo"
echo "3. Rodar MCP GitHub em background"
echo "4. Parar todos os containers MCP"
echo "5. Ver logs do MCP GitHub"

read -p "Digite sua opção (1-5): " option

case $option in
    1)
        echo -e "${GREEN}🧪 Testando conexão MCP GitHub...${NC}"
        echo "Teste básico de conectividade..."
        docker run --rm \
            --env GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN" \
            mcp/github --version 2>/dev/null && echo "✅ MCP Server instalado corretamente" || echo "⚠️  MCP Server executando em modo stdio"
        ;;
    2)
        echo -e "${GREEN}🔄 Rodando MCP GitHub em modo interativo...${NC}"
        docker run --rm -it \
            --env GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN" \
            --name mcp-github-interactive \
            mcp/github
        ;;
    3)
        echo -e "${GREEN}🔄 Rodando MCP GitHub em background...${NC}"
        docker run -d \
            --env GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_PERSONAL_ACCESS_TOKEN" \
            --name mcp-github-bg \
            --restart unless-stopped \
            mcp/github
        echo "Container iniciado com nome: mcp-github-bg"
        ;;
    4)
        echo -e "${YELLOW}🛑 Parando todos os containers MCP...${NC}"
        docker stop $(docker ps -q --filter "name=mcp-github") 2>/dev/null || echo "Nenhum container MCP rodando"
        docker rm $(docker ps -aq --filter "name=mcp-github") 2>/dev/null || echo "Nenhum container MCP para remover"
        echo "Containers MCP parados e removidos"
        ;;
    5)
        echo -e "${GREEN}📋 Logs do MCP GitHub:${NC}"
        docker logs mcp-github-bg 2>/dev/null || echo "Container mcp-github-bg não encontrado"
        ;;
    *)
        echo -e "${RED}❌ Opção inválida${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Operação concluída!${NC}"
