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

    def set_settings(self, protocol=None, port=None, path=None, extension=None, url_address=None, timeout=None, retries=None, allow_redirects=None, verify_ssl=None):
        """
        Configurar los componentes de la URL y los parámetros de conectividad
        
        Args:
            protocol (str, optional): Protocolo. Defaults to None.
            port (int, optional): Puerto. Defaults to None.
            path (str, optional): Ruta. Defaults to None.
            extension (str, optional): Extensión. Defaults to None.
            url_address (str, optional): URL base. Defaults to None.
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
        Construye URL completa con los componentes guardados en la clase
        
        Steps:
            1. Validar que la URL base exista
            2. Crear lista de componentes en orden de construcción y procesarla
            3. Unir componentes con '/' y retornar

        Returns:
            str: URL completa construida
        """
        if not self.url_address:
            return None
        
        components = [
            self.protocol,
            self.url_address,
            self.extension,
            f":{self.port}" if self.port is not None else None,
            self.path if self.path else None
        ]
        url_components = []
        for component in components:
            if component is not None:
                url_components.append(component)
        
        self.final_target = "".join(url_components)
        return self.final_target

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
        # Si no se ha construido la dirección final, construirla
        if not self.final_target:
            self.final_target = self.build_target()

        try:
            response = requests.get(
                self.final_target, 
                timeout=self.timeout, 
                allow_redirects=self.allow_redirects,
                verify=self.verify_ssl
            )           
                
        except requests.exceptions.MissingSchema as e:
            if "No scheme supplied" in str(e):
                self.result = ("Error", "❌ Error de URL: Falta http:// o https://")
            else:
                self.result = ("Error", f"❌ Error de URL: {str(e)}")
            return self.result
        except requests.exceptions.ConnectionError as e:
            if "Name or service not known" in str(e):
                self.result = ("Error", "❌ Error de DNS: Dominio no encontrado")
            elif "Connection refused" in str(e):
                self.result = ("Error", "❌ Conexión rechazada: Servidor no disponible")
            else:
                self.result = ("Error", f"❌ Error de conexión: {str(e)}")
            return self.result
        except requests.exceptions.Timeout as e:
            self.result = ("Error", f"❌ Timeout: {str(e)}")
            return self.result
        except requests.exceptions.RequestException as e:
            self.result = ("Error", f"❌ Error de solicitud: {str(e)}")
            return self.result
        
        status_type, base_message = HTTP_STATUS_DICT.get(response.status_code, ("Error", f"⚠️ Error HTTP"))
        self.result = (status_type, f"{base_message}: {response.status_code}")
        return self.result

if __name__ == "__main__":
    url_manager = URLManager()
    url_manager.set_settings("https://", None, "/get", None, "httpbin.org", 5, 1, True, True)
    status_type, message = url_manager.check_connectivity()
    print(status_type, " - ", message)