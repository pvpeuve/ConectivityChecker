#!/usr/bin/env python3
"""
Verificador de Conectividad - Aplicación Streamlit con Navigation
"""

import streamlit as st
from pages import urls, ips

st.set_page_config(
    page_title="Verificador de Conectividad", 
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Configurar navegación multi-página con secciones
pg = st.navigation({
    "Herramientas": [
        st.Page(urls.urls_page, title="🌐 Verificar URL"),
        st.Page(ips.ips_page, title="🌍 Verificar IP")
    ],
    "Análisis": [
        st.Page("pages/analytics.py", title="📊 Análisis")
    ]
})  

# Ejecutar la página seleccionada
pg.run()

# Footer
st.markdown("---")
st.text("Verificador de Conectividad | Hecho con ❤️ usando Streamlit")