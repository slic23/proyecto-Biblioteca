from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.views import generic 
from .forms import LectorForm, FormularioRegistro

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



def registro(request):
    if request.method == "POST":
        form = LectorForm(request.POST)
        if form.is_valid():
            objeto = form.save(commit=False)
            contras = form.cleaned_data.get("password2")
            usaurioSystem = User.objects.create_user(username = objeto.nombre, password = contras)

            objeto.usuario = usaurioSystem
            objeto.save()
            return redirect("index")
        

    else: 
        form = LectorForm()
    return render(request, "registro.html", {"form":form})

""" esto es un view que sirve un  formulario que me sirve para practicar entre forms, Modelform """
def registro2(request):
    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            qnombre = form.cleaned_data.get("nombre")
            qapellidos = form.cleaned_data.get("apellidos")
            qnacimiento = form.cleaned_data.get("fecha_nacimiento")
            qlocalidad = form.cleaned_data.get("localidad")
            qprovincia = form.cleaned_data.get("pronvincia")  
            qpassword2 = form.cleaned_data.get("password2")

            # creamos el objeto user 
            usuaro_sistema = User.objects.create_user(username=qnombre, password = qpassword2)
            lector1 = lector(nombre = qnombre, apellidos = qapellidos, localidad = qlocalidad, pronvincia = qprovincia, 
                             fecha_nacimineto = qnacimiento, usuario = usuaro_sistema)
            
            lector1.save()

            return redirect("index")

    else: 
        form = FormularioRegistro()


    return render(request, "registro.html", {"form":form})






def editarCrear(request, pk= None):
    if pk: 
        lectorobjeto = lector.objects.get(pk=pk)



    else:
        pass 
        
        



    
