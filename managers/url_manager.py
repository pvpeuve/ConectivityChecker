#!/usr/bin/env python3
import requests
from managers.base_manager import BaseManager
from data.status_codes_dicts import HTTP_STATUS_DICT

class URLManager(BaseManager):
    """
    Clase para construir URLs y verificar conectividad

    Methods:
        set_settings: Configura la estructura de la URL y los parámetros de conectividad
        build_target: Construye la URL final
        check_connectivity: Verifica la conectividad de una URL

    """
    def __init__(self):
        super().__init__()
        self.protocol = None
        self.url_address = None
        self.port = None
        self.path = None
        self.extension = None

    def set_target_params(self, url_address, protocol=None, port=None, path=None, extension=None, timeout=None, retries=None, allow_redirects=None, verify_ssl=None):
        """
        Configurar los componentes de la URL y los parámetros de conectividad
        
        Args:
            url_address (str): URL base.
            protocol (str, optional): Protocolo. Defaults to None.
            port (int, optional): Puerto. Defaults to None.
            path (str, optional): Ruta. Defaults to None.
            extension (str, optional): Extensión. Defaults to None.
            timeout (int, optional): Tiempo máximo de espera en segundos. Defaults to None
            retries (int, optional): Número de reintentos. Defaults to None
            allow_redirects (bool, optional): Permitir redirecciones. Defaults to None
            verify_ssl (bool, optional): Verificar certificados SSL. Defaults to None
        """
        # Asignar componentes (dejar None si es Manual)
        self.url_address = url_address
        self.protocol = protocol if protocol != "Manual" else None
        self.extension = extension if extension != "Manual" else None
        self.port = port if port != "Manual" else None
        self.path = path if path != "Manual" else None

        # Parámetros de conectividad
        self.timeout = timeout
        self.retries = retries
        self.allow_redirects = allow_redirects
        self.verify_ssl = verify_ssl

        # Clase base
        self.target = url_address

    def build_target(self):
        """
        Construir URL completa con los componentes guardados en la clase
        
        Steps:
            1. Validar que la URL base exista
            2. Construir lista de componentes y unir

        Returns:
            str: URL completa construida
        """
        if self.url_address is None:
            raise ValueError("url_address cannot be None or empty")
        
        # Construir lista de componentes (solo los que no son None)
        components = [
            self.protocol + "://" if self.protocol else "",
            self.url_address,
            self.extension if self.extension else "",
            f":{self.port}" if self.port else "",
            self.path if self.path else ""
        ]
        
        # Unir todos los componentes
        self.target = "".join(components)
        return self.target

    def check_connectivity(self):
        """
        Verifica la conectividad de una URL

        Steps:
            1. Validar que la dirección final exista
            2. Hacer la petición HTTP
            3. Analizar el status code
            4. Guardar el resultado
            
        Returns:
            tuple: (estado, mensaje)
        """
        import time
        start_time = time.time()
        
        try:
            response = requests.get(
                self.target, 
                timeout=self.timeout, 
                allow_redirects=self.allow_redirects,
                verify=self.verify_ssl
            )           
                
        except requests.exceptions.MissingSchema as e:
            if "No scheme supplied" in str(e):
                self.result = ("Error", "❌ Error de URL: Falta http:// o https://")
            else:
                self.result = ("Error", "❌ Error de URL: " + str(e))
            self._send_to_analytics(time.time() - start_time)
            return self.result
        except requests.exceptions.ConnectionError as e:
            if "Name or service not known" in str(e):
                self.result = ("Error", "❌ Error de DNS: Dominio no encontrado")
            elif "Connection refused" in str(e):
                self.result = ("Error", "❌ Conexión rechazada: Servidor no disponible")
            else:
                self.result = ("Error", "❌ Error de conexión: " + str(e))
            self._send_to_analytics(time.time() - start_time)
            return self.result
        except requests.exceptions.Timeout as e:
            self.result = ("Error", "❌ Timeout: " + str(e))
            self._send_to_analytics(time.time() - start_time)
            return self.result
        except requests.exceptions.RequestException as e:
            self.result = ("Error", "❌ Error de solicitud: " + str(e))
            self._send_to_analytics(time.time() - start_time)
            return self.result
        
        status_type, base_message = HTTP_STATUS_DICT.get(response.status_code, ("Error", f"⚠️ Error HTTP"))
        self.result = (status_type, f"{base_message}: {response.status_code}")
        
        # Enviar a analytics
        self._send_to_analytics(time.time() - start_time)
        
        return self.result

    def set_analytics_callback(self, manager):
        """Configurar callback para analytics"""
        self.analytics_callback = manager
    
    def _extract_error_type(self, message):
        """Extraer tipo de error del mensaje"""
        if "Timeout" in message:
            return "timeout"
        elif "DNS" in message or "Dominio no encontrado" in message:
            return "dns_error"
        elif "Conexión rechazada" in message:
            return "connection_refused"
        elif "URL" in message:
            return "url_error"
        elif "SSL" in message or "certificado" in message.lower():
            return "ssl_error"
        else:
            return "unknown"
    
    def _send_to_analytics(self, response_time):
        """Enviar datos a analytics si hay callback configurado"""
        if hasattr(self, 'analytics_callback') and self.analytics_callback:
            import time
            analytics_data = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "url",
                "target": self.target,
                "status": self.result[0],
                "response_time": response_time,
                "protocol": self.protocol,  
                "port": self.port,        
                "error_type": self._extract_error_type(self.result[1]) if self.result[0] == "Error" else None
            }
            self.analytics_callback.add_data(analytics_data)

if __name__ == "__main__":
    url_manager = URLManager()
    url_manager.set_target_params("https://", None, "/get", None, "httpbin.org", 5, 1, True, True)
    url_manager.build_target()
    print("Target:", url_manager.target)
    status_type, message = url_manager.check_connectivity()
    print(status_type, " - ", message)