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
        # Asignar componentes (dejar None si es Manual)
        self.ip_address = ip_address
        self.port = port if port != "Manual" else None
        self.protocol = protocol if protocol != "Manual" else "tcp"

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
            1. Validar que la IP base exista
            2. Construir lista de componentes y unir

        Returns:
            str: IP completa construida
        """
        if self.ip_address is None:
            raise ValueError("ip_address cannot be None or empty")
        
        # Construir lista de componentes (solo los que no son None)
        components = [
            self.ip_address,
            f":{self.port}" if self.port else ""
        ]
        
        # Unir todos los componentes
        self.target = "".join(components)
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
        import time
        start_time = time.time()
        
        try:
            ip, port = self.target.split(":")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout or 3)
            # Actualizar self.port con el puerto real del target
            self.port = int(port)
            socket_result = sock.connect_ex((ip, int(port)))
            sock.close()
        except ValueError:
            self.result = ("Error", "❌ Formato inválido: Debe ser <IP> : <PUERTO>")
            self._handle_exception(start_time)
            return self.result
        except socket.timeout:
            self.result = ("Error", f"❌ Timeout conectando a {self.target}")
            self._handle_exception(start_time)
            return self.result
        except socket.error as e:
            self.result = ("Error", f"❌ Error de socket: {str(e)}")
            self._handle_exception(start_time)
            return self.result
        except Exception as e:
            self.result = ("Error", f"❌ Error de conexión: {str(e)}")
            self._handle_exception(start_time)
            return self.result
        status_type, message_template = SOCKET_STATUS_DICT.get(
            socket_result, 
            ("Error", f"❌ Error de conexión ({socket_result}) a {ip}:{port}")
        )
        # Reemplazar placeholders en el mensaje
        message = message_template.format(port=port, ip=ip)
        self.result = (status_type, message)

        # Guardar los datos de la entrada para acceso externo
        self.request_data = {
            "target": self.target,
            "protocol": self.protocol,
            "port": self.port,
            "timeout": self.timeout,
            "retries": self.retries
        }

        # Guardar los datos de la respuesta para acceso externo
        self.response_data = {
            'socket_code': socket_result,
            'response_time': time.time() - start_time,
            'host_info': socket.gethostbyname(ip) if ':' not in ip else ip,
            'connection_type': 'IPv4' if '.' in ip else 'IPv6'
        }

        # Guardar los datos de metadata para acceso externo
        self.request_metadata = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "ip",
            "status": self.result[0],
            "error_type": self._extract_error_type(self.result[1]) if self.result[0] == "Error" else None
        }
        
        # Enviar a analytics
        self._send_to_analytics(self.request_data, self.response_data, self.request_metadata)
        
        return self.result

    def _handle_exception(self, start_time):
        """Manejar excepción usando datos centralizados"""
        request_data, response_data, request_metadata = self._create_exception_data(start_time, self.result)
        
        # Asignar como atributos para que los tests los encuentren
        self.request_data = request_data
        self.response_data = response_data
        self.request_metadata = request_metadata
        
        self._send_to_analytics(request_data, response_data, request_metadata)
    
    def _create_exception_data(self, start_time, error_result):
        """
        Crear datos de excepción para analytics
        
        Args:
            start_time: Tiempo de inicio
            error_result: Tupla (status, message)
        
        Returns:
            tuple: (request_data, response_data, request_metadata)
        """
        import time
        request_data = {
            "target": getattr(self, 'target', None),
            "protocol": getattr(self, 'protocol', None),
            "port": getattr(self, 'port', None),
            "timeout": getattr(self, 'timeout', None),
            "retries": getattr(self, 'retries', None)
        }
        response_data = {
            'response_time': time.time() - start_time,
            'socket_code': None,
            'host_info': None,
            'connection_type': None
        }
        request_metadata = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "ip",  
            "status": error_result[0],
            "error_type": self._extract_error_type(error_result[1]) if hasattr(self, '_extract_error_type') else None
        }
        return request_data, response_data, request_metadata
    
    def set_analytics_callback(self, manager):
        """Configurar callback para analytics"""
        self.analytics_callback = manager
    
    def _extract_error_type(self, message):
        """Extraer tipo de error del mensaje"""
        if "Timeout" in message:
            return "timeout"
        elif "conexión" in message or "connection" in message.lower():
            return "connection_refused"
        elif "Formato inválido" in message:
            return "invalid_format"
        elif "socket" in message.lower():
            return "socket_error"
        else:
            return "unknown"
    
    def _send_to_analytics(self, request_data, response_data, request_metadata):
        """Enviar datos a analytics si hay callback configurado"""
        if hasattr(self, 'analytics_callback') and self.analytics_callback:
            complete_data = {**request_data, **response_data, **request_metadata}
            self.analytics_callback.add_data(complete_data)

if __name__ == "__main__":
    ip_manager = IPManager()
    ip_manager.set_target_params("127.0.0.1", 8080, "tcp", 5, 1, True, True)
    ip_manager.build_target()
    print("Target:", ip_manager.target)
    status_type, message = ip_manager.check_connectivity()
    print(status_type, " - ", message)