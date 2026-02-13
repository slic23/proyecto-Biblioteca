from django.urls import path 
from .  import views
urlpatterns = [path('',views.index, name="index"),
               path("Libros/",views.ListaLibros.as_view(),name="listabooks"),
               path("Autores/",views.ListaAutores.as_view(),name="listaauthors"),
               path("Libros/<int:pk>",views.DetalleLibro.as_view(),name="detalle-libro"),
               path("Autores/<int:pk>",views.DetalleAutor.as_view(),name = "detalle-autor"),
               path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
               path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
               path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
               path("listaprestados/",views.ListaPrestados.as_view(),name = "prestados"), 
               path("registro/", views.registro, name="registro"), 
               path("registro2/", views.registro2, name = "registro2"), 
               path("registroEditar/", views.editarCrear, name="editarCrear"), 
               path("registroEditar/<int:pk>/", views.editarCrear, name="editarCrear"), 
               path("ejemplaresDisponibles/",views.EjemplaresDisponibles.as_view(), name="ejemplaresDisp"), 
               path("prestar/<uuid:pk>/", views.prestarEjemplar, name ="prestar"), 
               path("ejemplar/<uuid:pk>/", views.detalleEjemplar.as_view(), name="ejemplarDetalle"), 
               path("gestionReserva/<uuid:pk>/", views.gestionReserva, name="gestionReserva"), 
               path("panelReservas/", views.PanelReservas.as_view(), name="panelReservas"), 
               path("ControlReservas/", views.PanelReservasAdmin.as_view(), name="adminReservas"), 
               path("ControlFinal/<int:pk>/", views.controlReservas, name="control"), 
               path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='ampliarFecha'), 
               path("operacion/<uuid:pk>/", views.operacion, name="operacion")]







