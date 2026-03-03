#!/usr/bin/env python3
"""
Pruebas de URLManager y conectividad HTTP
"""

import pytest
import requests
from managers.url_manager import URLManager
from data.status_codes_dicts import HTTP_STATUS_DICT
from unittest.mock import patch

class TestURLExamples:
    """Pruebas de construcción de URLs con diferentes componentes"""
    
    @pytest.fixture
    def url_manager(self):
        """Fixture para crear instancia de URLManager"""
        return URLManager()
    
    def test_build_url_basic(self, url_manager):
        """Prueba construcción básica de URLs"""
        test_cases = [
            ("https", "example.com", None, "", "https://example.com"),
            ("http", "example.com", 8080, "/api", "http://example.com:8080/api"),
            ("https", "api.example.com", None, "/v1/users", "https://api.example.com/v1/users"),
            ("ftp", "files.example.com", 21, "", "ftp://files.example.com:21"),
            ("wss", "ws.example.com", None, "/socket", "wss://ws.example.com/socket"),
        ]
        
        for protocol, url_address, port, path, expected in test_cases:
            url_manager.set_target_params(url_address, protocol, port, path, None, None, None, None, None)
            constructed_url = url_manager.build_target()
            
            assert constructed_url == expected
            print(f"✅ URL construida: {constructed_url}")
    
    def test_build_url_edge_cases(self, url_manager):
        """Prueba casos extremos de construcción de URLs"""
        # Protocolo manual
        url_manager.set_target_params("https://manual.com/path", None, None, None, None, None, None, None, None)
        constructed_url = url_manager.build_target()
        assert constructed_url == "https://manual.com/path"
        
        # Puerto estándar (el método es genérico, incluye el puerto)
        url_manager.set_target_params("example.com", "https", 443, "/get", None, None, None, None, None)
        constructed_url = url_manager.build_target()
        assert constructed_url == "https://example.com:443/get"
        
        # Puerto no estándar
        url_manager.set_target_params("example.com", "https", 8443, "/get", None, None, None, None, None)
        constructed_url = url_manager.build_target()
        assert constructed_url == "https://example.com:8443/get"
        
        # Puerto 80 con HTTP
        url_manager.set_target_params("localhost", "http", 80, "/", None, None, None, None, None)
        constructed_url = url_manager.build_target()
        assert constructed_url == "http://localhost:80/"
        
        # Protocolo no web (ejemplo FTP)
        url_manager.set_target_params("ftp.server.com", "ftp", 21, "/files", None, None, None, None, None)
        constructed_url = url_manager.build_target()
        assert constructed_url == "ftp://ftp.server.com:21/files"
        
        print("✅ Todos los casos extremos funcionan correctamente")

class TestConnectivityExamples:
    """Pruebas de conectividad HTTP"""

    @pytest.fixture
    def url_manager(self):
        """Fixture para crear instancia de URLManager"""
        return URLManager()

    def test_check_connectivity_response_codes(self, url_manager):
        """Pruebas de códigos de estado HTTP"""
        with patch('requests.get') as mock_get:
            # Configurar URLManager
            url_manager.set_target_params("example.com", "https", None, "test", 5, 1, True, True)
            
            # Prueba de éxito
            mock_response = mock_get.return_value
            mock_response.status_code = 200
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Éxito"
            assert "200" in message

            # Pruebas de redirección
            redirect_codes = [301, 302, 307, 308]
            for code in redirect_codes:
                mock_response.status_code = code
                status_type, message = url_manager.check_connectivity()
                assert status_type == "Advertencia"
                assert str(code) in message

            # Pruebas de error cliente
            client_error_codes = [400, 401, 403, 404]
            for code in client_error_codes:
                mock_response.status_code = code
                status_type, message = url_manager.check_connectivity()
                assert status_type == "Error"
                assert str(code) in message

            # Prueba de error servidor
            mock_response.status_code = 500
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Error"
            assert "500" in message

        print("✅ Todos los códigos de estado HTTP funcionan correctamente")

    def test_check_connectivity_exception_codes(self, url_manager):
        """Pruebas de errores de conexión HTTP"""
        with patch('requests.get') as mock_get:
            # Configurar URLManager
            url_manager.set_target_params("example.com", "https", None, "test", 5, 1, True, True)
            
            # Prueba de excepción de Timeout
            mock_get.side_effect = requests.exceptions.Timeout("Request timeout")
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Error"
            assert "Timeout" in message
            
            # Verificar que se llamó a _handle_exception y se asignaron atributos
            assert hasattr(url_manager, 'request_data')
            assert hasattr(url_manager, 'response_data')
            assert hasattr(url_manager, 'request_metadata')

            # Prueba de excepción de DNS
            mock_get.side_effect = requests.exceptions.ConnectionError("DNS resolution failed")
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Error"
            assert "DNS" in message or "no encontrado" in message
            
            # Verificar que se llamó a _handle_exception y se asignaron atributos
            assert hasattr(url_manager, 'request_data')
            assert hasattr(url_manager, 'response_data')
            assert hasattr(url_manager, 'request_metadata')

            # Prueba de excepción de SSL
            mock_get.side_effect = requests.exceptions.SSLError("SSL error")
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Error"
            assert "SSL" in message
            
            # Verificar que se llamó a _handle_exception y se asignaron atributos
            assert hasattr(url_manager, 'request_data')
            assert hasattr(url_manager, 'response_data')
            assert hasattr(url_manager, 'request_metadata')

            # Prueba de conexión rechazada
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Error"
            assert "rechazada" in message or "refused" in message
            
            # Verificar que se llamó a _handle_exception y se asignaron atributos
            assert hasattr(url_manager, 'request_data')
            assert hasattr(url_manager, 'response_data')
            assert hasattr(url_manager, 'request_metadata')

            # Prueba de demasiados redirects
            mock_get.side_effect = requests.exceptions.TooManyRedirects("Too many redirects")
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Error"
            assert "redirect" in message or "redirección" in message

            # Prueba de HTTP Error
            mock_get.side_effect = requests.exceptions.HTTPError("HTTP error")
            status_type, message = url_manager.check_connectivity()
            assert status_type == "Error"
            assert "HTTP" in message

        print("✅ Todos los códigos de excepción funcionan correctamente")

if __name__ == "__main__":
    print("🧪 Ejecutando pruebas de URLManager...")
    try:
        manager = URLManager()
        print("\n📐 Pruebas de construcción de URLs:")
        url_tests = TestURLExamples()
        url_tests.test_build_url_basic(manager)
        url_tests.test_build_url_edge_cases(manager)
        print("\n🌐 Pruebas de conectividad HTTP:")
        connectivity_tests = TestConnectivityExamples()
        connectivity_tests.test_check_connectivity_response_codes(manager)
        connectivity_tests.test_check_connectivity_exception_codes(manager)
        print("\n✅ Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en pruebas: {e}")
