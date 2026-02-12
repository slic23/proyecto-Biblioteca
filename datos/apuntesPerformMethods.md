# Apuntes: Los Métodos `perform_...` (Interceptar Guardado)

**¿Funciona igual en `generics` y `ViewSets`?**
¡SÍ! Absolutamente. Ambos heredan de la misma clase madre, así que esto sirve para los dos.

---

## ¿Para qué sirven?
DRF hace el `save()` automáticamente. Pero a veces quieres meter mano JUSTO antes de que se guarde en la base de datos (para añadir datos que el usuario no envió, enviar correos, logs, etc.).

---

## 1. `perform_create(self, serializer)`
Se ejecuta en el **POST**. Ideal para asignar el "dueño" del objeto.

```python
def perform_create(self, serializer):
    # El usuario no envía su ID en el JSON, se lo pegamos nosotros aquí
    serializer.save(usuario=self.request.user)
    
    # También puedes hacer cosas extra después
    print("¡Se ha creado un libro nuevo!")
```

---

## 2. `perform_update(self, serializer)`
Se ejecuta en el **PUT** y **PATCH**. Ideal para actualizar campos automáticos (como "fecha de última edición") o lógica extra.

```python
def perform_update(self, serializer):
    # Guardamos los cambios
    instance = serializer.save()
    
    # Lógica extra: Enviar un email si se cambió algo importante
    if instance.estado == 'publicado':
        enviar_email_aviso(instance)
```

---

> [!NOTE]
> **¿Existe `perform_partial_update`?**
> **NO**.
> `perform_update` maneja TANTO las actualizaciones completas (`PUT`) como las parciales (`PATCH`). El serializer ya sabe si es parcial o no al validarse (`partial=True`), así que tú solo te preocupas de `perform_update`.

---

## 3. `perform_destroy(self, instance)`
Se ejecuta en el **DELETE**. **OJO**: Aquí no hay serializer, recibes la `instance` (el objeto) directamente.

```python
def perform_destroy(self, instance):
    # Lógica extra antes de borrar
    print(f"Borrando el libro {instance.titulo}...")
    
    # Ejecutas el borrado real
    instance.delete()
```

---

## Resumen

| Método | Cuándo salta | Qué recibe | Para qué usarlo |
| :--- | :--- | :--- | :--- |
| **`perform_create`** | POST | `serializer` | Asignar usuario (`request.user`), datos por defecto. |
| **`perform_update`** | PUT / PATCH | `serializer` | Actualizar timestamps, logs de cambios, notificaciones. |
| **`perform_destroy`** | DELETE | `instance` | Borrado lógico (soft delete), limpiar archivos asociados. |
