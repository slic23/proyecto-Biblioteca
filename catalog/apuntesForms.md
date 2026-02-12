# Apuntes: Django Forms vs ModelForms

Una guía rápida para no dudar entre uno u otro.

---

## 1. `forms.Form` (Manual)
Úsalo cuando el formulario **NO** guarda datos directamente en un modelo (ej: Contacto, Filtros de búsqueda, Login).

**Claves:**
-   Defines cada campo a mano.
-   Tú controlas el tipo (`CharField`, `DateField`...).
-   Tienes que escribir más código para guardar.

**Ejemplo:**
```python
from django import forms
from .models import Book

class BuscadorForm(forms.Form):
    # Campo de texto simple
    termino = forms.CharField(label="Buscar", max_length=100)
    
    # Checkbox simple (Booleano)
    solo_disponibles = forms.BooleanField(required=False)
    
    # Select cargando datos de la BBDD (ModelChoiceField)
    # queryset: Qué datos cargar.
    # empty_label: Texto por defecto ("Selecciona...").
    categoria = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        empty_label="Cualquier género",
        required=False
    )
```

---

## 2. `forms.ModelForm` (Automático)
Úsalo cuando el formulario **SÍ** va a crear o editar un registro en la base de datos (ej: Crear Libro, Editar Perfil).

**Claves:**
-   Se vincula a un modelo (`model = Libro`).
-   Django crea los campos automáticamente.
-   `form.save()` guarda el objeto directamente.
-   Usas `widgets` para cambiar la apariencia HTML.

**Ejemplo:**
```python
from django import forms
from .models import BookInstance

class EjemplarForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'imprent', 'due_back', 'status']
        
        # WIDGETS: La magia para cambiar el HTML sin tocar la lógica
        widgets = {
            # Cambiar input de fecha por calendario nativo
            'due_back': forms.DateInput(attrs={'type': 'date'}),
            
            # Cambiar un Select por Radio Buttons (bolitas)
            'status': forms.RadioSelect(),
            
            # Añadir clases CSS o placeholders
            'imprent': forms.TextInput(attrs={'class': 'mi-clase-css', 'placeholder': 'Editorial...'})
        }
```

---

## 3. Widgets Útiles (Copia y pega)

| Widget | HTML que genera | Cuándo usarlo |
| :--- | :--- | :--- |
| `forms.TextInput(attrs={'placeholder': '...'})` | `<input type="text">` | Texto corto. |
| `forms.Textarea(attrs={'rows': 3})` | `<textarea>` | Texto largo. |
| `forms.DateInput(attrs={'type': 'date'})` | `<input type="date">` | Calendarios. |
| `forms.PasswordInput` | `<input type="password">` | Contraseñas (no se ven). |
| `forms.CheckboxSelectMultiple` | Lista de `<input type="checkbox">` | Selección múltiple visual. |
| `forms.RadioSelect` | Lista de `<input type="radio">` | Selección única visual. |

---

## 4. `ModelChoiceField` vs `ModelMultipleChoiceField`

-   **`ModelChoiceField`**: Eliges UNO (Dropdown por defecto).
-   **`ModelMultipleChoiceField`**: Eliges VARIOS (Lista con Ctrl por defecto). *Truco: Úsalo con `widget=forms.CheckboxSelectMultiple` para que sean casillas.*
