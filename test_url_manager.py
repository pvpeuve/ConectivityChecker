#!/usr/bin/env python3
"""
Pruebas de conectividad usando httpbin.org para verificar diferentes escenarios
"""

import pytest
from connectivity_checker import URLManager

class TestURLExamples:
    """Pruebas de construcción de URLs con diferentes componentes"""
    
    @pytest.fixture
    def url_manager(self):
        """Fixture para crear instancia de URLManager"""
        return URLManager()
    
    def test_url_construction_basic(self, url_manager):
        """Prueba construcción básica de URLs"""
        test_cases = [
            ("https://", "example.com", None, "", "https://example.com"),
            ("http://", "example.com", 8080, "/api", "http://example.com:8080/api"),
            ("https://", "api.example.com", None, "/v1/users", "https://api.example.com/v1/users"),
            ("ftp://", "files.example.com", 21, "", "ftp://files.example.com:21"),
            ("wss://", "ws.example.com", None, "/socket", "wss://ws.example.com/socket"),
        ]
        
        for protocol, base_url, port, path, expected in test_cases:
            url_manager.set_url_settings(protocol, port, path, None, base_url)
            constructed_url = url_manager.build_url()
            
            assert constructed_url == expected
            print(f"✅ URL construida: {constructed_url}")
    
    def test_url_construction_edge_cases(self, url_manager):
        """Prueba casos extremos de construcción de URLs"""
        # Protocolo manual
        url_manager.set_url_settings(None, None, None, None, "https://manual.com/path")
        constructed_url = url_manager.build_url()
        assert constructed_url == "https://manual.com/path"
        
        # Puerto estándar (el método es genérico, incluye el puerto)
        url_manager.set_url_settings("https://", 443, "/get", None, "example.com")
        constructed_url = url_manager.build_url()
        assert constructed_url == "https://example.com:443/get"
        
        # Puerto no estándar
        url_manager.set_url_settings("https://", 8443, "/get", None, "example.com")
        constructed_url = url_manager.build_url()
        assert constructed_url == "https://example.com:8443/get"
        
        # Puerto 80 con HTTP
        url_manager.set_url_settings("http://", 80, "/", None, "localhost")
        constructed_url = url_manager.build_url()
        assert constructed_url == "http://localhost:80/"
        
        # Protocolo no web (ejemplo FTP)
        url_manager.set_url_settings("ftp://", 21, "/files", None, "ftp.server.com")
        constructed_url = url_manager.build_url()
        assert constructed_url == "ftp://ftp.server.com:21/files"
        
        print("✅ Todos los casos extremos funcionan correctamente")


class TestConnectivityExamples:
    """Pruebas de conectividad con ejemplos reales de httpbin.org"""
    
    @pytest.fixture
    def url_manager(self):
        """Fixture para crear instancia de URLManager"""
        return URLManager()
    
    @pytest.fixture
    def httpbin_base(self):
        """URL base de httpbin para pruebas"""
        return "httpbin.org"
    
    def test_httpbin_get_success(self, url_manager, httpbin_base):
        """Prueba GET exitosa a httpbin.org/get"""
        url_manager.set_url_settings("https://", None, "/get", None, httpbin_base)
        url_manager.set_connectivity_settings(5, 1, True, True)
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Éxito"
        assert "200" in message
        print(f"✅ GET exitoso: {message}")
    
    def test_httpbin_status_codes(self, url_manager, httpbin_base):
        """Prueba diferentes códigos de estado HTTP"""
        test_cases = [
            ("/status/200", "Éxito"),
            ("/status/400", "Advertencia"), 
            ("/status/401", "Advertencia"),
            ("/status/403", "Error"),
            ("/status/404", "Error"),
            ("/status/500", "Error")
        ]
        
        for endpoint, expected_status in test_cases:
            url_manager.set_url_settings("https://", None, endpoint, None, httpbin_base)
            url_manager.set_connectivity_settings(5, 1, True, True)
            
            status_type, message = url_manager.check_connectivity()
            
            assert status_type == expected_status
            print(f"✅ {endpoint}: {status_type} - {message}")
    
    def test_httpbin_redirects(self, url_manager, httpbin_base):
        """Prueba redirecciones HTTP"""
        # Probar con redirecciones permitidas
        url_manager.set_url_settings("https://", None, "/redirect/2", None, httpbin_base)
        url_manager.set_connectivity_settings(5, 1, True, True)  # allow_redirects=True
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Éxito"
        print(f"✅ Redirección permitida: {message}")
        
        # Probar sin redirecciones permitidas
        url_manager.set_connectivity_settings(5, 1, False, True)  # allow_redirects=False
        
        status_type, message = url_manager.check_connectivity()
        
        # Debería ser advertencia con código 302 (redirección no seguida)
        assert status_type == "Advertencia"
        assert "302" in message
        print(f"✅ Redirección no permitida: {message}")
    
    def test_httpbin_delay(self, url_manager, httpbin_base):
        """Prueba timeout con respuesta lenta"""
        # Probar con timeout corto (debería fallar)
        url_manager.set_url_settings("https://", None, "/delay/3", None, httpbin_base)
        url_manager.set_connectivity_settings(1, 1, True, True)  # timeout=1s
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Error"
        assert "Timeout" in message
        print(f"✅ Timeout correcto: {message}")
        
        # Probar con timeout más largo (debería funcionar)
        url_manager.set_connectivity_settings(5, 1, True, True)  # timeout=5s
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Éxito"
        print(f"✅ Timeout suficiente: {message}")
    
    def test_httpbin_ssl_verification(self, url_manager, httpbin_base):
        """Prueba verificación SSL"""
        # Probar con SSL verificado (debería funcionar)
        url_manager.set_url_settings("https://", None, "/get", None, httpbin_base)
        url_manager.set_connectivity_settings(5, 1, True, True)  # verify_ssl=True
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Éxito"
        print(f"✅ SSL verificado: {message}")
        
        # Probar sin SSL verificado (debería funcionar también)
        url_manager.set_connectivity_settings(5, 1, True, False)  # verify_ssl=False
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Éxito"
        print(f"✅ SSL no verificado: {message}")
    
    def test_httpbin_different_ports(self, url_manager, httpbin_base):
        """Prueba diferentes puertos"""
        # Puerto 443 (HTTPS estándar)
        url_manager.set_url_settings("https://", 443, "/get", None, httpbin_base)
        url_manager.set_connectivity_settings(5, 1, True, True)
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Éxito"
        print(f"✅ Puerto 443: {message}")
        
        # Puerto 80 (HTTP estándar)
        url_manager.set_url_settings("http://", 80, "/get", None, httpbin_base)
        url_manager.set_connectivity_settings(5, 1, True, True)
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Éxito"
        print(f"✅ Puerto 80: {message}")
    
    def test_httpbin_invalid_paths(self, url_manager, httpbin_base):
        """Prueba paths que no existen"""
        url_manager.set_url_settings("https://", None, "/path/that/does/not/exist", None, httpbin_base)
        url_manager.set_connectivity_settings(5, 1, True, True)
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Error"
        assert "404" in message
        print(f"✅ Path inexistente: {message}")
    
    def test_httpbin_invalid_domain(self, url_manager):
        """Prueba dominio que no existe"""
        url_manager.set_url_settings("https://", None, "/get", None, "this-domain-does-not-exist-12345.com")
        url_manager.set_connectivity_settings(5, 1, True, True)
        
        status_type, message = url_manager.check_connectivity()
        
        assert status_type == "Error"
        assert "DNS" in message or "no encontrado" in message
        print(f"✅ Dominio inválido: {message}")


if __name__ == "__main__":
    # Ejecutar pruebas manualmente
    print("🧪 Ejecutando pruebas de httpbin.org...")
    
    # Pruebas de URL
    print("\n📐 Pruebas de construcción de URLs:")
    url_tests = TestURLConstruction()
    manager = URLManager()
    
    try:
        url_tests.test_url_construction_basic(manager)
        url_tests.test_url_construction_edge_cases(manager)
        
        # Pruebas de conectividad
        print("\n🌐 Pruebas de conectividad:")
        connectivity_tests = TestConnectivityExamples()
        base_url = "httpbin.org"
        
        connectivity_tests.test_httpbin_get_success(manager, base_url)
        connectivity_tests.test_httpbin_status_codes(manager, base_url)
        connectivity_tests.test_httpbin_redirects(manager, base_url)
        connectivity_tests.test_httpbin_delay(manager, base_url)
        connectivity_tests.test_httpbin_ssl_verification(manager, base_url)
        connectivity_tests.test_httpbin_different_ports(manager, base_url)
        connectivity_tests.test_httpbin_invalid_paths(manager, base_url)
        connectivity_tests.test_httpbin_invalid_domain(manager)
        
        print("\n🎉 Todas las pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"\n❌ Error en pruebas: {e}")
