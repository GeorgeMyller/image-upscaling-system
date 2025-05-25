# Configuração MCP GitHub para VS Code

Para configurar o MCP do GitHub no VS Code, você precisa configurar no arquivo de configurações do Claude Desktop ou outro cliente MCP.

## Passo a Passo:

### 1. Configure o Token do GitHub
```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=seu_token_aqui
```

### 2. Configure no arquivo de configuração MCP

Para **Claude Desktop**, adicione ao arquivo `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--env",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "mcp/github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": ""
      }
    }
  }
}
```

### 3. Para outros clientes MCP

Use a configuração no arquivo `mcp-settings.json` que está na raiz do projeto.

### 4. Testando

Execute o script de teste:
```bash
./run_mcp_github.sh
```

O MCP do GitHub agora está configurado para funcionar com Docker! 🎉
