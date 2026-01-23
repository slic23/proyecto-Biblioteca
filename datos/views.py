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




