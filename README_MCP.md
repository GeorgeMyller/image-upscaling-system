# MCP GitHub + Docker - Guia de Configuração

Este repositório inclui configuração completa para usar o Model Context Protocol (MCP) do GitHub com Docker.

## 🚀 Instalação e Configuração

### 1. Pré-requisitos
- Docker Desktop instalado e rodando
- Token pessoal do GitHub (Personal Access Token)

### 2. Configuração do Token GitHub

1. Vá para [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Clique em "Generate new token (classic)"
3. Selecione as permissões necessárias:
   - `repo` (acesso completo a repositórios)
   - `read:user` (acesso de leitura ao perfil)
   - `read:org` (acesso de leitura a organizações)

4. Configure a variável de ambiente:
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=seu_token_aqui
```

Para tornar permanente, adicione no seu `~/.zshrc`:
```bash
echo 'export GITHUB_PERSONAL_ACCESS_TOKEN=seu_token_aqui' >> ~/.zshrc
source ~/.zshrc
```

### 3. Uso do MCP

#### Opção 1: Script Automático (Recomendado)
```bash
./run_mcp_github.sh
```

#### Opção 2: Comandos Docker Manuais

**Testar o MCP:**
```bash
docker run --rm -it --env GITHUB_PERSONAL_ACCESS_TOKEN mcp/github --help
```

**Rodar em modo interativo:**
```bash
docker run --rm -it --env GITHUB_PERSONAL_ACCESS_TOKEN --name mcp-github mcp/github
```

**Rodar em background:**
```bash
docker run -d --env GITHUB_PERSONAL_ACCESS_TOKEN --name mcp-github-bg --restart unless-stopped mcp/github
```

### 4. Configuração no VS Code

O arquivo `.vscode/settings.json` já está configurado. Para usar:

1. Instale a extensão "GitHub Copilot" no VS Code
2. Configure seu token no arquivo de configurações
3. O MCP será iniciado automaticamente quando necessário

### 5. Verificação

Para verificar se tudo está funcionando:

```bash
# Verificar se o Docker está rodando
docker --version

# Verificar se a imagem foi criada
docker images | grep mcp/github

# Testar o MCP
./run_mcp_github.sh
```

## 🛠️ Resolução de Problemas

### Erro: "spawn docker ENOENT"
- **Causa:** Docker não instalado ou não está no PATH
- **Solução:** Instale o Docker Desktop e certifique-se que está rodando

### Erro: Token inválido
- **Causa:** Token do GitHub incorreto ou sem permissões
- **Solução:** Verifique o token e suas permissões

### Container não inicia
- **Causa:** Docker não está rodando
- **Solução:** Inicie o Docker Desktop

## 📁 Arquivos de Configuração

- `Dockerfile.mcp` - Configuração do container Docker
- `run_mcp_github.sh` - Script de gerenciamento
- `.vscode/settings.json` - Configuração VS Code
- `mcp-settings.json` - Configuração standalone

## 🔧 Personalização

Para modificar a configuração do MCP, edite o arquivo `Dockerfile.mcp` e reconstrua a imagem:

```bash
docker build -t mcp/github -f Dockerfile.mcp .
```

## 📚 Recursos Adicionais

- [Documentação MCP](https://modelcontextprotocol.io/)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Docker Documentation](https://docs.docker.com/)

---

Agora o MCP do GitHub está configurado e pronto para uso! 🎉
