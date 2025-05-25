# 🚀 Image Upscaling Studio

Interface unificada para todos os métodos de upscaling de imagem disponíveis.

## ✨ Modelos Disponíveis

### 🎨 Classic (PIL + OpenCV) ⚡
- **Status**: ✅ Funcionando
- **Tipo**: Processamento em tempo real
- **Descrição**: Método clássico otimizado usando PIL e OpenCV
- **Parâmetros**:
  - Scale Factor (1-8)
  - Denoise Filter Size (filtro de mediana)
  - Bilateral Filter Diameter (redução de ruído)
  - CLAHE Clip Limit (contraste adaptativo)
  - Saturation Factor (saturação de cores)
  - Brightness Factor (brilho)

### 🧠 Smart Upscaling 🔄
- **Status**: ✅ Funcionando
- **Tipo**: Processamento por botão
- **Descrição**: Upscaling inteligente com SRCNN/TensorFlow e métodos clássicos aprimorados
- **Tecnologias**: TensorFlow, Scikit-image, OpenCV
- **Parâmetros**:
  - Scale Factor (1-8)
  - Enhance Contrast (checkbox)
  - Enhance Sharpness (checkbox)

### 🚀 Real-ESRGAN (New) 🔄
- **Status**: ✅ Funcionando
- **Tipo**: Processamento por botão
- **Descrição**: Real-ESRGAN versão atualizada e otimizada
- **Parâmetros**:
  - Scale Factor (2 ou 4)
  - Apply Post-Processing (checkbox)

### 🤗 Real-ESRGAN (HuggingFace) 🔄
- **Status**: ✅ Funcionando
- **Tipo**: Processamento por botão
- **Descrição**: Real-ESRGAN via HuggingFace - Fácil instalação
- **Parâmetros**:
  - Apply Post-Processing (checkbox)

### ❌ Modelos Não Disponíveis
- **🎌 Waifu2x**: Requer instalação adicional
- **🤖 Real-ESRGAN (Original)**: Requer módulo RealESRGAN

## 🚀 Como Usar

### 1. Executar o App
```bash
cd curriculo_vaga_novo-curriculo2
uv run streamlit run scripts_upscaling_realce/app_upscaling_studio.py --server.port 8504
```

### 2. Interface
1. **Upload de Imagem**: Arraste ou selecione uma imagem (PNG, JPG, JPEG, BMP, TIFF)
2. **Escolha do Método**: Selecione o método de upscaling na sidebar
3. **Ajuste de Parâmetros**: Configure os parâmetros específicos do método
4. **Processamento**:
   - ⚡ **Tempo Real**: Parâmetros se aplicam automaticamente (Classic)
   - 🔄 **Por Botão**: Clique em "Process Image" para aplicar (outros métodos)
5. **Download**: Baixe a imagem processada

### 3. Tipos de Processamento

#### ⚡ Processamento em Tempo Real (Classic)
- Os parâmetros são aplicados automaticamente conforme você move os sliders
- Ideal para ajustes finos e experimentos rápidos
- Cache inteligente para evitar reprocessamento desnecessário

#### 🔄 Processamento por Botão (AI Models)
- Clique no botão "Process Image" para aplicar as configurações
- Usado para métodos mais pesados computacionalmente
- Mantém resultado anterior até novo processamento

## 📊 Status dos Modelos

O app verifica automaticamente quais modelos estão disponíveis:
- ✅ = Modelo disponível e funcionando
- ❌ = Modelo não disponível (módulos não instalados)
- ⚡ = Suporte a processamento em tempo real
- 🔄 = Processamento por botão

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Interface web
- **PIL/Pillow**: Processamento básico de imagens
- **OpenCV**: Filtros avançados e processamento
- **TensorFlow**: SRCNN para Smart Upscaling
- **Scikit-image**: Processamento científico de imagens
- **NumPy**: Operações matriciais

## 📁 Estrutura dos Arquivos

```
scripts_upscaling_realce/
├── app_upscaling_studio.py          # Interface principal unificada
├── test_models.py                   # Teste de disponibilidade dos modelos
├── upscaling_realce_pillow_opencv.py # Método clássico (PIL + OpenCV)
├── upscaling_smart.py               # Smart upscaling com IA
├── upscaling_realce_realesrgan_new.py # Real-ESRGAN versão nova
├── upscaling_realce_huggingface.py  # Real-ESRGAN via HuggingFace
├── upscaling_waifu2x.py            # Waifu2x (requer instalação)
└── upscaling_realce_realesrgan.py  # Real-ESRGAN original (requer RealESRGAN)
```

## 🎯 Recomendações de Uso

1. **Para ajustes rápidos**: Use o método **Classic** com processamento em tempo real
2. **Para melhor qualidade com IA**: Use **Smart Upscaling** ou **Real-ESRGAN**
3. **Para imagens pequenas**: Classic ou Smart funcionam bem
4. **Para imagens grandes**: Real-ESRGAN pode dar melhores resultados
5. **Para experimentar parâmetros**: Classic é ideal pela resposta instantânea

## 🔧 Resolução de Problemas

- **Modelo não aparece**: Verifique se os módulos necessários estão instalados
- **Erro de processamento**: Tente um método diferente ou reduza o tamanho da imagem
- **Performance lenta**: Use Scale Factor menor ou método Classic
- **Qualidade baixa**: Ajuste os parâmetros de pós-processamento

## 📈 Comparação de Métodos

| Método | Velocidade | Qualidade | Facilidade | Parâmetros |
|--------|------------|-----------|------------|-------------|
| Classic | ⚡⚡⚡ | ⭐⭐⭐ | ⚡⚡⚡ | ⚙️⚙️⚙️ |
| Smart | ⚡⚡ | ⭐⭐⭐⭐ | ⚡⚡ | ⚙️⚙️ |
| Real-ESRGAN New | ⚡ | ⭐⭐⭐⭐⭐ | ⚡⚡ | ⚙️ |
| Real-ESRGAN HF | ⚡ | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | ⚙️ |

---

Desenvolvido para o projeto **Resume Optimize Crew** 🤖
