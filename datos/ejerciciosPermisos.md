# Plan de Dominio de Permisos en 2 Horas

Este es un entrenamiento intensivo. Si lo sigues paso a paso, en 2 horas entenderás cómo proteger tu API.

**Objetivo:** Pasar de "público" a "solo el dueño puede tocar su data".

---

## Bloque 1: Calentamiento (0 - 30 min)
**Tema:** Vistas basadas en funciones y decoradores simples.

1.  **Hacer una API pública**: Crea una vista `@api_view(['GET'])` que devuelva un "Hola mundo". Verifica que puedes acceder sin login.
2.  **Cerrar la puerta**: Añade `@permission_classes([IsAuthenticated])`. Intenta acceder. ¿Te da 401/403? Bien.
3.  **El VIP**: Crea un usuario `admin` (superuser) y uno `normal`. Cambia el permiso a `IsAdminUser`. Verifica que el usuario normal rebota y el admin entra.

---

## Bloque 2: Clases y Métodos (30 - 60 min)
**Tema:** `APIView` y permisos por método.

4.  **La APIView de Libros**: Crea una `class LibroAPI(APIView)`.
5.  **Lectura para todos, escritura para nadie**:
    -   Define `permission_classes = [IsAuthenticatedOrReadOnly]`.
    -   Prueba hacer un GET sin login (debería funcionar).
    -   Prueba hacer un POST sin login (debería fallar).
    -   Prueba hacer un POST con login (debería funcionar).

---

## Bloque 3: ViewSets y La Magia Rápida (60 - 90 min)
**Tema:** `ModelViewSet` y ViewSets.

6.  **El CRUD automático**: Crea un `LibroViewSet`.
7.  **Candado total**: Ponle `permission_classes = [IsAuthenticated]`.
8.  **El reto del "Solo Lectura"**: Sin cambiar la clase, intenta que solo se pueda LEER. (Pista: usa `ReadOnlyModelViewSet` en vez de `ModelViewSet` y mira qué permisos necesitas quitar/poner).

---

## Bloque 4: "Boss Final" - Custom Permissions (90 - 120 min)
**Tema:** Crear tu propio permiso (`BasePermission`).

9.  **El problema**: Ahora mismo, si estoy logueado, puedo borrar los libros de OTRO usuario. ¡Mal!
10. **La solución**: Crea un archivo `permissions.py`.
    -   Escribe una clase `IsOwnerOrReadOnly`.
    -   Hereda de `BasePermission`.
    -   Implementa el método para comprobar si el usuario es el dueño.
    -   Lógica: Si es `GET`, `HEAD`, `OPTIONS` -> `return True`.
    -   Si es `PUT`, `DELETE` -> `return obj.propietario == request.user`.
11. **Aplicarlo**: Ve a tu vista de detalle (o ViewSet) y pon `permission_classes = [IsOwnerOrReadOnly]`.
12. **Test final**:
    -   Usuario A crea libro A.
    -   Usuario B intenta borrar libro A -> **Debe fallar (403)**.
    -   Usuario A intenta borrar libro A -> **Debe funcionar (204)**.

---

**¡Si logras el paso 12, ya sabes más de permisos que la mayoría!**
