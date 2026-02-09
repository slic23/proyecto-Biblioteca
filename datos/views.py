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




class lecturaLibros(APIView):
    def get(self, request):
        libro = Book.objects.all()
        serializer = serializers.libros(libro, many=True)
        return Response(serializer.data)



    def post(self,request):
        pass



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