# Guía de Configuración para APIs (Django REST Framework + JWT)

Estos son los archivos y configuraciones clave que necesitas tener para que todo funcione.

---

## 1. Instalación (Terminal)

Antes de nada, asegúrate de tener instalados estos paquetes:

```bash
pip install djangorestframework djangorestframework-simplejwt
```

---

## 2. Archivo `settings.py`

Aquí es donde "enciendes" la API y configuras la seguridad.

### A. INSTALLED_APPS
Añade estas dos líneas para activar DRF y JWT:

```python
INSTALLED_APPS = [
    # ... tus otras apps ...
    'rest_framework',            # El cerebro de la API
    'rest_framework_simplejwt',  # El sistema de tokens (login)
]
```

### B. REST_FRAMEWORK (Configuración Global)
Esto define cómo se comporta tu API por defecto. 

*Cópialo tal cual al final de tu settings.py:*

```python
REST_FRAMEWORK = {
    # Autenticación: ¿Cómo saben quién soy? -> Usando JWT (Tokens)
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    
    # Permisos: ¿Quién puede entrar? -> Por defecto, cualquiera (luego restringes en las vistas)
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
}
```

### C. SIMPLE_JWT (Opcional pero recomendado)
Configura cuánto duran los tokens.

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60), # El token dura 1 hora
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),    # Tienes 1 día para renovarlo
}
```
*(Recuerda importar `timedelta` arriba del todo: `from datetime import timedelta`)*

---

## 3. Archivo `urls.py` (de tu app, ej: `datos/urls.py`)

Necesitas una ruta para que los usuarios puedan enviar su usuario/contraseña y RECIBIR el token (el "login").

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # ... tus otras rutas ...
    
    # RUTA DE LOGIN (Devuelve el token de acceso)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # RUTA DE REFRESH (Para renovar token sin loguearse de nuevo)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

## Resumen del Flujo

1.  El usuario hace POST a `/api/token/` con `username` y `password`.
2.  Django comprueba `settings.py` -> `REST_FRAMEWORK` -> `JWTAuthentication`.
3.  Si es correcto, devuelve un `access` token.
4.  En las siguientes peticiones, el usuario envía ese token en la cabecera:
    `Authorization: Bearer <tu_token_aqui>`
