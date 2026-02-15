#!/usr/bin/env python3
import pandas as pd
from collections import defaultdict

class AnalyticsManager:
    """
    Clase para manejar los datos de análisis
    """
    def __init__(self):
        self.data = []
    
    def add_data(self, data):
        """Agregar datos"""
        self.data.append(data)
    
    def get_data(self):
        """Obtener datos"""
        return self.data
    
    def get_total_checks(self):
        """Obtener total de verificaciones"""
        return len(self.data)
    
    def get_success_rate(self):
        """Obtener tasa de éxito"""
        if not self.data:
            return 0.0
        successful = sum(1 for item in self.data if item['status'] == 'Éxito')
        return (successful / len(self.data)) * 100
    
    def get_checks_by_type(self):
        """Obtener verificaciones por tipo (url/ip)"""
        type_counts = defaultdict(int)
        for item in self.data:
            type_counts[item['type']] += 1
        return dict(type_counts)
    
    def get_checks_by_status(self):
        """Obtener verificaciones por estado"""
        status_counts = defaultdict(int)
        for item in self.data:
            status_counts[item['status']] += 1
        return dict(status_counts)
    
    def get_error_types(self):
        """Obtener tipos de error"""
        error_counts = defaultdict(int)
        for item in self.data:
            if item['error_type']:
                error_counts[item['error_type']] += 1
        return dict(error_counts)
    
    def get_average_response_time(self):
        """Obtener tiempo de respuesta promedio"""
        if not self.data:
            return 0.0
        response_times = [item['response_time'] for item in self.data]
        return sum(response_times) / len(response_times)
    
    def get_data_for_chart(self):
        """Obtener datos formateados para gráficos"""
        if not self.data:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df