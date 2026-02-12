from django.urls import path , include 
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'librosSet', views.EjemplosViewset, 
             )
router.register( r"aprobando", views.aprobando ,  basename="aprobando" )


urlpatterns = [path("calcula/", views.calcula.as_view()),
               path("hola/", views.holaMundo),
               path("login/", TokenObtainPairView.as_view() ), 
               path("todosLibros/", views.lecturaLibros.as_view()), 
               path("libros/<int:pk>", views.libros.as_view()), 
               path("libros/", views.libros.as_view()), 
               path("libross/<int:pk>", views.tresAcciones.as_view()), 
               path("libross/", views.listarLibros.as_view()), 
               path("ejemplo/",views.ejemplo2),
               path("", include(router.urls)), 
               path("sumar/", views.sumar)  , 
               path("secreto/", views.secreto), 
               path("crudManual/<int:pk>/", views.lecturModifEliminacion), 
               path("crudApi/", views.crudApi.as_view()), 
               path("crudApi/<int:pk>/", views.crudApi.as_view()), 
               path("libritos/", views.listarCrear.as_view()), 
               path("libritos/<int:pk>/", views.recuperarCambiarDestroy.as_view())
               ]
               




