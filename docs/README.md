# Image Upscaling and Enhancement Scripts

Este diretório contém scripts para upscaling e melhoria de qualidade de imagens usando diferentes técnicas.

## Scripts Disponíveis

### 1. `app_upscaling_realce.py` - Aplicação Streamlit Principal
**Interface web** para upload e processamento de imagens com duas opções de processamento:

- **Básico (Pillow + OpenCV)**: Upscaling 2x + filtros de redução de ruído e realce
- **Real-ESRGAN (IA)**: Upscaling com IA + pós-processamento avançado (quando disponível)

**Como usar:**
```bash
uv run streamlit run scripts_upscaling_realce/app_upscaling_realce.py
```

### 2. `upscaling_realce_realesrgan.py` - Módulo Real-ESRGAN
Implementa funções de upscaling usando Real-ESRGAN com fallback para PIL/OpenCV.

**Principais funções:**
- `upscale_and_enhance(input_path, output_path)` - Para uso via linha de comando
- `upscale_and_enhance_realesrgan(img_pil, ...)` - Para uso no Streamlit

### 3. `upscaling_realce_pillow_opencv.py` - Módulo Básico
Implementação usando apenas Pillow e OpenCV (sem dependência de IA).

## Dependências

### Principais:
- `streamlit` - Interface web
- `pillow` - Manipulação de imagens
- `opencv-python` - Filtros avançados
- `numpy` - Operações numéricas

### Opcionais (para Real-ESRGAN):
- `py-real-esrgan` - Upscaling com IA
- `torch` - Backend PyTorch
- `torchvision` - Utilitários de visão computacional

## Instalação

```bash
# Instalar dependências principais
uv add streamlit pillow opencv-python numpy

# Instalar dependências opcionais para Real-ESRGAN
uv add py-real-esrgan torch torchvision
```

## Características

### Processamento Básico (Sempre Disponível)
- Upscaling 2x usando interpolação LANCZOS
- Filtro mediano para redução de ruído
- CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Filtro bilateral para suavização preservando bordas
- Realce de nitidez configurável

### Processamento com Real-ESRGAN (Quando Disponível)
- Upscaling inteligente usando redes neurais treinadas
- Melhor qualidade para imagens fotorealísticas
- Pós-processamento idêntico ao método básico
- Fallback automático se não estiver disponível

## Configuração

Os parâmetros podem ser ajustados nos arquivos:

```python
# Em upscaling_realce_realesrgan.py
MODEL_NAME = 'RealESRGAN_x2.pth'  # Modelo Real-ESRGAN
MODEL_SCALE = 2                    # Fator de escala
BILATERAL_D = 9                    # Filtro bilateral
BILATERAL_SIGMA_COLOR = 75
BILATERAL_SIGMA_SPACE = 75
SHARPNESS_FACTOR = 1.5            # Intensidade do realce
```

## Solução de Problemas

### Erro: "No module named 'torchvision.transforms.functional_tensor'"
- **Causa**: Incompatibilidade entre versões do PyTorch/torchvision
- **Solução**: O app automaticamente usa o fallback PIL/OpenCV

### Real-ESRGAN não funciona
- **Causa**: Dependências não instaladas ou incompatíveis
- **Solução**: O app continua funcionando com processamento básico

### Performance lenta
- **CUDA**: Se disponível, Real-ESRGAN usará GPU automaticamente
- **CPU**: Processamento será mais lento mas funcional

## Formato de Arquivos

- **Entrada**: JPG, PNG, WEBP, BMP (via Streamlit)
- **Saída**: PNG (para preservar qualidade)

## Melhorias Futuras

- [ ] Suporte a processamento em lote
- [ ] Mais opções de modelos Real-ESRGAN
- [ ] Parâmetros ajustáveis na interface
- [ ] Comparação lado-a-lado antes/depois
- [ ] Exportação em diferentes formatos
