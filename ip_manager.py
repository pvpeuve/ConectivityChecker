#! /usr/bin/env python3
from base_manager import BaseManager
from status_codes_dicts import SOCKET_STATUS_DICT

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

    def set_settings(self, ip_address, port=None, protocol="tcp", timeout=None, retries=None, allow_redirects=None, verify_ssl=None):
        
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
            1. Validar que la IP base exista
            2. Crear lista de componentes en orden de construcción y procesarla
            3. Unir componentes con ':' y retornar

        Returns:
            str: IP completa construida
        """
        if not self.ip_address:
            return None
        
        components = [
            self.ip_address,
            f":{self.port}" if self.port is not None else None,
        ]
        ip_components = []
        for component in components:
            if component is not None:
                ip_components.append(component)
        
        self.final_target = "".join(ip_components)
        return self.final_target

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
        if not self.final_target:
            target = self.build_target()
        else:
            target = self.final_target

        if self.protocol == "tcp":
            return self.check_tcp_socket(target)

    def check_tcp_socket(self, target):
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
        import socket
        try:
            ip, port = target.split(":")
            port = int(port)

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            sock.settimeout(self.timeout or 3)

            result = sock.connect_ex((ip, port))

            sock.close()
            
        except ValueError:
            self.result = ("Error", "❌ Formato inválido. Usa IP:puerto")
            return self.result
        except socket.timeout:
            self.result = ("Error", f"❌ Timeout conectando a {target}")
            return self.result
        except Exception as e:
            self.result = ("Error", f"❌ Error de conexión: {str(e)}")
            return self.result
        
        status_type, message_template = SOCKET_STATUS_DICT.get(
            result, 
            ("Error", f"❌ Error de conexión ({result}) a {{ip}}:{{port}}")
        )
        
        # Reemplazar placeholders en el mensaje
        message = message_template.format(port=port, ip=ip)
        
        self.result = (status_type, message)
        return self.result