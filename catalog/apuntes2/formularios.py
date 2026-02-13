from django import forms
from catalog.models import Book, Author, Genre

# =============================================================================
# 1. FORMS NORMALES (forms.Form)
# Usando un "QuerySet Ficticio" (lista de tuplas) para simular datos de BBDD.
# =============================================================================

# Imaginemos que esto viene de una BBDD o API externa
QUERYSET_FICTICO = [
    ('id_1', 'Opción A (Ficticia)'),
    ('id_2', 'Opción B (Ficticia)'),
    ('id_3', 'Opción C (Ficticia)'),
    ('id_4', 'Opción D (Ficticia)'),
]

class EjemploWidgetsForm(forms.Form):
  
    # A. SELECT SIMPLE (El desplegable de toda la vida)
    # -------------------------------------------------------------------------
    select_simple = forms.ChoiceField(
        choices=QUERYSET_FICTICO,
        label="Select Simple (ChoiceField)",
        widget=forms.Select(attrs={'class': 'mi-clase'})
    )

    # B. RADIO BUTTONS (Círculos, selección única)
    # -------------------------------------------------------------------------
    radio_buttons = forms.ChoiceField(
        choices=QUERYSET_FICTICO,
        label="Radio Buttons (ChoiceField + RadioSelect)",
        widget=forms.RadioSelect
    )

    # C. SELECT MÚLTIPLE (Caja con opciones, Ctrl+Click)
    # -------------------------------------------------------------------------
    select_multiple = forms.MultipleChoiceField(
        choices=QUERYSET_FICTICO,
        label="Select Múltiple (MultipleChoiceField)",
        widget=forms.SelectMultiple
    )

    # D. CHECKBOXES (Cuadrados, selección múltiple)
    # -------------------------------------------------------------------------
    checkboxes = forms.MultipleChoiceField(
        choices=QUERYSET_FICTICO,
        label="Checkboxes (MultipleChoiceField + CheckboxSelectMultiple)",
        widget=forms.CheckboxSelectMultiple
    )


# =============================================================================
# 2. MODEL FORMS (forms.ModelForm)
# Aquí transformamos los campos de relaciones (ForeignKey/ManyToMany) en widgets.
# =============================================================================

class LibroForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['author', 'genre'] # Solo relaciones para este ejemplo
        
        widgets = {
            # ForeignKey (Autor): Por defecto es un Select.
            # Lo cambiamos a RADIO BUTTONS (Círculos).
            'author': forms.RadioSelect(),
            
            # ManyToMany (Géneros): Por defecto es un Select Multiple.
            # Lo cambiamos a CHECKBOXES (Cuadrados).
            'genre': forms.CheckboxSelectMultiple(),
        }
        
        labels = {
            'author': 'Selecciona UN Autor (Radio)',
            'genre': 'Selecciona VARIOS Géneros (Checkbox)',
        }
