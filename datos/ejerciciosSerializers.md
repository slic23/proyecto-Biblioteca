# Plan de Dominio de Serializers en 2 Horas

Igual que con los permisos, aquí tienes un plan práctico para entender de verdad cómo funcionan los traductores de DRF.

**Objetivo:** Dejar de sufrir cuando el JSON no tiene el formato que quieres.

---

## Bloque 1: Lo Básico y "El Renombrado" (0 - 30 min)
**Tema:** `ModelSerializer` y manipulación básica.

1.  **El Espejo**: Crea un `LibroSerializer` que use `ModelSerializer` y `fields = '__all__'`. Comprueba que devuelve todo.
2.  **El Selectivo**: Cambia a `fields = ['titulo', 'autor']`. Comprueba que el resto desaparece.
3.  **El Alias (source)**: Imagina que en el JSON quieres que `titulo` se llame `nombre_del_libro`.
    -   En el serializer: `nombre_del_libro = serializers.CharField(source='titulo')`.
    -   Añádelo a `fields`.

---

## Bloque 2: Validaciones (El Portero) (30 - 60 min)
**Tema:** `validate_<campo>` y `validate`.

4.  **Regla simple**: Que el `titulo` no pueda tener la palabra "Prohibido".
    -   Método: `def validate_titulo(self, value): ...`
    -   Si falla, lanza `serializers.ValidationError`.
5.  **Regla compuesta**: Que el `titulo` y la `descripcion` no sean iguales.
    -   Método: `def validate(self, data): ...` (accedes a todo `data`).

---

## Bloque 3: Relaciones y Profundidad (60 - 90 min)
**Tema:** `Nested Serializers` vs `PrimaryKeys`.

6.  **El ID**: Por defecto, el `autor` sale como un número (ID).
7.  **El String**: Usa `autor = serializers.StringRelatedField()`. Ahora sale el `__str__` del autor.
8.  **El Objeto Completo (Nested)**:
    -   Crea un `AutorSerializer`.
    -   En `LibroSerializer`, pon `autor = AutorSerializer()`.
    -   ¡Magia! Ahora dentro del libro viene el objeto autor entero.
    -   *Nota: Intenta crear un libro con esto activado. ¿Te deja? (Spoiler: Es complicado escribir en nested, normalmente es read_only=True).*

---

## Bloque 4: Campos Calculados (90 - 120 min)
**Tema:** `SerializerMethodField` (Meter datos que NO existen en la BD).

9.  **El Campo Fantasma**: Quieres enviar un campo `es_bestseller` que sea `True` si tiene más de 500 páginas.
    -   Campo: `es_bestseller = serializers.SerializerMethodField()`.
    -   Método: `def get_es_bestseller(self, obj): return obj.paginas > 500`.
10. **La Prueba Final**:
    -   Haz un serializer que devuelva: Título, Autor (nombre), y una frase generada "El libro {titulo} fue escrito por {autor}".

---

**Si dominas el Bloque 3 y 4, puedes modelar cualquier JSON que te pida el Frontend.**
