# Apuntes: Vistas Genéricas (`generics`)

Las **Generic Views** son el punto medio perfecto: escribes muy poco código (como en los ViewSets) pero mantienes el control de qué hace cada vista (como en las APIView).

---

## 1. La Filosofía

En lugar de escribir el código para "listar" o "crear" desde cero, heredas de una clase que YA sabe hacerlo. Tú solo configuras:
1.  `queryset`: ¿Qué datos busco?
2.  `serializer_class`: ¿Cómo los traduzco?

---

## 2. Las Más Usadas

-   **`ListAPIView`**: Solo listar (GET).
-   **`CreateAPIView`**: Solo crear (POST).
-   **`ListCreateAPIView`**: Listar (GET) y Crear (POST). *Muy común para colecciones.*
-   **`RetrieveAPIView`**: Ver detalle de uno (GET con ID).
-   **`RetrieveUpdateDestroyAPIView`**: Ver, Editar y Borrar (GET, PUT, DELETE con ID). *Muy común para detalles.*

---

## 3. Ejemplo Básico

```python
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Para /libros/ (Lista y Crea)
class LibroListCreate(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]

# Para /libros/<int:pk>/ (Detalle, Edita, Borra)
class LibroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]
```
*¡Ya está! Con esto tienes un CRUD completo.*

---

## 4. Sobreescribir el Comportamiento (Lo Importante)

A veces no quieres el comportamiento por defecto. Aquí es donde **sobreescribes métodos**.

### A. `get_queryset(self)`: Filtrar datos
Si no quieres devolver `objects.all()`, usa esto.

```python
class MisLibrosList(generics.ListAPIView):
    serializer_class = LibroSerializer

    def get_queryset(self):
        # Solo devuelvo los libros DEL USUARIO conectado
        usuario = self.request.user
        return Libro.objects.filter(autor__usuario=usuario)
```

### B. `perform_create(self, serializer)`: Guardar datos extra
Cuando creas algo (POST), a veces quieres guardar datos automáticos que no vienen en el JSON (como el dueño).

```python
class LibroCreate(generics.CreateAPIView):
    serializer_class = LibroSerializer

    def perform_create(self, serializer):
        # Guardo el libro, pero fuerzo que el 'autor' sea el usuario actual
        # (El usuario no manda su propio ID, se lo pongo yo aquí)
        serializer.save(autor__usuario=self.request.user)
```

---

## Resumen

1.  Elige la clase que necesites (`ListCreate...`, `Retrieve...`).
2.  Define `queryset` y `serializer_class`.
3.  Si necesitas lógica especial:
    -   Para filtrar lista -> `get_queryset`.
    -   Para guardar data autòmatica -> `perform_create`.
