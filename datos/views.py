from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view
from .permissions import TienesPermisoHola
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from catalog.models import *
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import * 
from  .  import serializers
class calcula(APIView):
    authentication_classes = [JWTAuthentication]
    def get_permissions(self):
       
        if self.request.method == "GET":
            return [AllowAny()]
        
        return [IsAuthenticated()]
    
    
    
    def get(self, request):
        return Response({"formula": (2+3)*23000})



    def post(self,request):
        formula = eval(request.data.get("formula"))

        return Response({"formula": formula})
@api_view(["get","post"])
@permission_classes([IsAuthenticated, TienesPermisoHola])
def holaMundo(request):
    if request.method =="GET":
        return Response({"mensaje": "Hola esto es un GET"})
    elif request.method == "POST":
        return Response({"mensaje": "datos recibidos", 
                         "datos": 
                               request.data
                              })


"""
estoy probando aqui diferentes maneras de usar las 4 maneras de trabajar con apis
con ejemplo sencillos hasta trabajar con bbdd, borrar elementos, crear, cambiar y eliminar 

"""


@api_view(["get","post"])
def ejemplo2(request):
    if request.method =="GET":
        dato = request.query_params.get("nombre", None)
        if dato:
            return Response({"mensaje":f"hola {dato} este es un mensaje"}, status = status.HTTP_200_OK)
        return Response({"mensaje": "Hola esto es una prueba"})
    
    elif request.method == "POST":
        return Response({"mensaje": "Estado recibido",
    
    
                      "datos": request.data})

class lecturaLibros(APIView):
    def get(self, request):
        libro = Book.objects.all()
        serializer = serializers.libros(libro, many=True)
        return Response(serializer.data)



    def post(self,request):
        pass


@api_view(["get","post"])
def sumar(request):
    if request.method == "GET":
        return Response({"a": 1, 
                         "b": 2}, status = status.HTTP_200_OK )
        
        
    elif request.method == "POST":
        a = request.data.get("a")
        b = request.data.get("b")  
        try: 
           a =  float(a)
           b = float(b)
            
            
        except (TypeError , ValueError):
            return Response({"error": "deben ser numeros"}, status=status.HTTP_400_BAD_REQUEST)
             
            
        
        
        return Response({"resultado": a + b  }  , status = status.HTTP_200_OK)
        
class libros(APIView):

    def get(self,request, pk = None) :
        if pk: 
            libroB = libro.objects.get(pk=pk)
            serializer = serializers.LibroBasico(libroB)
            return Response(serializer.data)

        else: 
            libros = libro.objects.all()
            serializer = serializers.LibroBasico(libros, many = True)
            return Response(serializer.data)



class listarLibros(generics.ListCreateAPIView):
    
    serializer_class = serializers.LibroBasico

    def get_queryset(self):
        queryset = libro.objects.all()
        titulo = self.request.query_params.get("titulo")

        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)

        return queryset

        
class tresAcciones(generics.RetrieveUpdateDestroyAPIView):
    queryset = libro.objects.all()
    serializer_class = serializers.LibroBasico
    
    
    
class AutorLecturaCreacion(generics.ListCreateAPIView):
    pass 



class AutoresCRUD(generics.RetrieveUpdateDestroyAPIView):
    pass 


class EjemplosViewset(viewsets.ModelViewSet):
    queryset = libro.objects.all()
    serializer_class = serializers.LibroBasico