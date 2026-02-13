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
		
		

class Autores(serializers.ModelSerializer):
	class Meta:
		model = Autor
		fields = "__all__"

"""
class LibroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio', 'stock', 'autor']
        read_only_fields = ['autor']  # El usuario no puede enviarlo

    # 🔹 Validación por campo
    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "El precio debe ser mayor que 0."
            )
        return value

    # 🔹 Otra validación por campo
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "El stock no puede ser negativo."
            )
        return value

    # 🔹 Validación global
    def validate(self, data):
        if "prohibido" in data.get("titulo", "").lower():
            raise serializers.ValidationError(
                "El título contiene una palabra prohibida."
            )
        return data

    # 🔹 CREATE personalizado
    def create(self, validated_data):
        request = self.context.get('request')

        validated_data['autor'] = request.user

        libro = Libro.objects.create(**validated_data)
        return libro

    # 🔹 UPDATE personalizado
    def update(self, instance, validated_data):

        # Evitamos cambiar autor
        validated_data.pop('autor', None)

        instance.titulo = validated_data.get(
            'titulo', instance.titulo
        )
        instance.precio = validated_data.get(
            'precio', instance.precio
        )
        instance.stock = validated_data.get(
            'stock', instance.stock
        )

        instance.save()
        return instance


"""



"""

from rest_framework import serializers
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):

    class Meta:
        model = Libro
        fields = ['id', 'titulo', 'precio', 'descuento']

    # 🔹 Validación global
    def validate(self, data):
        precio = data.get('precio', 0)
        descuento = data.get('descuento', 0)

        # Validación cruzada
        if descuento > precio:
            raise serializers.ValidationError(
                "El descuento no puede ser mayor que el precio."
            )

        # Si quieres calcular un valor derivado
        data['precio_final'] = float(precio) - float(descuento)

        return data





"""


