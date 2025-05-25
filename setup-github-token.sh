#!/bin/bash

# Script para configurar o token do GitHub

echo "=== Configuração do MCP GitHub ==="
echo ""

# Verificar se já existe .env
if [ -f .env ]; then
    echo "Arquivo .env já existe. Deseja sobrescrevê-lo? (s/n)"
    read -r response
    if [[ ! "$response" =~ ^[Ss]$ ]]; then
        echo "Configuração cancelada."
        exit 0
    fi
fi

# Criar .env a partir do exemplo
if [ -f .env.example ]; then
    cp .env.example .env
    echo "Arquivo .env criado a partir do exemplo."
else
    echo "Arquivo .env.example não encontrado. Criando .env básico..."
    cat > .env << EOF
# Configuração do GitHub MCP
GITHUB_PERSONAL_ACCESS_TOKEN=seu_token_aqui
GITHUB_DEFAULT_REPO=
EOF
fi

echo ""
echo "Para obter seu token do GitHub:"
echo "1. Acesse: https://github.com/settings/tokens"
echo "2. Clique em 'Generate new token (classic)'"
echo "3. Dê um nome para o token (ex: MCP Access)"
echo "4. Selecione as permissões: repo, read:user, read:org"
echo "5. Clique em 'Generate token'"
echo "6. Copie o token gerado"
echo ""

# Perguntar se quer abrir o navegador
echo "Deseja abrir a página de tokens do GitHub agora? (s/n)"
read -r response
if [[ "$response" =~ ^[Ss]$ ]]; then
    open https://github.com/settings/tokens
fi

echo ""
echo "Agora edite o arquivo .env e substitua 'seu_token_aqui' pelo seu token real."
echo "Use o comando: nano .env"
echo ""
echo "Após configurar o token, execute: ./run-mcp-github.sh"
