from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view
from .permissions import TienesPermisoHola, EsStaff  , EsAdulto
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

@api_view(["get","put","delete"])

def lecturModifEliminacion(request, pk):
    try: 
        book = libro.objects.get(pk=pk)


        if request.method == "GET":
            return Response({"id":book.pk, 
                         "titulo":book.titulo,
                         "autor":book.autor,
                         "disponible":book.disponible}, status=status.HTTP_200_OK)
        
        elif request.method == "PUT":
            titulo = request.data.get("titulo")
            autor = request.data.get("autor")
            disponible = request.data.get("disponible")

            book.titulo = titulo
            book.autor = autor 
            book.disponible = disponible
            book.save()
            return Response({"id":book.pk, 
                         "titulo":book.titulo,
                         "autor":book.autor,
                         "disponible":book.disponible}, status=status.HTTP_200_OK)
             
        elif request.method == "DELETE":
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
         

    except libro.DoesNotExist:
        return Response({"error":"El libro no existe"}, status=status.HTTP_404_NOT_FOUND)



@api_view(["get","post"])
@permission_classes([EsStaff])
def secreto(request):
    if request.method =="GET":
        return Response({"Entrada":"bienvenido has podido pasar porque eres staff"})
    
    elif request.method =="POST":
        return Response({"servicio":"secreto","datos":request.data}, status=status.HTTP_200_OK)


@api_view(["get","post"])
def ejemplo2(request):
    if request.method =="GET":
        dato = request.query_params.get("nombre", None)
        if dato:
            return Response({"mensaje":f"hola {dato} este es un mensaje"}, status = status.HTTP_200_OK)
        return Response({"mensaje": "Hola esto es una prueba"})
    
    elif request.method == "POST":

        if not request.data:
            return Response({"Error":"no se enviaron datos"}, status=status.HTTP_400_BAD_REQUEST)
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



class crudApi(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method in ["GET"]:
            return [AllowAny()]
        
        return [IsAuthenticated()]


    

    def get_object(self, pk):
       return get_object_or_404(libro, pk=pk)
    





    def get(self, request, pk = None):
        if pk:
            book = self.get_object(pk)
            serializer = serializers.LibroBasico(book)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else: 
            libros = libro.objects.all()
            serializer = serializers.LibroBasico(libros,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):

        serializer = serializers.LibroBasico(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        
    def put(self,request,pk):
        objeto = self.get_object(pk)
        serializer = serializers.LibroBasico(objeto,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request, pk ):
        objeto = self.get_object(pk)
        objeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request,pk):
        objeto = self.get_object(pk)
        serializer = serializers.LibroBasico(objeto,data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class listarCrear(generics.ListCreateAPIView):
    serializer_class = serializers.Autores

    def get_queryset(self):
        dato = self.request.query_params.get("nombre")
        queryset = Autor.objects.all()
        if dato: 
            queryset = Autor.objects.filter(nombre__icontains =dato)
        return queryset
    

    def get_permissions(self):
        if self.request.method == "POST":
            return [EsAdulto()]

        return [AllowAny()]        


    
class recuperarCambiarDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.Autores
    queryset = Autor.objects.all()



@api_view(["GET"])
@permission_classes([IsAdminUser])
def holaMundo(request):
    return Response({"mensaje": "hola mundo"}, status=status.HTTP_200_OK)








class aprobando(viewsets.ModelViewSet):
    queryset = libro.objects.all()
    serializer_class = serializers.LibroBasico

    def get_permissions(self):
        """
        Asigna permisos según la acción que se está ejecutando en el ViewSet.
        self.action corresponde a: 'list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'
        """

        # Listar y ver detalle → cualquiera puede ver
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        # Crear → solo usuarios autenticados
        elif self.action == "create":
            return [IsAuthenticated()]

        # Actualizar completo o parcial → solo admins
        elif self.action in ["update", "partial_update"]:
            return [IsAdminUser()]

        # Borrar → solo admins
        elif self.action == "destroy":
            return [IsAdminUser()]

        # Si la acción no coincide con las anteriores, usar permisos por defecto del ViewSet
        return super().get_permissions()
    


    def perform_create(self, serializer):
        datos = serializer.validated_data

        print(datos)

        serializer.save()

        


################### APUNTES 



# -----------------------------------------------------------------------------
# EJEMPLOS DE CÓDIGO SIMPLIFICADO (LO QUE MÁS USARÁS)
# -----------------------------------------------------------------------------

# 1. FUNCIÓN SIMPLE (@api_view)
# Lo más fácil: usas decoradores para método y permisos.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) # Solo gente logueada
def funcion_simple(request):
    if request.method == 'GET':
        libros = libro.objects.all()
        serializer = serializers.LibroBasico(libros, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = serializers.LibroBasico(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. CLASE APIView (Más ordenado)
# Separas la lógica en métodos (get, post, put...)
class LibroAPIViewSimple(APIView):
    permission_classes = [IsAdminUser] # Solo admins

    def get(self, request):
        # Lógica de listar
        libros = libro.objects.filter(disponible=True) # Ejemplo: solo disponibles
        serializer = serializers.LibroBasico(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Lógica de crear
        serializer = serializers.LibroBasico(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3. GENERIC VIEW (Casi automático)
# Le dices qué modelo y qué serializer, y él hace el trabajo sucio.
class ListarCrearLibros(generics.ListCreateAPIView):
    queryset = libro.objects.all()
    serializer_class = serializers.LibroBasico
    permission_classes = [IsAuthenticated] # O el que quieras


# 4. VIEWSET SIMPLE (Todo automático)
# CRUD completo en 3 líneas. Sin complicaciones.
class LibroViewSetSimple(viewsets.ModelViewSet):
    queryset = libro.objects.all()
    serializer_class = serializers.LibroBasico
    # Permisos simples:
    permission_classes = [IsAuthenticated] 
    
    # Si quieres filtrar por usuario (muy común):
    def get_queryset(self):
        # Retorna solo los libros del usuario que hace la petición
        return libro.objects.filter(autor__usuario=self.request.user)

# 5. INTERCEPTANDO EL GUARDADO (perform_create, perform_update, perform_destroy)
# Estos métodos sirven para meter lógica JUSTO ANTES de guardar en base de datos.
# Funcionan IGUAL en GenericAPIView y en ModelViewSet.

class LibroConLogicaGuardado(viewsets.ModelViewSet):
    queryset = libro.objects.all()
    serializer_class = serializers.LibroBasico
    permission_classes = [IsAuthenticated]

    # SE EJECUTA EN: POST (Crear)
    def perform_create(self, serializer):
        # El usuario no envía su ID en el JSON, se lo pegamos nosotros aquí automágicamente
        # serializer.save() guarda el objeto, y le puedes pasar campos extra
        print(f"Creando libro... Usuario: {self.request.user}")
        serializer.save(autor__usuario=self.request.user) 

    # SE EJECUTA EN: PUT y PATCH (Actualizar total o parcial)
    def perform_update(self, serializer):
        # Antes de guardar
        print("Actualizando libro...")
        
        # Guardamos (esto devuelve la instancia ya actualizada)
        instancia = serializer.save()
        
        # Después de guardar (ej: enviar correo si cambió el estado)
        if instancia.disponible == False:
            print(f"El libro {instancia.titulo} ya no está disponible.")

    # SE EJECUTA EN: DELETE (Borrar)
    def perform_destroy(self, instance):
        # Aquí NO hay serializer, recibes el objeto (instance) directo
        print(f"Borrando el libro {instance.titulo} para siempre...")
        
        # Ejecutas el borrado real (o podrías hacer un 'soft delete' cambiando un campo activo=False)
        instance.delete()
