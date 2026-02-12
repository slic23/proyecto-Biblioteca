from django.db import models
from django.urls import reverse 
import uuid
from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
    """
    modelo representa a los genereos literarios 
    """
    name = models.CharField(max_length= 200,help_text="Introduce un genero")
    def __str__(self):
        """
        Sobrescrbimos el str para que devuelva el nombre del genero
        """
        return self.name 

class Book(models.Model):
    """
    modelo que representa un libro 
    """
    title = models.CharField(max_length = 200, help_text= "Introduce el nombre del libro")
    author = models.ForeignKey("Author",on_delete = models.SET_NULL, null= True)
    summary = models.TextField(max_length = 1000 , help_text = "ingrese una breve descripcion del libro")

    genre = models.ManyToManyField(Genre,help_text = "Selecciona un genero")
    def display_genre(self):
        """
           crea un string para el admin 
        """
        return " ".join([genre.name for genre in self.genre.all()])
    display_genre.shortDescription = "Genre"
    isbn = models.CharField("ISBN",max_length = 13,help_text = "13 Caracteres <a href='https://www.isbn-international.org/content/what-isbn'ISBN number</a>")
    def __str__(self):
        return self.title 
    def get_absolute_url(self):
        return reverse("detalle-libro", args=[str(self.id)])
class BookInstance(models.Model):
    """
        Este modelo representa el ejemplar
    """
    id = models.UUIDField(primary_key = True, default=uuid.uuid4,help_text="id unico del ejemplar en toda la biblioteca")
    imprent = models.CharField(max_length= 200, help_text="Introduce el nombre de la editorial")
    due_back = models.DateField(null=True,blank = True)
    loan_status =(
            ("m","Maintenance"),
            ("o","on loan"),
            ("a","available"),
            ("r","reserverd")

        )
    pdf = models.FileField(upload_to="pdfs/", null=True, blank=True)
    video = models.FileField(upload_to="videos/", null=True , blank = True)
    book = models.ForeignKey(Book,on_delete = models.SET_NULL, null = True)
    lenguaje = models.ForeignKey("Language", on_delete = models.SET_NULL , null = True)
    status = models.CharField(max_length = 1, choices = loan_status, blank = True, default = "m",help_text = "Disponibilidad d del ejemplar")
    lector = models.ForeignKey("lector", on_delete= models.SET_NULL, null=True )
    portada = models.ImageField(upload_to="portadas/", null=True , blank=True)
    
    reservadores = models.ManyToManyField(
        "lector",
        through='Reservation',
        related_name='reservas'
    )
    class Meta: 
        ordering = ["due_back"]
    def __str__(self):
        return "%s  (%s)" % (self.id,self.book.title)

class Author(models.Model):
    """
        Modelo quer representa un autor 
    
    """
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField("Died",null = True, blank =True)

    
    def get_absolute_url(self):
        return  reverse("detalle-autor",args=[str(self.id)])

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Language(models.Model):
    lengua = models.CharField(max_length = 100)
    def __str__(self):
        return self.lengua




class lector(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length = 100)
    localidad = models.CharField(max_length =100)
    pronvincia = models.CharField(max_length = 100)
    fecha_nacimineto = models.DateField()
    penalizado = models.BooleanField(null=True, default=False)
    leidos = models.IntegerField(default=0)
    
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nombre  
    class Meta:
        permissions = (("can_mark_returned", "Set book as returned"),
                       ("bibliotecario_poder","Permiso alto rango"), 
                       ("carnet_lector", "permiso de lector"))
        

class Reservation(models.Model):
    usuario_reservador = models.ForeignKey(lector, on_delete=models.CASCADE, related_name="lectores", related_query_name="lectoresquery")
    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE, related_name= "ejemplares", related_query_name="ejemplaresquery")
    fecha_reserva = models.DateField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('pendiente','Pendiente'),
            ('aprobada','Aprobada'),
            ('rechazada','Rechazada'),
        ],
        default='pendiente'
    )







