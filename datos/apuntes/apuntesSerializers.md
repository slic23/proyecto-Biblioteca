# Apuntes Maestros: Serializers en Django REST Framework

El **Serializer** es el traductor universal.
-   **Python (Modelos/Clases) -> JSON** (Para que el frontend lo entienda).
-   **JSON -> Python** (Para guardar en la BD).

---

## 1. `ModelSerializer` (El Automático)
Casi siempre usarás este. Copia la estructura de tu modelo.

```python
from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'  # Ojo: Mejor listar los campos uno a uno en producción
        # fields = ['id', 'titulo', 'autor']
        # exclude = ['password']
```

---

## 2. Personalizando Campos (El "Renombrado")

A veces el frontend quiere claves distintas a tu base de datos.
Usa `source` para decirle de dónde sacar el dato.

```python
class LibroCustomSerializer(serializers.ModelSerializer):
    # En el JSON saldrá "nombre_del_libro", pero sacará el dato de 'titulo'
    nombre_del_libro = serializers.CharField(source='titulo')
    
    # Campo de solo lectura (no se pide al crear)
    autor = serializers.CharField(read_only=True)

    class Meta:
        model = Libro
        fields = ['id', 'nombre_del_libro', 'autor']
```

**Propiedades clave:**
-   `read_only=True`: Solo sale en el GET. No se pide en POST/PUT.
-   `write_only=True`: Solo se pide en POST/PUT (ej: passwords). No sale en el GET.
-   `required=False`: No es obligatorio enviarlo.

---

## 3. Validaciones (El Portero)

DRF valida tipos automáticamente (que un entero sea entero). Tú añades la lógica de negocio.

### A. Validación de UN campo (`validate_<campo>`)
```python
    def validate_titulo(self, value):
        # value es lo que ha enviado el usuario
        if "prohibido" in value.lower():
            raise serializers.ValidationError("No puedes usar esa palabra.")
        return value # Siempre devolver el valor (limpio)
```

### B. Validación de TODO el objeto (`validate`)
Para comparar dos campos entre sí.
```python
    def validate(self, data):
        # data es un diccionario con todos los campos
        if data['titulo'] == data['resumen']:
            raise serializers.ValidationError("El título y el resumen no pueden ser iguales.")
        return data
```

---

## 4. Campos Calculados (`SerializerMethodField`)
Para enviar datos que **NO existen** en la base de datos, sino que se calculan al vuelo.
*Siempre son de solo lectura.*

```python
class LibroExtraSerializer(serializers.ModelSerializer):
    es_largo = serializers.SerializerMethodField()
    nombre_completo_autor = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = ['titulo', 'es_largo', 'nombre_completo_autor']

    # La función debe llamarse: get_<nombre_del_campo>
    def get_es_largo(self, obj):
        # obj es la instancia del Libro
        return obj.paginas > 500

    def get_nombre_completo_autor(self, obj):
        return f"{obj.autor.first_name} {obj.autor.last_name}"
```

---

## 5. Relaciones (ForeignKeys y ManyToMany)

¿Cómo representamos al `autor` de un libro?

### A. Por ID (Defecto)
```python
# JSON: { "titulo": "Libro", "autor": 1 }
```

### B. Por String (`StringRelatedField`)
Usa el método `__str__` del modelo relacionado.
```python
# JSON: { "titulo": "Libro", "autor": "Cervantes" }
autor = serializers.StringRelatedField()
```

### C. Por Slug (`SlugRelatedField`)
Usa un campo específico (ej: el nombre o el DNI) en vez del ID.
```python
# JSON: { "titulo": "Libro", "autor": "miguel-de-cervantes" }
autor = serializers.SlugRelatedField(slug_field='slug', read_only=True)
```

### D. Anidado (Nested Serializer)
Meter el objeto entero dentro.
```python
class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id', 'nombre']

class LibroNestedSerializer(serializers.ModelSerializer):
    # Usamos el otro serializer como campo
    autor = AutorSerializer() 
    
    class Meta:
        model = Libro
        fields = ['titulo', 'autor']

# JSON: 
# { 
#   "titulo": "Quijote", 
#   "autor": { "id": 1, "nombre": "Cervantes" } 
# }
```
**¡CUIDADO!** Los nested serializers son de solo lectura por defecto. Para crear/editar datos anidados hay que sobreescribir el método `create()` o `update()` del serializer.

---

## 6. `create` y `update` (Magia Oscura)

Solo necesitas tocarlos si vas a guardar datos en tablas relacionadas a la vez.

```python
    def create(self, validated_data):
        # Sacamos los datos anidados (ej: crear Autor a la vez que Libro)
        autor_data = validated_data.pop('autor') 
        
        # Creamos el autor primero
        autor_obj = Autor.objects.create(**autor_data)
        
        # Creamos el libro asignándole el autor
        libro = Libro.objects.create(autor=autor_obj, **validated_data)
        
        return libro
```
