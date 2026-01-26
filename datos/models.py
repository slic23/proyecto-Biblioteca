from django.db import models

# Create your models here.

class libro(models.Model):
    titulo = models.CharField(max_length= 100)
    autor = models.CharField(max_length= 100)
    disponible = models.BooleanField(default=True)
    