# Contributing to Image Upscaling System

Obrigado pelo seu interesse em contribuir! Este guia vai te ajudar a começar.

## 🚀 Como Contribuir

### Reportar Bugs
1. Verifique se o bug já foi reportado nas [Issues](https://github.com/GeorgeMyller/image-upscaling-system/issues)
2. Se não, abra uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Screenshots (se aplicável)
   - Informações do sistema (OS, Python version)

### Sugerir Melhorias
1. Abra uma issue com o label "enhancement"
2. Descreva claramente sua sugestão
3. Explique por que seria útil

### Contribuir com Código

#### Setup do Ambiente
1. Fork o repositório
2. Clone seu fork:
   ```bash
   git clone https://github.com/GeorgeMyller/image-upscaling-system.git
   cd image-upscaling-system
   ```

3. Instale dependências:
   ```bash
   # Dependências básicas
   pip install -r requirements.txt
   
   # Dependências de desenvolvimento (opcional)
   pip install -e ".[dev]"
   ```

4. Execute os testes:
   ```bash
   python -m pytest tests/
   ```

#### Processo de Desenvolvimento
1. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. Faça suas alterações
3. Execute os testes:
   ```bash
   python diagnostico.py
   python -m pytest tests/
   ```

4. Commit suas mudanças:
   ```bash
   git commit -m "feat: adiciona nova funcionalidade"
   ```

5. Push para sua branch:
   ```bash
   git push origin feature/nova-funcionalidade
   ```

6. Abra um Pull Request

## 📋 Diretrizes

### Código
- Use Python 3.8+ features
- Siga PEP 8 (use `black` para formatação)
- Adicione docstrings para funções públicas
- Inclua type hints quando possível

### Commit Messages
Use o formato [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` mudanças na documentação
- `style:` formatação, sem mudanças de código
- `refactor:` refatoração de código
- `test:` adição/modificação de testes
- `chore:` mudanças de build, etc.

### Pull Requests
- Descreva claramente o que sua PR faz
- Referencie issues relacionadas
- Inclua screenshots para mudanças visuais
- Certifique-se que os testes passam

## 🧪 Testes

### Executar Testes
```bash
# Diagnóstico completo
python diagnostico.py

# Testes unitários
python -m pytest tests/

# Teste de instalação
python tests/test_installation.py

# Teste de modelos
python tests/test_models.py
```

### Adicionar Novos Testes
- Adicione testes para novas funcionalidades
- Mantenha cobertura de teste alta
- Use pytest para testes unitários

## 📂 Estrutura do Projeto

```
scripts_upscaling_realce/
├── apps/           # Aplicações Streamlit
├── modules/        # Módulos de upscaling
├── tests/          # Testes
├── docs/           # Documentação
├── examples/       # Exemplos
├── config.py       # Configurações
└── run_app.py      # Script principal
```

## 🏷️ Adicionando Novos Métodos de Upscaling

1. Crie um novo arquivo em `modules/`
2. Implemente a interface padrão:
   ```python
   def upscale_image(input_path, output_path, scale_factor=2, **kwargs):
       """
       Função principal de upscaling
       
       Args:
           input_path: Caminho da imagem de entrada
           output_path: Caminho da imagem de saída
           scale_factor: Fator de escala
           **kwargs: Parâmetros específicos do método
       
       Returns:
           bool: True se bem-sucedido
       """
       pass
   ```

3. Adicione testes em `tests/`
4. Atualize a documentação
5. Adicione ao `config.py` se necessário

## 💡 Ideias para Contribuições

- [ ] Novos métodos de upscaling
- [ ] Melhorias na interface Streamlit
- [ ] Otimizações de performance
- [ ] Suporte a novos formatos de imagem
- [ ] Processamento em batch
- [ ] API REST
- [ ] Docker container
- [ ] Testes mais abrangentes
- [ ] Documentação melhorada

## 📞 Contato

Se tiver dúvidas, abra uma issue ou entre em contato!

---

Obrigado por contribuir! 🚀
