#!/usr/bin/env python3
"""
Página de verificación de URLs - Streamlit
"""

import streamlit as st
from url_manager import URLManager

def urls_page():
    st.header("🌐 Verificación de URLs")
    st.markdown("Verifica la conectividad de sitios web y APIs HTTP/HTTPS")
    
    # Crear instancia del manager
    url_manager = URLManager()
    
    # GUI (form) para ingresar URL
    with st.form("verification_form"):
        url = st.text_input(label="Dirección Web", placeholder="https://google.com, https://github.com, etc.")
        form_col1, form_col2 = st.columns([4,1])
        with form_col1:
            submitted = st.form_submit_button("Verificar Web")
        with form_col2:
            link_button = st.empty()
    # GUI (warning/info/error/success) para mostrar resultados de la verificación
    target_result = st.empty()

    # ==============================================================================
    # 1. CONFIGURACIÓN - Widgets y opciones
    # ==============================================================================

    # Tabs para organizar la configuración
    tab1, tab2 = st.tabs(["⚙️ Configuración", "📊 Detalles"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:

            st.markdown("**Componentes:**")
            subcol1, subcol2 = st.columns(2)

            with subcol1:
                # Protocolo
                protocol = st.selectbox(
                    "Protocolo:",
                    ["Manual", "https://", "http://", "ftp://", "ws://", "wss://"],
                    index=0
                )
            
                # Extensión
                extension = st.selectbox(
                    "Extensión:",
                    ["Manual", ".com", ".io", ".org", ".net", ".dev", ".tech", ".app", ".es", ".fr", ".de", ".it", ".co", ".ai", ".xyz", ".me"],
                    index=0
                )
            
            with subcol2:
                # Puerto
                port = st.selectbox(
                    "Puerto:",
                    ["Manual", 80, 443, 8080, 3000, 5000, 8000],
                    index=0
                )
                
                # Path adicional
                path = st.text_input("Path adicional:", placeholder="/api/v1/users")
            
        with col2:

            st.markdown("**Parámetros de Conexión:**")
            subcol1, subcol2 = st.columns(2)

            with subcol1:
                # Timeout
                timeout = st.number_input("Timeout (segundos):", min_value=1, max_value=60, value=3)
            
                # Reintentos
                retries = st.number_input("Reintentos:", min_value=1, max_value=10, value=1)
            
            with subcol2:
                # Opciones básicas
                allow_redirects = st.checkbox("Seguir redirecciones", value=True)
                verify_ssl = st.checkbox("Verificar SSL", value=True)
        
        # Actualizar configuración del manager principal para previsualización
        final_protocol = None if protocol == "Manual" else protocol
        final_extension = None if extension == "Manual" else extension
        final_port = None if port == "Manual" else port
        
        # Usar la URL del usuario o "ejemplo" si no ha escrito nada
        preview_url_input = url if url else "Protocolo://Dirección (ej: https://google.com)"
        
        url_manager.set_settings(final_protocol, final_port, path, final_extension, preview_url_input, timeout, retries, allow_redirects, verify_ssl)
        
        # Construir URL de previsualización
        preview_target = url_manager.build_target()
        
        # Mostrar previsualización
        st.text("Previsualización de la URL:")
        st.code(preview_target)
    
    with tab2:
        st.markdown("## 📊 Información de la Verificación")
        
        # Placeholder para detalles (siempre existe)
        details_placeholder = st.empty()
        
        st.markdown("### ℹ️ Acerca de las Verificaciones URL")
        st.markdown("""
        - **Protocolos HTTP/HTTPS**: Verifica conectividad web mediante requests
        - **Timeout**: Tiempo máximo de espera para la respuesta HTTP
        - **Reintentos**: Número de intentos en caso de fallo
        - **Redirecciones**: Sigue automáticamente redireccionamientos 301/302
        - **SSL**: Verifica certificados HTTPS para conexiones seguras
        - **Protocolos comunes**:
          - **https://**: Conexión segura (puerto 443)
          - **http://**: Conexión estándar (puerto 80)
          - **ftp://**: Transferencia de archivos (puerto 21)
          - **ws://** / **wss://**: WebSockets (puertos 80/443)
        """)

    # ==============================================================================
    # 2. PROCESO - Formulario principal y lógica
    # ==============================================================================

    # Variables para resultados (inicializadas para evitar errores)
    status_type = None
    message = None
    full_target = None

    # Procesamiento del formulario
    if submitted:
        if not url:
            st.warning("Por favor, ingresa una URL válida")
        else:
            # Guardar configuración de URL en la instancia
            final_protocol = None if protocol == "Manual" else protocol
            final_extension = None if extension == "Manual" else extension
            final_port = None if port == "Manual" else port
            
            url_manager.set_settings(final_protocol, final_port, path, final_extension, url, timeout, retries, allow_redirects, verify_ssl)
            
            # Construir URL según las opciones seleccionadas
            if protocol == "Manual" and extension == "Manual" and port == "Manual":
                full_target = url  # Usa exactamente lo que escribió el usuario
            else:
                # check_connectivity() construirá la URL internamente
                full_target = None
            
            # Mostrar URL que se va a verificar y enlace para abrir
            if full_target:
                link_button.markdown(f"[Abrir]({full_target})")
            else:
                # check_connectivity() construirá y usará la URL
                pass
            
            with st.spinner(f"Verificando conectividad..."):
                status_type, message = url_manager.check_connectivity()
                
                # Obtener la URL final que se usó para la verificación
                if not full_target:
                    full_target = url_manager.final_target
                    link_button.markdown(f"[Abrir]({full_target})")

    # ==============================================================================
    # 3. VISUALIZACIÓN - Mostrar resultados
    # ==============================================================================

    # Mostrar resultados del procesamiento
    if submitted and url and status_type and message:
        if status_type == "Éxito":
            target_result.success(message)
        elif status_type == "Advertencia":
            target_result.warning(message)
        else:
            target_result.error(message)
