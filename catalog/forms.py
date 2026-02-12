from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data






class LectorForm(forms.ModelForm):
    password1 = forms.CharField(max_length=100, widget= forms.PasswordInput)
    password2 = forms.CharField(max_length=100 , widget=forms.PasswordInput)

    class Meta:
        model = lector
        exclude = ["usuario",]
        widgets = {
                "fecha_nacimineto": forms.DateInput(attrs={"type": "date"}),
            }


    def clean(self):
        cleaned_data = super().clean() 
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1!= password2:
            raise ValidationError(_("Las contraseñas no coinciden, vuelve a ponerlas"))
        

        return cleaned_data
    




class FormularioRegistro(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length = 100)
    localidad = forms.CharField(max_length =100)
    pronvincia = forms.CharField(max_length = 100)
    fecha_nacimiento =forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise ValidationError(_("Las contraseñas no coinciden"))
        return cleaned_data
        
        


class AvanzadoModel(forms.ModelForm):
    password1 = forms.CharField(max_length=100, widget= forms.PasswordInput)
    password2 = forms.CharField(max_length=100 , widget=forms.PasswordInput)
    aceptarTerminos= forms.BooleanField(required=True, label="Acepte terminos")
    class Meta:
        model = lector
        exclude = ["usuario"]
        widgets = {"nombre": forms.TextInput(attrs={"placeholder":"tu nombre"}), 
                   "apellidos": forms.TextInput(attrs= {"placeholder": "tus apellidos" }), 
                   " localidad": forms.TextInput(attrs={"placeholder":"introduce la localidad"}),
                   "fecha_nacimineto": forms.TextInput(attrs={"placeholder": "introduce fecha de nacimiento", "type":"date"})}
        



    def clean(self):
        cleaned_data = super().clean()
        dato = cleaned_data.get("aceptarTerminos")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError(_("Las contraseñas no coinciden"))
        if not dato:

            self.add_error("Tienes que aceptar los terminos, si quieres continuar")



        return cleaned_data
    




class PrestamoForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ["book", "lector", "due_back"]
        widgets = {"due_back": forms.DateInput(attrs={"type":"date"}),
                   "lector":forms.Select(),
                   "book":forms.Select() 
                   }






                    




# -----------------------------------------------------------------------------
# EJEMPLO SOLICITADO: FORMS.FORM CON WIDGETS Y QUERYSETS (LO QUE NECESITAS)
# -----------------------------------------------------------------------------

class FormularioSimpleWidgets(forms.Form):
    # 1. SELECT SIMPLE (DROPDOWN) DESDE BASE DE DATOS
    # Carga todos los libros de la BD en un desplegable
    libro_favorito = forms.ModelChoiceField(
        queryset=Book.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Elige tu libro favorito",
        empty_label="-- Selecciona un libro --"
    )

    # 2. CHECKBOXES MULTIPLES DESDE BASE DE DATOS
    # Carga todos los autores, pero en lugar de lista, salen casillas para marcar varios
    autores_preferidos = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Marca tus autores preferidos"
    )

    # 3. RADIO BUTTONS (CIRCULITOS) CON OPCIONES FIJAS
    # Opciones escritas a mano
    TIPO_PORTADA = (
        ('dura', 'Tapa Dura'),
        ('blanda', 'Tapa Blanda'),
        ('digital', 'Ebook'),
    )
    portada = forms.ChoiceField(
        choices=TIPO_PORTADA,
        widget=forms.RadioSelect, # <--- Esto lo convierte en bolitas
        label="¿Qué formato prefieres?"
    )

    # 4. SELECT MULTIPLE (LISTA CON CTRL) DESDE BASE DE DATOS
    # Igual que el punto 2, pero en lista nativa (incómodo de usar, mejor Checkbox)
    generos = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label="Selecciona géneros (usa Ctrl para varios)"
    )



"""

class modelfORM(forms.Form):
    atributo = forms.ModelChoiceField(queryset="", widget=forms.Select())


    atribut2 = forms.ModelMultipleChoiceField(queryset= "", )




"""

