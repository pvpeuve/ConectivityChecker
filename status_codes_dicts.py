#!/usr/bin/env python3
"""
Diccionarios de códigos de estado para diferentes protocolos
"""

# HTTP Status Codes (para URLManager)
HTTP_STATUS_DICT = {
    200: ("Éxito", "✅ Conexión exitosa"),
    301: ("Advertencia", "🔄 Redirección permanente"),
    302: ("Advertencia", "🔄 Redirección temporal"),
    307: ("Advertencia", "🔄 Redirección temporal"),
    308: ("Advertencia", "🔄 Redirección permanente"),
    400: ("Advertencia", "❌ Solicitud incorrecta"),
    401: ("Advertencia", "🔒 No autorizado"),
    403: ("Error", "🚫 Acceso denegado"),
    404: ("Error", "❓ Página no encontrada")
}

# Socket Error Codes (para IPManager)
SOCKET_STATUS_DICT = {
    0: ("Éxito", "✅ Puerto TCP {port} abierto en {ip}"),
    111: ("Error", "❌ Puerto TCP {port} cerrado en {ip}"),      # Linux ECONNREFUSED
    10061: ("Error", "❌ Puerto TCP {port} cerrado en {ip}"),      # Windows WSAECONNREFUSED
    110: ("Error", "❌ Timeout conectando a {ip}:{port}"),        # Linux ETIMEDOUT
    10060: ("Error", "❌ Timeout conectando a {ip}:{port}"),       # Windows WSAETIMEDOUT
    113: ("Error", "❌ No route to host: {ip}"),                   # Linux NOHOST
    10065: ("Error", "❌ No route to host: {ip}"),                 # Windows WSAEHOSTUNREACH
}