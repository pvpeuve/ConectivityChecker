#!/usr/bin/env python3
"""
Pruebas de IPManager y conectividad TCP
"""
import pytest
import socket
from ip_manager import IPManager
from unittest.mock import patch

class TestIPExamples:
    """Pruebas de construcción de IPs con diferentes componentes"""
    
    @pytest.fixture
    def ip_manager(self):
        """Fixture para crear instancia de IPManager"""
        return IPManager()
    
    def test_build_ip_basic(self, ip_manager):
        """Prueba construcción básica de IPs"""
        test_cases = [
            ("192.168.1.1", None, "192.168.1.1"),           # IP sin puerto
            ("10.0.0.1", 80, "10.0.0.1:80"),               # IP con puerto 80
            ("172.16.0.1", 443, "172.16.0.1:443"),          # IP con puerto 443
            ("localhost", 22, "localhost:22"),                # localhost con SSH
            ("8.8.8.8", 53, "8.8.8.8:53"),                  # DNS público
            ("127.0.0.1", 3000, "127.0.0.1:3000"),           # Loopback con puerto custom
        ]
        
        for ip_address, port, expected in test_cases:
            ip_manager.set_settings(ip_address, port)
            constructed_target = ip_manager.build_target()
            
            assert constructed_target == expected
            print(f"✅ Target construido: {constructed_target}")
    
    def test_build_ip_edge_cases(self, ip_manager):
        """Prueba casos extremos de construcción de targets IP"""
        # IP con puerto estándar HTTP
        ip_manager.set_settings("192.168.1.100", 80)
        constructed_target = ip_manager.build_target()
        assert constructed_target == "192.168.1.100:80"
        
        # IP con puerto estándar HTTPS
        ip_manager.set_settings("10.0.0.1", 443)
        constructed_target = ip_manager.build_target()
        assert constructed_target == "10.0.0.1:443"
        
        # IP con puerto no estándar
        ip_manager.set_settings("172.16.0.50", 8080)
        constructed_target = ip_manager.build_target()
        assert constructed_target == "172.16.0.50:8080"
        
        # IP con puerto alto
        ip_manager.set_settings("192.168.1.200", 65535)
        constructed_target = ip_manager.build_target()
        assert constructed_target == "192.168.1.200:65535"
        
        # localhost con diferentes puertos
        ip_manager.set_settings("localhost", 3306)
        constructed_target = ip_manager.build_target()
        assert constructed_target == "localhost:3306"
        
        print("✅ Todos los casos extremos de IP funcionan correctamente")

class TestConnectivityExamples:
    """Pruebas de conectividad IP con sockets"""

    @pytest.fixture
    def ip_manager(self):
        """Fixture para crear instancia de IPManager"""
        return IPManager()

    def test_check_connectivity_socket_codes(self, ip_manager):
        """Pruebas de códigos de estado de socket TCP"""
        with patch('socket.socket') as mock_socket_class:
            # Configurar IPManager
            ip_manager.set_settings("192.168.1.1", 80)
            
            # Mock del socket
            mock_socket = mock_socket_class.return_value
            
            # Prueba de éxito (puerto abierto)
            mock_socket.connect_ex.return_value = 0
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Éxito"
            assert "80" in message and "192.168.1.1" in message

            # Pruebas de error (puerto cerrado) - Linux
            mock_socket.connect_ex.return_value = 111
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "cerrado" in message

            # Pruebas de error (puerto cerrado) - Windows
            mock_socket.connect_ex.return_value = 10061
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "cerrado" in message

            # Pruebas de timeout - Linux
            mock_socket.connect_ex.return_value = 110
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "Timeout" in message

            # Pruebas de timeout - Windows
            mock_socket.connect_ex.return_value = 10060
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "Timeout" in message

            # Pruebas de no route to host - Linux
            mock_socket.connect_ex.return_value = 113
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "route" in message

            # Pruebas de no route to host - Windows
            mock_socket.connect_ex.return_value = 10065
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "route" in message

        print("✅ Todos los códigos de socket funcionan correctamente")

    def test_check_connectivity_socket_exceptions(self, ip_manager):
        """Pruebas de errores de conexión TCP"""
        with patch('socket.socket') as mock_socket_class:
            # Configurar IPManager
            ip_manager.set_settings("192.168.1.1", 80)
            
            # Mock del socket
            mock_socket = mock_socket_class.return_value
            
            # Prueba de excepción de socket
            mock_socket.connect_ex.side_effect = socket.error("Socket error")
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "conexión" in message

            # Prueba de excepción de timeout
            mock_socket.connect_ex.side_effect = socket.timeout("Socket timeout")
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "Timeout" in message

            # Prueba de excepción genérica
            mock_socket.connect_ex.side_effect = Exception("Generic error")
            status_type, message = ip_manager.check_connectivity()
            assert status_type == "Error"
            assert "conexión" in message

        print("✅ Todos los códigos de excepción de socket funcionan correctamente")

if __name__ == "__main__":
    print("🧪 Ejecutando pruebas de IPManager...")
    try:
        manager = IPManager()
        print("\n📐 Pruebas de construcción de targets IP:")
        ip_tests = TestIPExamples()
        ip_tests.test_build_ip_basic(manager)
        ip_tests.test_build_ip_edge_cases(manager)
        print("\n🌐 Pruebas de conectividad TCP:")
        connectivity_tests = TestConnectivityExamples()
        connectivity_tests.test_check_connectivity_socket_codes(manager)
        connectivity_tests.test_check_connectivity_socket_exceptions(manager)
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en pruebas: {e}")
