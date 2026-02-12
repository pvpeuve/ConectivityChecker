# ConectivityChecker - Verificador de Conectividad Web y IP

<!-- # ![Tests](https://github.com/usuario/repo/workflows/Tests/badge.svg) -->

Una aplicación web interactiva construida con Streamlit para verificar la conectividad de URLs, sitios web y direcciones IP, con una arquitectura modular basada en managers especializados.

## 🚀 Características

### 🌐 Verificación de URLs
- **Verificación HTTP/HTTPS**: Comprueba accesibilidad web con manejo completo de códigos HTTP
- **Configuración flexible**: Protocolos (http, https, ftp, ws, wss), puertos, extensiones y paths
- **Parámetros de conexión**: Timeout, reintentos, redirecciones y verificación SSL
- **Previsualización dinámica**: Muestra la URL construida en tiempo real

### 🌍 Verificación de IPs
- **Verificación TCP**: Comprueba conectividad directa a direcciones IP y puertos
- **Soporte multi-puerto**: Puertos comunes (22, 23, 25, 53, 3306, 5432) o personalizados
- **Configuración de red**: Timeout y reintentos para conexiones TCP
- **Previsualización de targets**: Formato IP:puerto en tiempo real

### 🎨 Interfaz Moderna
- **Navegación multi-página**: `st.navigation` con páginas separadas para URLs e IPs
- **Session state dinámico**: Actualización en tiempo real sin perder datos
- **Diseño profesional**: Tabs, placeholders, y UX optimizada
- **Enlaces directos**: Botones para abrir URLs verificadas

### 🧪 Testing Robusto
- **Tests automatizados**: Suites completas para URLManager e IPManager
- **Mocks y patches**: Pruebas aisladas sin dependencias externas
- **Cobertura completa**: Construcción, conectividad, errores y casos extremos

## 📋 Requisitos

- Python 3.7+
- Streamlit 1.53.1+
- Requests 2.32.5+
- Pytest 9.0.2+ (para pruebas)

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone <repositorio-url>
cd ConectivityChecker
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🎯 Uso

### Aplicación Web
1. Inicia la aplicación:
```bash
streamlit run main.py
```

2. Abre en tu navegador la dirección que te indica streamlit (normalmente `http://localhost:8501`)

3. Navega entre las páginas:
   - **🌐 URLs**: Verificación de sitios web y APIs HTTP/HTTPS
   - **🌍 IPs**: Verificación de conectividad TCP a direcciones IP

4. Configura los parámetros y verifica la conectividad

### Ejecución Directa
```bash
# Ejecutar managers directamente
./url_manager.py
./ip_manager.py

# Ejecutar pruebas manualmente
./test_url_manager.py
./test_ip_manager.py

# Ejecutar con pytest
pytest test_url_manager.py test_ip_manager.py -v
```

## 📁 Estructura del Proyecto

```
ConectivityChecker/
├── main.py                    # Aplicación principal con st.navigation
├── pages/                     # Páginas de Streamlit
│   ├── urls.py               # Página de verificación de URLs
│   └── ips.py                # Página de verificación de IPs
├── managers/                  # Clases managers (lógica de negocio)
│   ├── url_manager.py        # Manager para URLs HTTP/HTTPS
│   ├── ip_manager.py         # Manager para IPs TCP
│   └── base_manager.py       # Clase base compartida
├── tests/                     # Suites de pruebas
│   ├── test_url_manager.py   # Pruebas para URLManager
│   └── test_ip_manager.py    # Pruebas para IPManager
├── data/                      # Datos y configuraciones
│   └── status_codes_dicts.py # Diccionarios de códigos HTTP y socket
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Documentación
```

## 🔧 Componentes

### URLManager (`managers/url_manager.py`)
Manager especializado para verificación web:
- **Construcción de URLs**: Genérica para cualquier protocolo (HTTP, HTTPS, FTP, WebSocket)
- **Verificación HTTP**: Requests con manejo completo de errores y códigos de estado
- **Configuración flexible**: Timeout, reintentos, redirecciones, verificación SSL
- **Target building**: Construcción dinámica de URLs con componentes modulares

### IPManager (`managers/ip_manager.py`)
Manager especializado para verificación de red:
- **Construcción de targets**: Formato IP:puerto con validación
- **Verificación TCP**: Sockets para conectividad directa a puertos
- **Configuración de red**: Timeout y reintentos para conexiones TCP
- **Manejo de errores**: Formato inválido, timeout, errores de socket

### BaseManager (`managers/base_manager.py`)
Clase base compartida que proporciona:
- **Atributos comunes**: target, result, timeout, retries
- **Interfaz estándar**: Métodos base para construcción y verificación
- **Herencia múltiple**: Base para managers especializados

### Páginas Streamlit (`pages/`)
Interfaz web moderna con:
- **urls.py**: Verificación de URLs con previsualización dinámica
- **ips.py**: Verificación de IPs con configuración de puertos
- **Session state**: Mantenimiento de estado entre interacciones
- **UX optimizada**: Tabs, placeholders, y actualización en tiempo real
- **Manejo de errores**: DNS, timeout, SSL, conexión rechazada

### Aplicación Principal (`main.py`)
Navegación y configuración global:
- **st.navigation**: Navegación multi-página con URLs e IPs
- **Configuración central**: Título, layout, y estructura global
- **Enrutamiento**: Manejo de páginas y navegación fluida

## 🌐 Funcionalidades Detalladas

### Verificación de URLs
- **Protocolos**: http://, https://, ftp://, ws://, wss://, o manual
- **Extensiones**: .com, .io, .org, .net, .dev, .tech, .app, .es, .fr, .de, .it, .co, .ai, .xyz, .me
- **Puertos**: 80, 443, 8080, 3000, 5000, 8000, o manual
- **Paths**: Rutas adicionales personalizadas (/api/v1/users, /socket, etc.)

### Verificación de IPs
- **Protocolos**: TCP (con soporte para futuras expansiones)
- **Puertos comunes**: 22 (SSH), 23 (Telnet), 25 (SMTP), 53 (DNS), 3306 (MySQL), 5432 (PostgreSQL)
- **Puertos personalizados**: Cualquier puerto válido (1-65535)
- **Formatos**: IPv4, localhost, nombres de host

### Parámetros de Conexión
- **Timeout**: Tiempo máximo de espera (1-60 segundos)
- **Reintentos**: Número de intentos (1-10)
- **Redirecciones**: Seguir o no redirecciones automáticas (solo URLs)
- **SSL**: Verificar certificados SSL (solo URLs HTTPS)

### Estados de Respuesta
- ✅ **Éxito**: Conexión exitosa (HTTP 200, TCP conectado)
- 🔄 **Advertencia**: Redirecciones (301, 302, 307, 308) o errores de cliente (400, 401)
- ❌ **Error**: Errores de servidor, conexión (403, 404, DNS, timeout, SSL, TCP cerrado)

## 🧪 Testing

### Ejecutar Pruebas
```bash
# Todas las pruebas
pytest test_url_manager.py test_ip_manager.py -v

# Pruebas específicas de URLs
pytest test_url_manager.py::TestURLExamples -v
pytest test_url_manager.py::TestConnectivityExamples -v

# Pruebas específicas de IPs
pytest test_ip_manager.py::TestIPExamples -v
pytest test_ip_manager.py::TestConnectivityExamples -v

# Con output detallado
pytest test_url_manager.py test_ip_manager.py -v -s
```

### Cobertura de Pruebas

#### URLManager
- **Construcción de URLs**: Protocolos, puertos, paths, casos extremos
- **Conectividad HTTP**: Códigos de estado, redirecciones, SSL
- **Manejo de errores**: Timeout, DNS, conexión rechazada, SSL
- **Mocks y patches**: Pruebas aisladas con requests mock

#### IPManager  
- **Construcción de targets**: Formato IP:puerto, validación
- **Conectividad TCP**: Códigos de socket, puertos abiertos/cerrados
- **Manejo de errores**: Formato inválido, timeout, errores de socket
- **Mocks y patches**: Pruebas aisladas con socket mock

### Arquitectura de Tests
- **Fixtures**: Instancias limpias de managers para cada test
- **Patches**: Aislamiento de dependencias externas (requests, socket)
- **Escenarios reales**: httpbin.org para URLs, mocks para IPs
- **Casos extremos**: Validación de formatos, errores inesperados

## 🤝 Contribuir

1. Fork del proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de los cambios (`git commit -m 'feat: añadir nueva funcionalidad'`)
4. Asegúrate de que las pruebas pasen (`pytest test_url_manager.py test_ip_manager.py`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

## 🚀 Roadmap v2.0

### Próximas Features
- **📊 Dashboard Analytics**: Métricas y estadísticas de verificación
- **🔄 Batch Processing**: Verificación múltiple de URLs/IPs
- **📱 Responsive Design**: Optimización para dispositivos móviles
- **🔐 Authentication**: Usuarios y sesiones personalizadas
- **📈 Export Results**: CSV, JSON, PDF con históricos
- **🌍 Internationalization**: Múltiples idiomas
- **⚡ Caching**: Cache inteligente para respuestas
- **🔔 Notifications**: Alertas y monitoreo continuo

### Mejoras Técnicas
- **🏗️ Microservicios**: Separación de servicios
- **🗄️ Database**: PostgreSQL/MongoDB para persistencia
- **🐳 Docker**: Contenerización completa
- **🚀 CI/CD**: GitHub Actions para testing y deploy
- **📊 Monitoring**: Prometheus + Grafana
- **🔒 Security**: JWT, rate limiting, input validation

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**⭐ Si este proyecto te fue útil, no olvides darle una estrella!**

**🐛 ¿Encontraste un bug? Por favor abre un [issue](https://github.com/usuario/repo/issues)**

**💡 ¿Tienes una idea? Contribuye con un [PR](https://github.com/usuario/repo/pulls)**