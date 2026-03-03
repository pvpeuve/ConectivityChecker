#!/usr/bin/env python3
"""
Página de verificación de IPs - Streamlit
"""
import streamlit as st
from managers.ip_manager import IPManager
from managers.analytics_manager import AnalyticsManager

def ips_page():
    st.header("🌍 Verificación de IPs")
    st.markdown("Verifica la conectividad de direcciones IP y puertos TCP")
    
    # Inicializar analytics manager en session state
    if 'analytics_manager' not in st.session_state:
        st.session_state.analytics_manager = AnalyticsManager()
    
    # Crear instancia del manager
    ip_manager = IPManager()
    ip_manager.set_analytics_callback(st.session_state.analytics_manager)
    # GUI (form) para ingresar IP
    with st.form("ip_verification_form"):
        ip_address = st.text_input(label="Dirección IP", placeholder="192.168.1.1, localhost, etc.", key="ip_input")
        form_col1, form_col2 = st.columns([4,1])
        with form_col1:
            submitted = st.form_submit_button("Verificar IP")
        with form_col2:
            # GUI (link) para mostrar el boton de enlace al resultado
            link_button = st.empty()
    # GUI (warning/info/error/success) para mostrar resultados de la verificación
    target_result = st.empty()

    # ==============================================================================
    # 1. CONFIGURACIÓN - Widgets y opciones
    # ==============================================================================

    # GUI (Tabs) para organizar la configuración
    tab1, tab2, tab3 = st.tabs(["⚙️ Configuración", "📊 Resultados", "❔ Ayuda"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Componentes:**")
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                # Protocolo
                protocol = st.selectbox("Protocolo:", ["tcp"], index=0, key="protocol_select")
                # Puerto
                port = st.selectbox("Puerto:", ["Manual", 22, 23, 25, 53, 3306, 5432], index=0, key="port_select")
            with subcol2:
                pass
        with col2:
            st.markdown("**Parámetros de Conexión:**")
            subcol1, subcol2 = st.columns(2)
            with subcol1:
                # Timeout
                timeout = st.number_input("Timeout (segundos):", min_value=1, max_value=60, value=3)
                # Reintentos
                retries = st.number_input("Reintentos:", min_value=1, max_value=10, value=1)
            with subcol2:
                pass
        # Configurar parámetros del target
        ip_manager.set_target_params(ip_address, port, protocol, timeout, retries)
        # Construir target usando el manager
        preview_target = ip_manager.build_target()
        # Mostrar previsualización
        if preview_target:
            with st.spinner("Preparando IP..."):
                st.text("Previsualización de la IP:")
                st.code(preview_target)
    with tab2:
        result_details_placeholder = st.empty()
    with tab3:
        with st.expander("💡 Casos de Uso Comunes"):
            st.markdown("""
            **🌐 Servicios de Red:**
            - `8.8.8.8:53` - DNS Google
            - `1.1.1.1:53` - DNS Cloudflare
            - `192.168.1.1:80` - Router local
            - `localhost:3000` - Desarrollo local
            
            **🔍 Herramientas Online:**
            - `208.67.222.222:53` - DNS OpenDNS
            - `9.9.9.9:53` - DNS Quad9
            - `1.0.0.1:53` - DNS Cloudflare secundario
            """)
        with st.expander("🧩 Componentes"):
            st.markdown("""
            **🌐 Dirección IP:** Identificador único en red
            - `192.168.1.1` - Red local privada
            - `8.8.8.8` - DNS público Google
            - `127.0.0.1` - Localhost
            
            **🔌 Protocolo:** Método de comunicación
            - `TCP` - Conexión fiable y ordenada
            - `UDP` - Conexión rápida sin confirmación
            
            **🚪 Puerto:** Servicio específico
            - `22` - SSH (acceso remoto)
            - `53` - DNS (resolución nombres)
            - `80` - HTTP (sitios web)
            - `443` - HTTPS (sitios seguros)
            """)
        with st.expander("📋 Estados de Verificación"):
            st.markdown("""
            **✅ Éxito:** Conexión establecida correctamente
            - Puerto abierto y respondiendo
            
            **⚠️ Advertencia:** Conexión con problemas menores
            - Conexión lenta, timeouts parciales
            
            **❌ Error:** No se pudo establecer conexión
            - Puerto cerrado, firewall, host inalcanzable
            
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
        if not ip_address:
            st.warning("Es necesario ingresar una IP")
            status_type = None
            message = None
        else:
            # Configurar parámetros del target
            ip_manager.set_target_params(ip_address, port, protocol, timeout, retries)
            # Construir target usando el manager
            ip_manager.build_target()
            # Mostrar IP que se va a verificar y enlace para abrir
            if ip_manager.target:
                with st.spinner(f"Verificando conectividad..."):
                    status_type, message = ip_manager.check_connectivity()

    # ==============================================================================
    # 3. VISUALIZACIÓN - Mostrar resultados
    # ==============================================================================

    # Mostrar resultados del procesamiento
    if submitted and ip_address and port and status_type and message:
        if status_type == "Éxito":
            target_result.success(message)
        elif status_type == "Advertencia":
            target_result.warning(message)
        else:
            target_result.error(message)
        
        # Mostrar datos enriquecidos si existen
        if hasattr(ip_manager, 'response_data'):
            response_data = ip_manager.response_data
            request_data = ip_manager.request_data
            request_metadata = ip_manager.request_metadata
            
            result_details_placeholder.code(f"""
🔧 DATOS DE ENTRADA
• Target: {request_data.get('target', 'N/A')}
• Protocolo: {request_data.get('protocol', 'N/A')}
• Puerto: {request_data.get('port', 'N/A')}
• Timeout: {request_data.get('timeout', 'N/A')}s
• Reintentos: {request_data.get('retries', 'N/A')}

📋 DATOS DE RESPUESTA
• Código Socket: {response_data.get('socket_code', 'N/A')}
• Tiempo de Respuesta: {response_data.get('response_time', 0):.3f}s
• Host Info: {response_data.get('host_info', 'N/A')}
• Tipo Conexión: {response_data.get('connection_type', 'N/A')}

📅 METADATOS
• Timestamp: {request_metadata.get('timestamp', 'N/A')}
• Type: {request_metadata.get('type', 'N/A')}
• Status: {request_metadata.get('status', 'N/A')}
• Error Type: {request_metadata.get('error_type', 'N/A')}""")
        else:
            # Mostrar mensaje informativo si no hay datos enriquecidos
            result_details_placeholder.info("🔍 Realiza una verificación para ver los datos enriquecidos")
    else:
        # Mostrar mensaje informativo en el placeholder
        result_details_placeholder.info("🔍 Realiza una verificación para ver los detalles aquí")