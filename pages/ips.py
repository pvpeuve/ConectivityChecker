#!/usr/bin/env python3
"""
Página de verificación de IPs - Streamlit
"""

import streamlit as st
from ip_manager import IPManager

def ips_page():
    st.header("🌍 Verificación de IPs")
    st.markdown("Verifica la conectividad de direcciones IP y puertos TCP")
    
    # Crear instancia del manager
    ip_manager = IPManager()
    
    # GUI (form) para ingresar IP
    with st.form("ip_verification_form"):
        ip_address = st.text_input(label="Dirección IP", placeholder="192.168.1.1, localhost, etc.")
        form_col1, form_col2 = st.columns([4,1])
        with form_col1:
            submitted = st.form_submit_button("Verificar IP")
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
                    ["tcp"],
                    index=0,
                    help="Actualmente solo soportamos TCP. UDP y ICMP próximamente."
                )
                # Puerto
                port = st.selectbox(
                    "Puerto:",
                    ["Manual", 22, 23, 25, 53, 3306, 5432],
                    index=0
                )
        
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
        
        # Construir target de previsualización
        if ip_address and port and port != "Manual":
            preview_target = f"{ip_address}:{port}"
        else:
            preview_target = "Dirección (ej: 192.168.1.1)"
        

        # Mostrar previsualización
        st.text("Previsualización de la IP:")
        st.code(preview_target)
    
    with tab2:
        st.markdown("## 📊 Información de la Verificación")
        
        # Placeholder para detalles (siempre existe)
        details_placeholder = st.empty()
        
        st.markdown("### ℹ️ Acerca de las Verificaciones IP")
        st.markdown("""
        - **Protocolo TCP**: Verifica conectividad directa mediante sockets
        - **Timeout**: Tiempo máximo de espera para la respuesta
        - **Reintentos**: Número de intentos en caso de fallo
        - **Puertos comunes**:
            - 22: SSH
            - 80: HTTP
            - 443: HTTPS
            - 53: DNS
            - 3306: MySQL
            - 5432: PostgreSQL
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
        if not ip_address:
            st.warning("Por favor, ingresa una dirección IP válida")
        elif not port or port == "Manual":
            st.warning("Por favor, selecciona un puerto válido")
        else:
            # Configurar IPManager
            ip_manager.set_settings(ip_address, port, protocol, timeout, retries)
            
            # Construir target
            full_target = ip_manager.build_target()
            
            with st.spinner(f"Verificando conectividad con {full_target}..."):
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

        # Actualizar el placeholder con los detalles
        details_placeholder.code(f"""Dirección verificada: {full_target}
Protocolo: {protocol.upper()}
Timeout: {timeout}s
Reintentos: {retries}
Status: {status_type}""")
    else:
        # Mostrar mensaje informativo en el placeholder
        details_placeholder.info("🔍 Realiza una verificación para ver los detalles aquí")

"""
### TODO: usar st.info y los parámetros help de los widgets.
# Información adicional (st.info):
    - "ℹ️ Las verificaciones de IP usan sockets TCP para probar la conectividad directa."
# Help:
    - "ℹ️ Las verificaciones de IP usan sockets TCP para probar la conectividad directa."
"""