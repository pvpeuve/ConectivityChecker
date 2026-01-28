import streamlit as st
from connectivity_checker import URLManager

st.set_page_config(page_title="Verificador de Conectividad Web", page_icon="🌐", layout="wide")
st.title("Verificador de Conectividad Web")

# Crear instancia del manager
url_manager = URLManager()

# Formulario principal arriba
with st.form("verification_form"):
    url = st.text_input(label="Conexión a verificar")
    submitted = st.form_submit_button("Verificar")

# ==============================================================================
# 1. CONFIGURACIÓN - Widgets y opciones
# ==============================================================================

# Expander de opciones de request
with st.expander("🔧 Configuración de URL", expanded=True):
    
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

    # Previsualización en tiempo real
    st.markdown("---")
    
    # Actualizar configuración del manager principal para previsualización
    final_protocol = None if protocol == "Manual" else protocol
    final_extension = None if extension == "Manual" else extension
    final_port = None if port == "Manual" else port
    
    # Usar la URL del usuario o "ejemplo" si no ha escrito nada
    preview_url_input = url if url else "ejemplo"
    
    url_manager.set_url_settings(final_protocol, final_port, path, final_extension, preview_url_input)
    url_manager.set_connectivity_settings(timeout, retries, allow_redirects, verify_ssl)
    
    # Construir URL de previsualización
    preview_url = url_manager.build_url()
    
    # Mostrar previsualización con botón de abrir
    preview_col, button_col = st.columns([4, 1])
    with preview_col:
        st.text(preview_url)
    with button_col:
        link_button = st.empty()

# ==============================================================================
# 2. PROCESO - Formulario principal y lógica
# ==============================================================================

# Variables para resultados (inicializadas para evitar errores)
status_type = None
message = None
full_url = None

# Procesamiento del formulario
if submitted:
    if not url:
        st.warning("Por favor, ingresa una URL válida")
    else:
        # Guardar configuración de URL en la instancia
        final_protocol = None if protocol == "Manual" else protocol
        final_extension = None if extension == "Manual" else extension
        final_port = None if port == "Manual" else port
        
        url_manager.set_url_settings(final_protocol, final_port, path, final_extension, url)
        
        # Guardar configuración de conectividad en la instancia
        url_manager.set_connectivity_settings(timeout, retries, allow_redirects, verify_ssl)
        
        # Construir URL según las opciones seleccionadas
        if protocol == "Manual" and extension == "Manual" and port == "Manual":
            full_url = url  # Usa exactamente lo que escribió el usuario
        else:
            full_url = url_manager.build_url()
        
        # Mostrar URL que se va a verificar y enlace para abrir
        link_button.markdown(f"[Abrir]({full_url})")
        
        with st.spinner(f"Verificando conectividad a {full_url} ..."):
            status_type, message = url_manager.check_connectivity()

# ==============================================================================
# 3. VISUALIZACIÓN - Mostrar resultados
# ==============================================================================

# Mostrar resultados del procesamiento
if submitted and url and status_type and message:
    if status_type == "Éxito":
        st.success(message)
    elif status_type == "Advertencia":
        st.warning(message)
    else:
        st.error(message)

# ==============================================================================
# INFORMACIÓN ADICIONAL
# ==============================================================================

# Expander de configuración detallada
# with st.expander("📋 Configuración actual", expanded=False):
#     st.code(f"Protocolo: {protocol}")
#     st.code(f"Puerto: {port}")
#     st.code(f"Extensión: {extension}")
#     st.code(f"Path: {path or '/'}")
#     st.code(f"Timeout: {timeout}s")
#     st.code(f"Reintentos: {retries}")
#     st.code(f"Redirects: {allow_redirects}")
#     st.code(f"SSL Verify: {verify_ssl}")