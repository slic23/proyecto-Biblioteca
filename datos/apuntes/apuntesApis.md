# Apuntes sobre APIs con Django REST Framework (DRF)

Aquí tienes una guía paso a paso, desde lo más básico hasta lo más "mágico" (ViewSets), centrándonos en cómo controlar quién puede hacer qué (Permisos).

---

## 1. Serializers (El traductor)

Antes de hacer vistas, necesitas algo que traduzca tus modelos de Django a JSON (para que la API lo entienda) y viceversa. Eso es el **Serializer**.

```python
from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__' # O pon una lista ['titulo', 'autor']
```

---

## 2. Vistas Basadas en Funciones (`@api_view`)

Es la forma más básica, parecida a las views normales de Django pero con esteroides. Usas decoradores para definir métodos y permisos.

**Lo bueno:** Tienes control total de lo que pasa.
**Lo malo:** Escribes más código si es algo estándar.

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Libro
from .serializers import LibroSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) # Solo si estás logueado
def lista_libros_api(request):
    
    if request.method == 'GET':
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

---

## 3. APIView (Clases básicas)

Aquí ya usamos Clases. Es más limpio que las funciones porque separas `get`, `post`, `put` en métodos.

**Permisos:** Se definen como una lista en la clase.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

class LibroAPIView(APIView):
    """
    Vista personalizada para listar y crear libros
    """
    permission_classes = [IsAdminUser] # Solo admins pueden tocar aquí

    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LibroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

## 4. Generics (Vistas Genéricas)

Aquí empieza la "magia". DRF ya tiene clases preparadas para lo típico (Listar, Crear, Borrar, Editar). Tú solo le dices "qué modelo" y "qué serializer".

**Tipos comunes:**
- `ListAPIView`: Solo ver lista.
- `CreateAPIView`: Solo crear.
- `ListCreateAPIView`: Ver lista y crear.
- `RetrieveUpdateDestroyAPIView`: Ver detalle, editar y borrar (necesita PK).

```python
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Esta vista lista y crea
class LibroListCreate(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    # Cualquiera puede ver (GET), pero solo logueados pueden crear (POST)
    permission_classes = [IsAuthenticatedOrReadOnly] 

# Esta vista ve detalle, actualiza y borra
class LibroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAdminUser] # Solo admin borra o edita
```

---

## 5. ViewSets (La magia total)

Si quieres hacer un CRUD completo (Crear, Leer, Actualizar, Borrar) y no quieres escribir 4 vistas diferentes, usas **ViewSets**.

Un `ModelViewSet` hace TODO automáticamente.

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

class LibroViewSet(viewsets.ModelViewSet):
    """
    Esto crea AUTOMÁTICAMENTE las rutas para:
    - GET /libros/ (lista)
    - POST /libros/ (crear)
    - GET /libros/1/ (detalle)
    - PUT /libros/1/ (editar)
    - DELETE /libros/1/ (borrar)
    """
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated] # Todo protegido
```

### ¿Cómo se conectan los ViewSets? (Routers)
Los ViewSets no se ponen en `urlpatterns` normal, necesitan un **Router**.

En `urls.py`:
```python
from rest_framework.routers import DefaultRouter
from .views import LibroViewSet

router = DefaultRouter()
router.register(r'libros', LibroViewSet)

urlpatterns = [
    # ... tus otras urls ...
]

urlpatterns += router.urls # Añades las rutas mágicas
```

---

## Resumen de Permisos

Puedes usarlos en `permission_classes = [...]`.

1.  **`AllowAny`**: Todo el mundo entra (público).
2.  **`IsAuthenticated`**: Solo usuarios logueados.
3.  **`IsAdminUser`**: Solo superusuarios (`is_staff=True`).
4.  **`IsAuthenticatedOrReadOnly`**:
    -   Logueados: Pueden escribir (POST, PUT, DELETE).
    -   No logueados: Solo pueden leer (GET).

### Tu propio permiso (Custom Permission)

Si quieres algo específico, como "Solo el dueño de este objeto puede editarlo":

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado: solo el dueño puede editar.
    """
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS se permiten siempre (Read-only)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions (PUT, DELETE) solo al dueño
        return obj.owner == request.user
```

---

**Resumen rápido:**
- **Serializer**: Convierte datos.
- **@api_view**: Para cosas muy específicas y manuales.
- **APIView**: Para lógica compleja pero organizada en clases.
- **Generics**: Para CRUDS estándar rápido.
- **ViewSets**: Para CRUDS completos con cero código repetido.
