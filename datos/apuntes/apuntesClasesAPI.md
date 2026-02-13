# Apuntes: Vistas Basadas en Clases (APIView)

Si `@api_view` es para funciones rápidas, `APIView` es para tenerlo todo **ordenado**. Aquí usas una **CLASE** y separas cada método HTTP en una función dentro de la clase.

---

## 1. La Estructura Básica

En lugar de `if request.method == 'GET'`, aquí defines una función llamada `get`. DRF sabe a cuál llamar automáticamente.

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MiVistaDeClase(APIView):
    
    def get(self, request):
        return Response({"mensaje": "Esto es un GET"})

    def post(self, request):
        return Response({"mensaje": "Esto es un POST", "datos": request.data})
```

---

## 2. Permisos (`permission_classes`)

Igual que en las funciones, pero se pone como una **variable de clase**.

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class VistaProtegida(APIView):
    # Aquí defines quién entra. Es una LISTA.
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        return Response({"secreto": "Solo para logueados"})
```

### Sobreescribir permisos por método (Truco Intermedio)
Si quieres que el GET sea público pero el POST sea privado, puedes usar `get_permissions`:

```python
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
```

---

## 3. Ejemplo CRUD Básico (GET y POST)

```python
class LibroListAPI(APIView):
    
    def get(self, request):
        # 1. Buscar datos
        libros = Libro.objects.all()
        # 2. Serializar (muchos=True porque es una lista)
        serializer = LibroSerializer(libros, many=True)
        # 3. Responder
        return Response(serializer.data)

    def post(self, request):
        # 1. Pasar datos al serializer
        serializer = LibroSerializer(data=request.data)
        # 2. Validar
        if serializer.is_valid():
            # 3. Guardar
            serializer.save()
            # 4. Responder con éxito (201 Created)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # 5. Si falla, responder error (400 Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

---

## 4. Ejemplo con ID (PUT y DELETE)

Para editar o borrar un elemento específico, necesitas recibir el `pk` (ID).

`URL: path('libros/<int:pk>/', LibroDetailAPI.as_view())`

```python
from django.shortcuts import get_object_or_404

class LibroDetailAPI(APIView):
    
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        serializer = LibroSerializer(libro)
        return Response(serializer.data)

    def put(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        # Pasa la instancia (libro) Y los datos nuevos
        serializer = LibroSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## Resumen

1.  Heredar de `APIView`.
2.  Definir métodos con nombre minúsculo: `get`, `post`, `put`, `delete`, `patch`.
3.  Permisos en `permission_classes = [...]`.
4.  Usar `status` para responder con el código HTTP correcto.
