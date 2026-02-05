#!/usr/bin/env python3
import requests
from base_manager import BaseManager
from status_codes_dicts import HTTP_STATUS_DICT

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
        # Componentes de la URL
        self.protocol = protocol
        self.url_address = url_address
        self.port = port
        self.path = path
        self.extension = extension

        # Parámetros de conectividad
        self.timeout = timeout
        self.retries = retries
        self.allow_redirects = allow_redirects
        self.verify_ssl = verify_ssl

        # Clase base
        self.target = url_address
        return

    def build_target(self):
        """
        Construir URL completa con los componentes guardados en la clase
        
        Steps:
            1. Validar que la URL base exista
            2. Formatear los componentes que no sean None o "Manual"
            3. Unir todos los componentes formateados

        Returns:
            str: URL completa construida
        """
        if self.url_address is None:
            raise ValueError("url_address cannot be None or empty")
        
        if self.protocol is None or self.protocol == "Manual":
            self.protocol = ""
        else:
            self.protocol = self.protocol + "://"

        if self.extension is None or self.extension == "Manual":
            self.extension = ""

        if self.port is None or self.port == "Manual":
            self.port = ""
        else:
            self.port = f":{self.port}"
        
        if self.path is None:
            self.path = ""

        self.target = self.protocol + self.url_address + self.extension + self.port + self.path
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
            return self.result
        except requests.exceptions.ConnectionError as e:
            if "Name or service not known" in str(e):
                self.result = ("Error", "❌ Error de DNS: Dominio no encontrado")
            elif "Connection refused" in str(e):
                self.result = ("Error", "❌ Conexión rechazada: Servidor no disponible")
            else:
                self.result = ("Error", "❌ Error de conexión: " + str(e))
            return self.result
        except requests.exceptions.Timeout as e:
            self.result = ("Error", "❌ Timeout: " + str(e))
            return self.result
        except requests.exceptions.RequestException as e:
            self.result = ("Error", "❌ Error de solicitud: " + str(e))
            return self.result
        
        status_type, base_message = HTTP_STATUS_DICT.get(response.status_code, ("Error", f"⚠️ Error HTTP"))
        self.result = (status_type, f"{base_message}: {response.status_code}")
        return self.result

if __name__ == "__main__":
    url_manager = URLManager()
    url_manager.set_target_params("https://", None, "/get", None, "httpbin.org", 5, 1, True, True)
    url_manager.build_target()
    print("Target:", url_manager.target)
    status_type, message = url_manager.check_connectivity()
    print(status_type, " - ", message)