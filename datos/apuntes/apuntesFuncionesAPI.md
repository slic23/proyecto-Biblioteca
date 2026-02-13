# Apuntes: Vistas Basadas en Funciones (Function-Based Views)

Las **FBV** son la forma más directa de escribir una API. Escribes una función de Python normal y le pones "poderes" con decoradores.

---

## 1. El Decorador Mágico: `@api_view`

Sin esto, es una vista normal de Django. Con esto, es una vista de DRF (recibe `Request` y devuelve `Response`).

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST']) # Aquí defines qué métodos acepta
def mi_vista(request):
    return Response({"mensaje": "Hola!"})
```

---

## 2. Controlando los Métodos (GET, POST, PUT...)

Dentro de la función, usas `if` para saber qué te están pidiendo.

```python
@api_view(['GET', 'POST'])
def lista_libros(request):
    
    # CASO 1: Alguien quiere LEER datos
    if request.method == 'GET':
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True)
        return Response(serializer.data)

    # CASO 2: Alguien quiere GUARDAR datos nuevos
    elif request.method == 'POST':
        serializer = LibroSerializer(data=request.data) # request.data ya viene limpio (JSON parseado)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

---

## 3. Permisos (`@permission_classes`)

¿Quién puede entrar aquí? Se define con otro decorador **debajo** de `@api_view`.

```python
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

@api_view(['DELETE'])
@permission_classes([IsAdminUser]) # Solo el administrador
def borrar_libro(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response(status=404)

    if request.method == 'DELETE':
        libro.delete()
        return Response(status=204)
```

**Permisos comunes:**
- `[AllowAny]`: Entra cualquiera (público).
- `[IsAuthenticated]`: Solo si envían token/login válido.
- `[IsAdminUser]`: Solo si `is_staff=True`.
- `[IsAuthenticatedOrReadOnly]`: Logueados escriben, anónimos solo leen.

---

## 4. Otros Decoradores Útiles

A veces necesitas más control. Se apilan uno tras otro.

```python
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.throttling import UserRateThrottle

@api_view(['GET'])
@throttle_classes([UserRateThrottle]) # Limita cuántas veces pueden llamar a esta API por minuto
def vista_lenta(request):
    return Response({"mensaje": "No abuses de mí"})
```

---

## Resumen de la Estructura

1.  **Decoradores**: `@api_view` (obligatorio) + `@permission_classes` (opcional).
2.  **Firma**: `def nombre(request, pk=None):`.
3.  **Lógica**: `if request.method == '...':`.
4.  **Respuesta**: Siempre devolver `Response(...)`.
