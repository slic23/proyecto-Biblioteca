from django.db import models

# Create your models here.

class libro(models.Model):
    titulo = models.CharField(max_length= 100)
    autor = models.CharField(max_length= 100)
    disponible = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.titulo} {self.autor}"
    
    
    
class Autor(models.Model):
    nombre = models.CharField(max_length= 100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_muerte = models.DateField(null=True, blank=True)
    
    
    