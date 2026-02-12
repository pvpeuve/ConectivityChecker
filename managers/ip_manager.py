#! /usr/bin/env python3
from managers.base_manager import BaseManager
from data.status_codes_dicts import SOCKET_STATUS_DICT
import socket
class IPManager(BaseManager):
    """
    Clase para construir IPs y verificar conectividad

    Methods:
        set_settings: Configura la IP y los parámetros de conectividad
        build_target: Construye la IP final
        check_connectivity: Verifica la conectividad de una IP
        check_tcp_socket: Verifica puerto TCP con socket

    """
    def __init__(self):
        super().__init__()
        self.protocol = None
        self.ip_address = None
        self.port = None

    def set_target_params(self, ip_address, port=None, protocol="tcp", timeout=None, retries=None, allow_redirects=None, verify_ssl=None):
        """
        Configurar los componentes de la IP y los parámetros de conectividad
        
        Args:
            ip_address (str): Dirección IP.
            port (int, optional): Puerto. Defaults to None.
            protocol (str, optional): Protocolo. Defaults to "tcp".
            timeout (int, optional): Tiempo máximo de espera en segundos. Defaults to None
            retries (int, optional): Número de reintentos. Defaults to None
            allow_redirects (bool, optional): Permitir redirecciones. Defaults to None
            verify_ssl (bool, optional): Verificar certificados SSL. Defaults to None
        """
        # Componentes de la IP
        self.ip_address = ip_address
        self.port = port
        self.protocol = protocol

        # Parámetros de conectividad
        self.timeout = timeout
        self.retries = retries
        self.allow_redirects = allow_redirects
        self.verify_ssl = verify_ssl

        # Clase base
        self.target = ip_address

    def build_target(self):
        """
        Construir IP completa con los componentes guardados en la clase
        
        Steps:
            1. Validar que la URL base exista
            2. Formatear los componentes que no sean None o "Manual"
            3. Unir todos los componentes formateados

        Returns:
            str: IP completa construida
        """
        if self.ip_address is None:
            raise ValueError("ip_address cannot be None or empty")

        if self.port is None or self.port == "Manual":
            self.port = ""
        else:
            self.port = f":{self.port}"

        self.target = self.ip_address + self.port
        return self.target

    def check_connectivity(self):
        """
        Verificar conectividad IP usando el protocolo especificado

        Steps:
            1. Validar que la dirección final exista
            2. Llamar al método del protocolo especificado

        Returns:
            function: Método del protocolo especificado
        """
        # Si no se ha construido la dirección final, construirla
        if not self.target:
            raise ValueError("Target not built")

        if self.protocol == "tcp":
            return self.check_tcp_socket()

    def check_tcp_socket(self):
        """
        Verificar puerto TCP con socket

        Steps:
            1. Parsear IP y puerto
            2. Crear socket
            3. Configurar timeout
            4. Conectar
            5. Cerrar socket
            6. Analizar el status code
            7. Guardar el resultado
        """
        
        try:
            ip, port = self.target.split(":")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout or 3)
            socket_result = sock.connect_ex((ip, int(port)))
            sock.close()
        except ValueError:
            self.result = ("Error", "❌ Formato inválido: Debe ser <IP> : <PUERTO>")
            return self.result
        except socket.timeout:
            self.result = ("Error", f"❌ Timeout conectando a {self.target}")
            return self.result
        except socket.error as e:
            self.result = ("Error", f"❌ Error de socket: {str(e)}")
            return self.result
        except Exception as e:
            self.result = ("Error", f"❌ Error de conexión: {str(e)}")
            return self.result
        status_type, message_template = SOCKET_STATUS_DICT.get(
            socket_result, 
            ("Error", f"❌ Error de conexión ({socket_result}) a {ip}:{port}")
        )
        # Reemplazar placeholders en el mensaje
        message = message_template.format(port=port, ip=ip)
        self.result = (status_type, message)
        return self.result

if __name__ == "__main__":
    ip_manager = IPManager()
    ip_manager.set_target_params("127.0.0.1", 8080, "tcp", 5, 1, True, True)
    ip_manager.build_target()
    print("Target:", ip_manager.target)
    status_type, message = ip_manager.check_connectivity()
    print(status_type, " - ", message)