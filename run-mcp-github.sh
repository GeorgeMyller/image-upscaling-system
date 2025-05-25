#!/bin/bash

# Script para executar o servidor MCP do GitHub

echo "Iniciando servidor MCP do GitHub..."

# Verificar se o Docker está rodando
if ! docker info >/dev/null 2>&1; then
    echo "Erro: Docker não está rodando. Por favor, inicie o Docker Desktop."
    exit 1
fi

# Carregar variáveis de ambiente do arquivo .env se existir
if [ -f .env ]; then
    echo "Carregando configurações do arquivo .env..."
    set -a
    source .env
    set +a
else
    echo "Arquivo .env não encontrado. Criando a partir do exemplo..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "Por favor, edite o arquivo .env e adicione seu token do GitHub."
        echo "Depois execute novamente este script."
        exit 1
    fi
fi

# Verificar se o token foi configurado
if [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ] || [ "$GITHUB_PERSONAL_ACCESS_TOKEN" = "seu_token_aqui" ]; then
    echo "Erro: Token do GitHub não configurado!"
    echo "Por favor, edite o arquivo .env e adicione seu token."
    echo "Obtenha um token em: https://github.com/settings/tokens"
    exit 1
fi

echo "Token configurado. Iniciando servidor MCP..."

# Executar o servidor MCP
docker run --rm -i \
    --env GITHUB_PERSONAL_ACCESS_TOKEN \
    mcp-github \
    < /dev/stdin
