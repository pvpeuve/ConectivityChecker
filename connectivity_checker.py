import requests

class URLManager:
    def __init__(self):
        """
        Inicializa el manejador de URLs

        Methods:
            set_connectivity_settings: Configura los parámetros de conectividad
            set_url_settings: Establece la URL a verificar
            check_connectivity: Verifica la conectividad de una URL
            build_url: Construye la URL final

        """
        return

    def set_connectivity_settings(self, timeout=None, retries=None, allow_redirects=None, verify_ssl=None):
        """
        Configura los parámetros de conectividad

        Args:
            timeout (int, optional): Tiempo máximo de espera en segundos. Defaults to None
            retries (int, optional): Número de reintentos. Defaults to None
            allow_redirects (bool, optional): Permitir redirecciones. Defaults to None
            verify_ssl (bool, optional): Verificar certificados SSL. Defaults to None
        """
        self.timeout = timeout
        self.retries = retries
        self.allow_redirects = allow_redirects
        self.verify_ssl = verify_ssl
        return

    def check_connectivity(self):
        """
        Verifica la conectividad de una URL

        Steps:
            1. Hacer la petición HTTP
            2. Analizar el status code
            3. Guardar el resultado
            
        Returns:
            tuple: (estado, mensaje)
        """
        
        status_dict = {
            200: ("Éxito", f"✅ Conexión exitosa"),
            400: ("Advertencia", f"❌ Solicitud incorrecta"),
            401: ("Advertencia", f"🔒 No autorizado"),
            403: ("Error", f"🚫 Acceso denegado"),
            404: ("Error", f"❓ Página no encontrada")
            }

        try:
            response = requests.get(
                self.final_url, 
                timeout=self.timeout, 
                allow_redirects=self.allow_redirects,
                verify=self.verify_ssl
            )

            status_type, base_message = status_dict.get(response.status_code, ("Error", f"⚠️ Error HTTP"))
            self.result = (status_type, f"{base_message}: {response.status_code}")
                
        except requests.exceptions.MissingSchema as e:
            if "No scheme supplied" in str(e):
                self.result = ("Error", "❌ Error de URL: Falta http:// o https://")
            else:
                self.result = ("Error", f"❌ Error de URL: {str(e)}")
        except requests.exceptions.ConnectionError as e:
            if "Name or service not known" in str(e):
                self.result = ("Error", "❌ Error de DNS: Dominio no encontrado")
            elif "Connection refused" in str(e):
                self.result = ("Error", "❌ Conexión rechazada: Servidor no disponible")
            else:
                self.result = ("Error", f"❌ Error de conexión: {str(e)}")
        except requests.exceptions.Timeout as e:
            self.result = ("Error", f"❌ Timeout: {str(e)}")
        except requests.exceptions.RequestException as e:
            self.result = ("Error", f"❌ Error de solicitud: {str(e)}")

        return self.result
    
    def set_url_settings(self, protocol=None, port=None, path=None, extension=None, base_url=None):
        """
        Configura los componentes de la URL
        
        Args:
            protocol (str, optional): Protocolo. Defaults to None.
            port (int, optional): Puerto. Defaults to None.
            path (str, optional): Ruta. Defaults to None.
            extension (str, optional): Extensión. Defaults to None.
            base_url (str, optional): URL base. Defaults to None.
        """
        self.protocol = protocol
        self.base_url = base_url
        self.port = port
        self.path = path
        self.extension = extension
        return

    def build_url(self):
        """
        Construye URL completa con los componentes guardados en la clase
        
        Steps:
            1. Validar que la URL base exista
            2. Limpiar la URL base de protocolos existentes
            3. Crear lista de componentes en orden de construcción
            4. Crear lista de componentes procesados
            5. Iterar y añadir componentes que no sean None
            6. Unir componentes con '/' y retornar

        Returns:
            str: URL completa construida
        """
        if not self.base_url:
            return None
        
        cleaned_url = self.base_url.replace('http://', '').replace('https://', '').strip('/')
        
        components = [
            self.protocol,
            cleaned_url,
            self.extension,
            f":{self.port}" if self.port is not None else None,
            self.path if self.path else None
        ]
        
        url_components = []

        for component in components:
            if component is not None:
                url_components.append(component)
        
        self.final_url = "".join(url_components)

        return self.final_url
