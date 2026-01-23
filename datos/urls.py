from django.urls import path 
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [path("calcula/", views.calcula.as_view()),
               path("hola/", views.holaMundo),
               path("login/", TokenObtainPairView.as_view() )]





