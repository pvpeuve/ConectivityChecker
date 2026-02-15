#!/usr/bin/env python3
"""
Página de verificación de URLs - Streamlit
"""
import streamlit as st
from managers.url_manager import URLManager
from managers.analytics_manager import AnalyticsManager

def urls_page():
    st.header("🌐 Verificación de URLs")
    st.markdown("Verifica la conectividad de sitios web y APIs HTTP/HTTPS")
    
    # Inicializar analytics manager en session state
    if 'analytics_manager' not in st.session_state:
        st.session_state.analytics_manager = AnalyticsManager()
    
    # Crear instancia del manager
    url_manager = URLManager()
    url_manager.set_analytics_callback(st.session_state.analytics_manager)
    # GUI (form) para ingresar URL
    with st.form("url_verification_form"):
        url_address = st.text_input(label="Dirección Web", placeholder="https://google.com, https://github.com, etc.", key="url_input")
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
                    ["Manual", "https", "http", "ftp", "ws", "wss"],
                    index=0,
                    key="protocol_select"
                )
                # Extensión
                extension = st.selectbox(
                    "Extensión:",
                    ["Manual", ".com", ".io", ".org", ".net", ".dev", ".tech", ".app", ".es", ".fr", ".de", ".it", ".co", ".ai", ".xyz", ".me"],
                    index=0,
                    key="extension_select"
                )
            with subcol2:
                # Puerto
                port = st.selectbox(
                    "Puerto:",
                    ["Manual", 80, 443, 8080, 3000, 5000, 8000],
                    index=0,
                    key="port_select"
                )
                # Path adicional
                path = st.text_input("Path adicional:", placeholder="/api/v1/users", key="path_input")
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
        # Configurar parámetros del target
        url_manager.set_target_params(url_address, protocol, port, path, extension, timeout, retries, allow_redirects, verify_ssl)
        # Construir target usando el manager
        preview_target = url_manager.build_target()
        # Mostrar previsualización
        if preview_target:
            with st.spinner("Preparando URL..."):
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

    # Procesamiento del formulario
    if submitted:
        if not url_address:
            st.warning("Es necesario ingresar una URL")
            status_type = None
            message = None
        else:
            # Configurar parámetros del target
            url_manager.set_target_params(url_address, protocol, port, path, extension, timeout, retries, allow_redirects, verify_ssl)
            # Construir target usando el manager
            url_manager.build_target()
            # Mostrar URL que se va a verificar y enlace para abrir
            if url_manager.target:
                with st.spinner(f"Verificando conectividad..."):
                    status_type, message = url_manager.check_connectivity()

    # ==============================================================================
    # 3. VISUALIZACIÓN - Mostrar resultados
    # ==============================================================================

    # Mostrar resultados del procesamiento
    if submitted and status_type and message:
        if status_type == "Éxito":
            target_result.success(message)
            link_button.markdown(f"[Abrir]({url_manager.target})")
        elif status_type == "Advertencia":
            target_result.warning(message)
            link_button.empty()
        else:
            target_result.error(message)
            link_button.empty()