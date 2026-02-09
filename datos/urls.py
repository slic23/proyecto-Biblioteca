from django.urls import path , include 
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'librosSet', views.EjemplosViewset)


urlpatterns = [path("calcula/", views.calcula.as_view()),
               path("hola/", views.holaMundo),
               path("login/", TokenObtainPairView.as_view() ), 
               path("todosLibros/", views.lecturaLibros.as_view()), 
               path("libros/<int:pk>", views.libros.as_view()), 
               path("libros/", views.libros.as_view()), 
               path("libross/<int:pk>", views.tresAcciones.as_view()), 
               path("libross/", views.listarLibros.as_view()), 
               path("", include(router.urls))
               ]





