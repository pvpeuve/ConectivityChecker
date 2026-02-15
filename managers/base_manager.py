#!/usr/bin/env python3

class BaseManager:
    """
    Clase base para manejar la URL/dirección
    """
    def __init__(self):
        self.target = None
        self.final_target = None
        self.timeout = 3
        self.retries = 1
        self.allow_redirects = True
        self.verify_ssl = True
        self.result = None

    def set_settings(self, target, timeout=None, retries=None, allow_redirects=None, verify_ssl=None):
        """Configurar parámetros generales"""
        raise NotImplementedError("Subclass must implement set_settings")
    
    def build_target(self):
        """Construir el objetivo final (URL o IP con puerto)"""
        raise NotImplementedError("Subclass must implement build_target")
    
    def check_connectivity(self):
        """Verificar conectividad"""
        raise NotImplementedError("Subclass must implement check_connectivity")
    
    def _send_to_analytics(self, response_time):
        """Enviar datos a analytics si hay callback configurado"""
        raise NotImplementedError("Subclass must implement _send_to_analytics")