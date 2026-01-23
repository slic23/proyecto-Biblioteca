from django.shortcuts import render
from django.http import HttpResponse 
from django.views import generic 

#Create your views here.
from .models import *
def index(request):
    num_books = Book.objects.all().count()
    num_autores = Author.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instancesAv = BookInstance.objects.filter(status__exact = "a").count()
    context = {
            "num_books" : num_books,
            "num_instances": num_instances,
            "num_instancesAv": num_instances,
            "num_autores": num_autores

            }

    return render(request,"index.html", context)
class ListaLibros(generic.ListView):
    model = Book


class ListaAutores(generic.ListView):

    model = Author
class DetalleLibro(generic.DetailView):
    model = Book
class DetalleAutor(generic.DetailView):
    model = Author

class ListaPrestados(generic.ListView):
    model = BookInstance 
    def get_queryset(self):
        return super().get_queryset().filter(status__exact = "o")
