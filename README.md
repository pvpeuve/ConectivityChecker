# Verificador de Conectividad Web

Una aplicación web interactiva construida con Streamlit para verificar la conectividad de URLs y sitios web.

## 🚀 Características

- **Verificación de conectividad**: Comprueba si una URL es accesible
- **Configuración flexible**: Permite personalizar protocolos, puertos, extensiones y paths
- **Parámetros de conexión**: Ajusta timeout, reintentos, redirecciones y verificación SSL
- **Previsualización en tiempo real**: Muestra la URL construida antes de verificar
- **Interfaz intuitiva**: Diseño moderno y fácil de usar con Streamlit

## 📋 Requisitos

- Python 3.7+
- Streamlit
- Requests

## 🛠️ Instalación

1. Clona el repositorio:
```bash
git clone <repositorio-url>
cd Streamlit
```

2. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install streamlit requests
```

## 🎯 Uso

1. Inicia la aplicación:
```bash
streamlit run main.py
```

2. Abre tu navegador en `http://localhost:8501`

3. Ingresa la URL que deseas verificar y configura las opciones según necesites

## 📁 Estructura del Proyecto

```
Streamlit/
├── main.py                 # Aplicación principal de Streamlit
├── connectivity_checker.py  # Clase URLManager para verificación de conectividad
├── README.md               # Este archivo
└── venv/                   # Entorno virtual
```

## 🔧 Componentes

### URLManager (`connectivity_checker.py`)
Clase principal que maneja:
- Construcción de URLs con componentes personalizados
- Verificación de conectividad HTTP
- Manejo de errores comunes (DNS, timeout, SSL, etc.)
- Configuración de parámetros de conexión

### Aplicación Streamlit (`main.py`)
Interfaz web que proporciona:
- Formulario de entrada de URL
- Configuración de componentes (protocolo, puerto, extensión, path)
- Parámetros de conexión (timeout, reintentos, SSL)
- Visualización de resultados con estados claros

## 🌐 Funcionalidades Detalladas

### Configuración de URL
- **Protocolos**: http://, https://, ftp://, ws://, wss://
- **Extensiones**: .com, .io, .org, .net, .dev, .tech, .app, .es, .fr, .de, .it, .co, .ai, .xyz, .me
- **Puertos**: 80, 443, 8080, 3000, 5000, 8000
- **Paths**: Rutas adicionales personalizadas

### Parámetros de Conexión
- **Timeout**: Tiempo máximo de espera (1-60 segundos)
- **Reintentos**: Número de intentos (1-10)
- **Redirecciones**: Seguir o no redirecciones automáticas
- **SSL**: Verificar certificados SSL

### Estados de Respuesta
- ✅ **Éxito**: Conexión exitosa (200)
- ⚠️ **Advertencia**: Errores de cliente (400, 401)
- ❌ **Error**: Errores de servidor y conexión (403, 404, DNS, timeout)

## 🤝 Contribuir

1. Fork del proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de los cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
