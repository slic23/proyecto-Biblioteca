from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse 
from django.views import generic 
from .forms import LectorForm, FormularioRegistro, AvanzadoModel, PrestamoForm
import datetime

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
        lectorObjeto = lector.objects.get(pk=pk)



    else:
        lectorObjeto = None



    if request.method == "POST":
        form = AvanzadoModel(request.POST, instance=lectorObjeto)
        if form.is_valid():
            objeto = form.save(commit=False)
            if  lectorObjeto is None: 
            
                contras = form.cleaned_data.get("password2")
                usuarioSystem = User.objects.create_user(
                    username=objeto.nombre,
                    password=contras
                )
                objeto.usuario = usuarioSystem
            objeto.save()
            return redirect("index")
        

    else:
        form = AvanzadoModel(instance=lectorObjeto, initial={"aceptarTerminos": True})



    return render(request, "registro.html", {"form":form})



def prestarEjemplar(request, pk):
    objeto = get_object_or_404(BookInstance , pk= pk)
    if request.method == "POST":
        form =  PrestamoForm(request.POST, instance=objeto)

        if form.is_valid():

            guardado = form.save(commit=False)

            if "reservar" in request.POST:


                guardado.status = "r"
            elif "prestar" in request.POST:
                guardado.status = "b"

            elif "mantenimiento" in request.POST:
                guardado.status = "m"


            guardado.save()

            return redirect("prestados")

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = PrestamoForm(instance=objeto, initial={"due_back": proposed_renewal_date} )

    return render(request, "prestamo.html", {"form": form})



class EjemplaresDisponibles(generic.ListView):
    model = BookInstance
    template_name = "catalog/ejemplaresDisponibles.html"
    def get_queryset(self):
        return super().get_queryset().filter(status__exact = "a")
    




class detalleEjemplar(generic.DetailView):
    model = BookInstance
    







        



    
