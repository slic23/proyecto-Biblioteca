# Apuntes Maestros: Permisos en Django REST Framework

Los permisos deciden **quién puede tocar qué**.
No confundir con **Autenticación** (que dice *quién eres*). Los permisos dicen *qué puedes hacer*.

---

## 1. Los 4 Jinetes (Permisos Estándar)

DRF trae estos de fábrica. Cubren el 90% de los casos.

| Permiso | Descripción |
| :--- | :--- |
| **`AllowAny`** | **Puertas abiertas**. Entra todo el mundo, logueado o anónimo. |
| **`IsAuthenticated`** | **Solo socios**. Si no estás logueado, error 401/403. |
| **`IsAdminUser`** | **Solo Staff**. `user.is_staff == True`. Para el panel de control. |
| **`IsAuthenticatedOrReadOnly`** | **Mirar sí, tocar no**. Cualquiera puede leer (GET), pero solo registrados pueden editar (POST, PUT, DELETE). Perfecto para blogs o foros. |

---

## 2. Dónde ponerlos

### A. A nivel Global (`settings.py`)
La regla por defecto para TODA tu API.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # Por defecto, cerrado a cal y canto
    ]
}
```

### B. A nivel de Vista (Específico)
Sobrescribe la regla global.

**En Clases (`APIView`, `Generics`, `ViewSets`):**
```python
from rest_framework.permissions import IsAuthenticated

class MiVista(APIView):
    permission_classes = [IsAuthenticated] 
```

**En Funciones (`@api_view`):**
```python
from rest_framework.decorators import permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mi_vista(request):
    ...
```

---

## 3. Combinando Poderes (&, |, ~)

Puedes usar lógica booleana para crear reglas complejas sin programar.

```python
# Tienes que ser Admin O (OR) ser el dueño de la cuenta
permission_classes = [IsAdminUser | IsOwner]

# Tienes que estar Autenticado Y (AND) ser Admin
permission_classes = [IsAuthenticated & IsAdminUser]

# NO (NOT) puede ser un usuario bloqueado
permission_classes = [~IsBlocked]
```

---

## 4. Permisos Personalizados (Custom Permissions)

Cuando los estándar no te valen (ej: "Solo usuarios mayores de 18", "Solo premium", "Solo en horario laboral").

**Pasos:**
1.  Crear un archivo `permissions.py`.
2.  Heredar de `BasePermission`.
3.  Implementar el método **`has_permission`**.

> **Nota:** Aquí evaluamos si el usuario tiene permiso para **entrar a la vista en general**.

```python
# permissions.py
from rest_framework.permissions import BasePermission

class EsMayorDeEdad(BasePermission):
    mensaje_error = "Vuelve cuando tengas 18 años." # Opcional: Personalizar mensaje

    def has_permission(self, request, view):
        # Devuelve True (pasa) o False (error 403)
        
        # 1. Comprobar si está logueado primero (buena práctica)
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Tu lógica personalizada
        # Suponiendo que el usuario tiene un campo 'edad' o 'fecha_nacimiento'
        return request.user.edad >= 18
```

**Cómo usarlo:**
```python
# views.py
from .permissions import EsMayorDeEdad

class SoloAdultosView(APIView):
    permission_classes = [IsAuthenticated, EsMayorDeEdad]
```
