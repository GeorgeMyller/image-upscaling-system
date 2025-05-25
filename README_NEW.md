# 🖼️ Sistema de Upscaling de Imagens

Sistema completo para upscaling e melhoria de qualidade de imagens usando diferentes técnicas, desde métodos básicos até IA avançada.

## 📁 Estrutura do Projeto

```
scripts_upscaling_realce/
├── apps/                    # Aplicações Streamlit
│   ├── app_final.py        # App principal (recomendado)
│   ├── app_upscaling_realce.py
│   ├── app_upscaling_simple.py
│   ├── app_upscaling_studio.py
│   └── app_upscaling_unified.py
├── modules/                 # Módulos de upscaling
│   ├── upscaling_advanced.py
│   ├── upscaling_realce_huggingface.py
│   ├── upscaling_realce_pillow_opencv.py
│   ├── upscaling_realce_realesrgan.py
│   ├── upscaling_smart.py
│   ├── upscaling_unified.py
│   └── upscaling_waifu2x.py
├── tests/                   # Scripts de teste
│   ├── test_installation.py
│   └── test_models.py
├── docs/                    # Documentação
│   ├── README.md
│   ├── README_SOLUCOES.md
│   └── README_UNIFIED.md
├── examples/               # Exemplos (para futuro uso)
└── run_app.py              # Script de execução simplificado
```

## 🚀 Como Usar

### Script de Execução Simplificado (Recomendado)
```bash
# A partir desta pasta
python run_app.py
```
Este script interativo apresenta um menu para escolher qual aplicação executar.

### Aplicação Principal
```bash
# A partir da raiz do projeto
uv run streamlit run scripts_upscaling_realce/apps/app_final.py
```

### Outras Aplicações
```bash
# Aplicação simples
uv run streamlit run scripts_upscaling_realce/apps/app_upscaling_simple.py

# Aplicação studio (mais recursos)
uv run streamlit run scripts_upscaling_realce/apps/app_upscaling_studio.py
```

## 🛠️ Técnicas Disponíveis

### 1. **Básico (Pillow + OpenCV)**
- Upscaling usando interpolação bicúbica
- Filtros de redução de ruído
- Realce de nitidez
- **Vantagens**: Rápido, sem dependências pesadas
- **Melhor para**: Imagens simples, uso geral

### 2. **Real-ESRGAN (IA)**
- Upscaling com redes neurais especializadas
- Múltiplos modelos disponíveis
- Pós-processamento avançado
- **Vantagens**: Qualidade superior, especialmente para fotos
- **Melhor para**: Fotos realísticas, detalhes complexos

### 3. **Waifu2x**
- Especializado em imagens de anime/artwork
- Redução de ruído eficiente
- **Vantagens**: Excelente para ilustrações
- **Melhor para**: Arte digital, anime, desenhos

### 4. **Hugging Face Models**
- Modelos variados da comunidade
- Fácil atualização e experimentação
- **Vantagens**: Acesso a modelos de última geração
- **Melhor para**: Experimentação, casos específicos

## ⚙️ Instalação

### Dependências Básicas
```bash
uv add streamlit pillow opencv-python numpy
```

### Dependências para IA (Opcional)
```bash
# Real-ESRGAN
uv add py-real-esrgan torch torchvision

# Hugging Face
uv add transformers diffusers

# Waifu2x
uv add waifu2x-python
```

## 🧪 Testes

### Verificar Instalação
```bash
python scripts_upscaling_realce/tests/test_installation.py
```

### Testar Modelos
```bash
python scripts_upscaling_realce/tests/test_models.py
```

## 📋 Status dos Módulos

| Módulo | Status | Descrição |
|--------|---------|-----------|
| `upscaling_realce_pillow_opencv.py` | ✅ Estável | Método básico sempre funcional |
| `upscaling_realce_realesrgan.py` | ✅ Estável | IA para fotos realísticas |
| `upscaling_advanced.py` | ✅ Estável | Múltiplas técnicas avançadas |
| `upscaling_unified.py` | ✅ Estável | Interface unificada |
| `upscaling_waifu2x.py` | ⚠️ Experimental | Para anime/artwork |
| `upscaling_realce_huggingface.py` | ⚠️ Experimental | Modelos da comunidade |

## 🎯 Casos de Uso Recomendados

1. **Fotos Pessoais**: Use Real-ESRGAN (`app_final.py`)
2. **Documentos/Texto**: Use método básico Pillow+OpenCV
3. **Arte Digital**: Use Waifu2x
4. **Experimentação**: Use Hugging Face models
5. **Uso Geral**: Use `app_final.py` (detecção automática)

## 📝 Próximos Passos

- [ ] Adicionar exemplos na pasta `examples/`
- [ ] Implementar batch processing
- [ ] Adicionar suporte para mais formatos
- [ ] Criar interface CLI
- [ ] Documentar APIs dos módulos

## 🤝 Contribuição

Para adicionar novos métodos de upscaling:
1. Crie um novo arquivo em `modules/`
2. Implemente a interface padrão
3. Adicione testes em `tests/`
4. Atualize a documentação

## 🔧 Manutenção

A pasta foi reorganizada em **24/05/2025** para melhor estruturação:
- Apps Streamlit movidos para `apps/`
- Módulos de upscaling movidos para `modules/`
- Testes movidos para `tests/`
- Documentação movida para `docs/`
- Script de execução simplificado adicionado (`run_app.py`)
