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
        submitted = st.form_submit_button("Verificar Web")
    # GUI (warning/info/error/success) para mostrar resultados de la verificación
    target_result = st.empty()

    # ==============================================================================
    # 1. CONFIGURACIÓN - Widgets y opciones
    # ==============================================================================

    # Tabs para organizar la configuración
    tab1, tab2, tab3 = st.tabs(["⚙️ Configuración", "📊 Resultados", "❔ Ayuda"])
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
        result_details_placeholder = st.empty()
        col1, col2, col3 = st.columns(3)
        with col1:
            copy_button_placeholder = st.empty()
        with col2:
            retry_button_placeholder = st.empty()
        with col3:
            open_button_placeholder = st.empty()

    with tab3:
        with st.expander("💡 Casos de Uso Comunes"):
            st.markdown("""
            **🌍 Sitios Web Populares:**
            - `https://google.com` - Motor de búsqueda
            - `https://github.com` - Repositorios de código
            - `https://stackoverflow.com` - Q&A programación
            - `https://api.github.com/users` - API pública
            
            **🔍 APIs y Servicios:**
            - `https://httpbin.org/status/200` - Test HTTP
            - `https://jsonplaceholder.typicode.com/posts` - API fake
            - `https://api.ipify.org` - Obtener IP pública
            - `https://reqres.in/api/users` - API REST test
            """)
        with st.expander("🧩 Componentes"):
            st.markdown("""
            **📍 Dirección Base:** URL principal sin protocolo
            - Ejemplo: `google.com` (no `https://`)
            
            **🔗 Protocolo:** Método de conexión
            - `https://` - Conexión segura (SSL/TLS)
            - `http://` - Conexión estándar (sin encriptar)
            - `ftp://` - Transferencia de archivos
            
            **🏷️ Extensión:** Dominio de nivel superior
            - `.com` - Comercial
            - `.io` - Tecnología
            - `.org` - Organización
            
            **🚪 Puerto:** Puerto específico
            - `80` - HTTP estándar
            - `443` - HTTPS estándar
            - `8080` - Desarrollo
            
            **🛤️ Path:** Ruta específica
            - `/api/v1/users` - Endpoint REST
            - `/admin` - Panel administración
            """)
        with st.expander("📋 Estados de Verificación"):
            st.markdown("""
            **✅ Éxito:** Conexión establecida correctamente
            - Código HTTP 2xx (200, 201, etc.)
            
            **⚠️ Advertencia:** Conexión con problemas menores
            - Redirecciones, certificados SSL débiles
            
            **❌ Error:** No se pudo establecer conexión
            - DNS no encontrado, timeout, SSL inválido
            
            **⏱️ Tiempos de Respuesta:**
            - **< 100ms:** Excelente
            - **100-500ms:** Bueno
            - **> 500ms:** Lento
            - **> 2000ms:** Muy lento
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
            copy_button_placeholder.button("📋 Copiar", key="copy", help="Copiar al portapapeles")
            retry_button_placeholder.button("🔄 Reintentar", key="retry", help="Volver a verificar")
            open_button_placeholder.button("🔗 Abrir", key="open", help="Abrir en nueva pestaña")
        elif status_type == "Advertencia":
            target_result.warning(message)
        else:
            target_result.error(message)
        # Actualizar el placeholder con los detalles
        result_details_placeholder.code(f"""Dirección verificada: {url_manager.target}
            Timeout: {timeout}s
            Reintentos: {retries}
            Status: {status_type}""")
    else:
        # Mostrar mensaje informativo en el placeholder
        result_details_placeholder.info("🔍 Realiza una verificación para ver los detalles aquí")