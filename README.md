# Verificador de Conectividad Web

<!-- # ![Tests](https://github.com/usuario/repo/workflows/Tests/badge.svg) -->

Una aplicación web interactiva construida con Streamlit para verificar la conectividad de URLs y sitios web, con un backend robusto basado en la clase `URLManager`.

## 🚀 Características

- **Verificación de conectividad**: Comprueba si una URL es accesible con manejo completo de códigos HTTP
- **Configuración flexible**: Permite personalizar protocolos, puertos, extensiones y paths
- **Parámetros de conexión**: Ajusta timeout, reintentos, redirecciones y verificación SSL
- **Previsualización en tiempo real**: Muestra la URL construida antes de verificar
- **Interfaz intuitiva**: Diseño moderno y fácil de usar con Streamlit
- **Tests automatizados**: Un conjunto de pruebas básicas para `URLManager` con pytest.
- **Código ejecutable**: Todos los archivos incluyen shebang para ejecución directa

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

3. Ingresa la URL que deseas verificar y configura las opciones según necesites

### Ejecución Directa
```bash
# Ejecutar módulo de conectividad directamente
./connectivity_checker.py

# Ejecutar pruebas manualmente
./test_url_manager.py

# Ejecutar con pytest
pytest test_url_manager.py -v
```

## 📁 Estructura del Proyecto

```
ConectivityChecker/
├── main.py                    # Aplicación principal de Streamlit
├── connectivity_checker.py    # Clase URLManager para verificación de conectividad
├── test_url_manager.py       # Suite completa de pruebas automatizadas
└── requirements.txt          # Dependencias del proyecto
```

## 🔧 Componentes

### URLManager (`connectivity_checker.py`)
Clase principal que maneja:
- **Construcción de URLs**: Genérica para cualquier protocolo (HTTP, HTTPS, FTP, etc.)
- **Verificación de conectividad**: HTTP requests con manejo completo de errores
- **Manejo de códigos HTTP**: 200, 301, 302, 307, 308, 400, 401, 403, 404, 500
- **Configuración flexible**: Timeout, reintentos, redirecciones, SSL
- **Manejo de errores**: DNS, timeout, SSL, conexión rechazada

### Aplicación Streamlit (`main.py`)
Interfaz web que proporciona:
- **Formulario de entrada**: URL con previsualización en tiempo real
- **Configuración de componentes**: Protocolo, puerto, extensión, path
- **Parámetros de conexión**: Timeout, reintentos, SSL, redirecciones
- **Visualización de resultados**: Estados claros con emojis y colores
- **Enlaces directos**: Botón para abrir URLs verificadas

### Suite de Pruebas (`test_url_manager.py`)
Pruebas automatizadas completas:
- **TestURLExamples**: Construcción de URLs y casos extremos
- **TestConnectivityExamples**: Pruebas reales con httpbin.org
- **Escenarios reales**: Redirecciones, SSL, timeout, DNS, diferentes puertos

## 🌐 Funcionalidades Detalladas

### Configuración de URL
- **Protocolos**: http://, https://, ftp://, ws://, wss://, o manual
- **Extensiones**: .com, .io, .org, .net, .dev, .tech, .app, .es, .fr, .de, .it, .co, .ai, .xyz, .me
- **Puertos**: 80, 443, 8080, 3000, 5000, 8000, o manual
- **Paths**: Rutas adicionales personalizadas

### Parámetros de Conexión
- **Timeout**: Tiempo máximo de espera (1-60 segundos)
- **Reintentos**: Número de intentos (1-10)
- **Redirecciones**: Seguir o no redirecciones automáticas
- **SSL**: Verificar certificados SSL

### Estados de Respuesta
- ✅ **Éxito**: Conexión exitosa (200)
- 🔄 **Advertencia**: Redirecciones (301, 302, 307, 308) o errores de cliente (400, 401)
- ❌ **Error**: Errores de servidor y conexión (403, 404, DNS, timeout, SSL)

## 🧪 Testing

### Ejecutar Pruebas
```bash
# Todas las pruebas
pytest test_url_manager.py -v

# Pruebas específicas
pytest test_url_manager.py::TestURLExamples -v
pytest test_url_manager.py::TestConnectivityExamples -v

# Con output detallado
pytest test_url_manager.py -v -s
```

### Cobertura de Pruebas
- **Construcción de URLs**: Protocolos, puertos, paths, casos extremos
- **Conectividad HTTP**: Códigos de estado, redirecciones, SSL
- **Manejo de errores**: Timeout, DNS, conexión rechazada
- **Servicios reales**: httpbin.org para pruebas auténticas

## 🤝 Contribuir

1. Fork del proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de los cambios (`git commit -m 'feat: añadir nueva funcionalidad'`)
4. Asegúrate de que las pruebas pasen (`pytest test_url_manager.py`)
5. Push a la rama (`git push origin feature/nueva-funcionalidad`)
6. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.