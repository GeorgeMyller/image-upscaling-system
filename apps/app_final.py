"""
Aplicação Streamlit Final para Upscaling de Imagens
Versão estável com múltiplos métodos funcionais
"""

import streamlit as st
import tempfile
import os
from PIL import Image
import io
import zipfile
from pathlib import Path

# Import our upscaling modules
import sys
sys.path.append('..')  # Para importar módulos da pasta parent

try:
    from modules.upscaling_advanced import AdvancedUpscaler, upscale_image
    ADVANCED_AVAILABLE = True
except ImportError:
    ADVANCED_AVAILABLE = False
    st.error("Módulo avançado não disponível")

try:
    from modules.upscaling_unified import UnifiedUpscaler
    UNIFIED_AVAILABLE = True
except ImportError:
    UNIFIED_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="AI Image Upscaler",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚀 AI Image Upscaler")
    st.markdown("**Melhore a qualidade das suas imagens com IA e algoritmos avançados**")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configurações")
    
    # Method selection
    if ADVANCED_AVAILABLE:
        upscaler_type = st.sidebar.selectbox(
            "Tipo de Upscaler:",
            ["Avançado (Recomendado)", "Unificado", "Simples"]
        )
    else:
        upscaler_type = "Simples"
        st.sidebar.warning("Apenas métodos simples disponíveis")
    
    # Scale factor
    scale_factor = st.sidebar.slider(
        "Fator de Escala:",
        min_value=1.5,
        max_value=4.0,
        value=2.0,
        step=0.5
    )
    
    # Quality settings
    if upscaler_type == "Avançado (Recomendado)":
        quality = st.sidebar.selectbox(
            "Qualidade:",
            ["highest", "high", "fast"],
            index=1
        )
    
    # Advanced settings
    with st.sidebar.expander("🔧 Configurações Avançadas"):
        apply_post_processing = st.checkbox("Aplicar pós-processamento", value=True)
        preserve_aspect_ratio = st.checkbox("Preservar proporção", value=True)
        output_format = st.selectbox("Formato de saída:", ["PNG", "JPEG", "WEBP"], index=0)
        if output_format == "JPEG":
            jpeg_quality = st.slider("Qualidade JPEG:", 70, 100, 95)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload da Imagem")
        uploaded_files = st.file_uploader(
            "Escolha as imagens:",
            type=['png', 'jpg', 'jpeg', 'webp', 'bmp'],
            accept_multiple_files=True,
            help="Formatos suportados: PNG, JPG, JPEG, WEBP, BMP"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} imagem(ns) carregada(s)")
            
            # Preview first image
            if len(uploaded_files) > 0:
                preview_image = Image.open(uploaded_files[0])
                st.image(preview_image, caption=f"Preview: {uploaded_files[0].name}", use_container_width=True)
                st.info(f"Tamanho original: {preview_image.size[0]}x{preview_image.size[1]} pixels")
                
                # Calculate new size
                new_width = int(preview_image.size[0] * scale_factor)
                new_height = int(preview_image.size[1] * scale_factor)
                st.info(f"Tamanho após upscaling: {new_width}x{new_height} pixels")
    
    with col2:
        st.header("🚀 Resultado do Upscaling")
        
        if uploaded_files and st.button("▶️ Iniciar Upscaling", type="primary"):
            
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Initialize upscaler
                if upscaler_type == "Avançado (Recomendado)" and ADVANCED_AVAILABLE:
                    upscaler = AdvancedUpscaler()
                elif upscaler_type == "Unificado" and UNIFIED_AVAILABLE:
                    upscaler = UnifiedUpscaler()
                else:
                    upscaler = None
                
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.text(f"Processando {uploaded_file.name}...")
                    
                    # Load image
                    image = Image.open(uploaded_file)
                    original_size = image.size
                    
                    try:
                        # Upscale based on selected method
                        if upscaler_type == "Avançado (Recomendado)" and ADVANCED_AVAILABLE:
                            result_image, method_used = upscaler.upscale_smart_auto(
                                image, scale_factor, quality
                            )
                        elif upscaler_type == "Unificado" and UNIFIED_AVAILABLE:
                            result_image, method_used = upscaler.upscale_smart(
                                image, scale_factor
                            )
                        else:
                            # Simple PIL upscaling
                            new_width = int(original_size[0] * scale_factor)
                            new_height = int(original_size[1] * scale_factor)
                            result_image = image.resize((new_width, new_height), Image.LANCZOS)
                            method_used = "PIL LANCZOS"
                        
                        # Post-processing if enabled
                        if apply_post_processing:
                            result_image = apply_post_processing_filters(result_image)
                        
                        # Store result
                        results.append({
                            'name': uploaded_file.name,
                            'original': image,
                            'result': result_image,
                            'method': method_used,
                            'original_size': original_size,
                            'new_size': result_image.size
                        })
                        
                    except Exception as e:
                        st.error(f"Erro ao processar {uploaded_file.name}: {e}")
                        # Fallback to simple upscaling
                        new_width = int(original_size[0] * scale_factor)
                        new_height = int(original_size[1] * scale_factor)
                        result_image = image.resize((new_width, new_height), Image.LANCZOS)
                        
                        results.append({
                            'name': uploaded_file.name,
                            'original': image,
                            'result': result_image,
                            'method': "PIL LANCZOS (fallback)",
                            'original_size': original_size,
                            'new_size': result_image.size
                        })
                    
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                status_text.text("✅ Processamento concluído!")
                
                # Display results
                if results:
                    st.success(f"🎉 {len(results)} imagem(ns) processada(s) com sucesso!")
                    
                    # Show first result as preview
                    result = results[0]
                    st.image(
                        result['result'], 
                        caption=f"Resultado: {result['name']} ({result['method']})",
                        use_container_width=True
                    )
                    
                    # Show comparison
                    with st.expander("📊 Comparação Antes/Depois"):
                        col_before, col_after = st.columns(2)
                        with col_before:
                            st.image(result['original'], caption="Original", use_container_width=True)
                            st.text(f"Tamanho: {result['original_size']}")
                        with col_after:
                            st.image(result['result'], caption="Upscaled", use_container_width=True)
                            st.text(f"Tamanho: {result['new_size']}")
                    
                    # Create download section
                    create_download_section(results, output_format, jpeg_quality if output_format == "JPEG" else None)
                    
            except Exception as e:
                st.error(f"Erro geral no processamento: {e}")
                st.exception(e)

def apply_post_processing_filters(image):
    """Apply post-processing filters to enhance image quality"""
    try:
        from PIL import ImageEnhance, ImageFilter
        
        # Slight sharpening
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.1)
        
        # Contrast enhancement
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.05)
        
        return image
    except Exception:
        return image

def create_download_section(results, output_format, jpeg_quality=None):
    """Create download section for processed images"""
    st.header("💾 Download dos Resultados")
    
    if len(results) == 1:
        # Single file download
        result = results[0]
        img_bytes = get_image_bytes(result['result'], output_format, jpeg_quality)
        
        filename = f"upscaled_{result['name'].split('.')[0]}.{output_format.lower()}"
        
        st.download_button(
            label=f"⬇️ Download {filename}",
            data=img_bytes,
            file_name=filename,
            mime=f"image/{output_format.lower()}"
        )
        
        # Show file info
        st.info(f"""
        **Informações do arquivo:**
        - Nome: {filename}
        - Formato: {output_format}
        - Tamanho: {result['new_size'][0]}x{result['new_size'][1]} pixels
        - Método: {result['method']}
        """)
    
    else:
        # Multiple files - create ZIP
        zip_bytes = create_zip_download(results, output_format, jpeg_quality)
        
        st.download_button(
            label=f"⬇️ Download ZIP ({len(results)} arquivos)",
            data=zip_bytes,
            file_name=f"upscaled_images_{len(results)}_files.zip",
            mime="application/zip"
        )
        
        # Show summary
        st.info(f"""
        **Resumo do processamento:**
        - {len(results)} imagens processadas
        - Formato de saída: {output_format}
        - Fator de escala aplicado: {st.session_state.get('scale_factor', 'N/A')}
        """)

def get_image_bytes(image, format_type, quality=None):
    """Convert PIL image to bytes"""
    img_byte_arr = io.BytesIO()
    
    if format_type == "JPEG":
        # Convert to RGB if necessary
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        image.save(img_byte_arr, format=format_type, quality=quality or 95)
    else:
        image.save(img_byte_arr, format=format_type)
    
    return img_byte_arr.getvalue()

def create_zip_download(results, output_format, jpeg_quality=None):
    """Create ZIP file with all processed images"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for result in results:
            img_bytes = get_image_bytes(result['result'], output_format, jpeg_quality)
            filename = f"upscaled_{result['name'].split('.')[0]}.{output_format.lower()}"
            zip_file.writestr(filename, img_bytes)
    
    return zip_buffer.getvalue()

def show_info_section():
    """Show information about available methods"""
    with st.sidebar.expander("ℹ️ Sobre os Métodos"):
        st.markdown("""
        **Métodos Disponíveis:**
        
        🔴 **Avançado (Recomendado):**
        - Múltiplos algoritmos de IA
        - HuggingFace ESRGAN
        - APIs online (Waifu2x)
        - OpenCV avançado
        
        🟡 **Unificado:**
        - OpenCV otimizado
        - PIL aprimorado
        - Pós-processamento
        
        🟢 **Simples:**
        - PIL LANCZOS
        - Sempre funciona
        - Rápido e confiável
        """)

if __name__ == "__main__":
    show_info_section()
    main()
