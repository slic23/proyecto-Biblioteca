from rest_framework import serializers
from catalog.models import *
from .models import *

class libros(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = "__all__"



class LibroBasico(serializers.ModelSerializer):
	class Meta:
		model = libro
		fields = "__all__"
		








