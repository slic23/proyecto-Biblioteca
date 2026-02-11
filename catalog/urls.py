from django.urls import path 
from .  import views
urlpatterns = [path('',views.index, name="index"),
               path("Libros/",views.ListaLibros.as_view(),name="listabooks"),
               path("Autores/",views.ListaAutores.as_view(),name="listaauthors"),
               path("Libros/<int:pk>",views.DetalleLibro.as_view(),name="detalle-libro"),
               path("Autores/<int:pk>",views.DetalleAutor.as_view(),name = "detalle-autor"),
               path("listaprestados/",views.ListaPrestados.as_view(),name = "prestados"), 
               path("registro/", views.registro, name="registro"), 
               path("registro2/", views.registro2, name = "registro2")]




