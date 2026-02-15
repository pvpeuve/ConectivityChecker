#!/usr/bin/env python3
"""
Página de análisis - Streamlit
"""
import streamlit as st
import pandas as pd
from managers.analytics_manager import AnalyticsManager

# Inicializar analytics manager en session state
if 'analytics_manager' not in st.session_state:
    st.session_state.analytics_manager = AnalyticsManager()

analytics_manager = st.session_state.analytics_manager

st.title("📊 Analytics Dashboard")
st.markdown("---")

# Métricas principales
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_checks = analytics_manager.get_total_checks()
    st.metric("Total Verificaciones", total_checks)

with col2:
    success_rate = analytics_manager.get_success_rate()
    st.metric("Tasa de Éxito", f"{success_rate:.1f}%")

with col3:
    avg_response_time = analytics_manager.get_average_response_time()
    st.metric("Tiempo Promedio", f"{avg_response_time:.3f}s")

with col4:
    checks_by_type = analytics_manager.get_checks_by_type()
    ip_checks = checks_by_type.get('ip', 0)
    url_checks = checks_by_type.get('url', 0)
    st.metric("IPs vs URLs", f"{ip_checks}:{url_checks}")

st.markdown("---")

# Gráficos
if analytics_manager.get_data():
    # Gráfico de estado
    st.subheader("📈 Estado de Verificaciones")
    status_data = analytics_manager.get_checks_by_status()
    if status_data:
        st.bar_chart(status_data)
    
    # Gráfico de tipos
    st.subheader("🔍 Tipos de Verificación")
    type_data = analytics_manager.get_checks_by_type()
    if type_data:
        st.bar_chart(type_data)
    
    # Errores
    st.subheader("❌ Tipos de Error")
    error_data = analytics_manager.get_error_types()
    if error_data:
        st.bar_chart(error_data)
    
    # Timeline
    st.subheader("⏰ Línea de Tiempo")
    df = analytics_manager.get_data_for_chart()
    if not df.empty:
        # Agrupar por hora
        df['hour'] = df['timestamp'].dt.floor('H')
        timeline_data = df.groupby(['hour', 'status']).size().unstack(fill_value=0)
        st.line_chart(timeline_data)
    
    # Datos crudos
    st.subheader("📋 Datos Detallados")
    df_display = analytics_manager.get_data_for_chart()
    if not df_display.empty:
        st.dataframe(df_display, use_container_width=True)
else:
    st.info("📝 No hay datos de verificación aún. Realiza algunas verificaciones de URLs o IPs para ver los analytics.")