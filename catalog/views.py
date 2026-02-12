from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse 
from django.views import generic 
from .forms import LectorForm, FormularioRegistro, AvanzadoModel, PrestamoForm
import datetime
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from .forms import RenewBookForm
from .models import *

#Create your views here.

# -----------------------------------------------------------------------------
#                                 VISTAS GENERALES
# -----------------------------------------------------------------------------

def index(request):
    """
    esta funcion es la pagina principal , cuenta los libros y autores que hay en la base de datos 
    y los muestra en el template .
    """
    num_books = Book.objects.all().count()
    num_autores = Author.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instancesAv = BookInstance.objects.filter(status__exact = "a").count()
    numero = request.session.get("numero", 0)
    numero += 1
    request.session["numero"] = numero
    context = {
            "num_books" : num_books,
            "num_instances": num_instances,
            "num_instancesAv": num_instances,
            "num_autores": num_autores,
            "visitas": numero
            }

    return render(request,"index.html", context)


# -----------------------------------------------------------------------------
#                           CLASES GENERICAS (LISTAS Y DETALLES)
# -----------------------------------------------------------------------------

class ListaLibros(generic.ListView):
    model = Book
    paginate_by = 4



class ListaAutores(generic.ListView):

    model = Author
    paginate_by = 3

class DetalleLibro(generic.DetailView):
    """
    muestra el detalle de un libro en concreto , todo lo que tiene 
    """
    model = Book

class DetalleAutor(generic.DetailView):
    """
    muestra el detalle del autor , sus libros y sus cosas 
    """
    model = Author

class EjemplaresDisponibles(generic.ListView):
    model = BookInstance
    template_name = "catalog/ejemplaresDisponibles.html"
    paginate_by = 3
    def get_queryset(self):
        lector1 = lector.objects.filter(nombre__exact = self.request.user.username).first()
        reservas_usuario = Reservation.objects.filter(usuario_reservador=lector1).values_list('book_instance__pk', flat=True)
        return super().get_queryset().filter(status__exact = "a" ).exclude(pk__in = reservas_usuario)
    

class detalleEjemplar(generic.DetailView):
    model = BookInstance
    

# -----------------------------------------------------------------------------
#                           REGISTRO Y GESTION DE USUARIOS
# -----------------------------------------------------------------------------

def registro(request):
    """
    esta funcion registra un nuevo lector en el sistema , crea el usuario y el lector a la vez 
    """
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
    """
    esta funcion sirve para editar un lector si existe , o crearlo si no existe , 
    comprueba si hay pk o no .
    """
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


# -----------------------------------------------------------------------------
#                           VISTAS DE LECTOR (INVENTARIO Y RESERVAS)
# -----------------------------------------------------------------------------

    """
    Esta consulta listo los ejemplares del lector que tiene tomados. 
    para en caso de devolverlos ,o pedir una ampliacion de la fecha. 
    """

class ListaPrestados(generic.ListView):
    model = BookInstance 
    paginate_by = 2
    def get_queryset(self):
        return super().get_queryset().filter(status__exact = "o", lector__nombre__exact = self.request.user.username)


"""
gestion de la reserva, no pueden reservar los que no cumplan estas normas 

"""
def gestionReserva(request, pk): 
    objetoEmplar = get_object_or_404(BookInstance,pk = pk)
    usuario = lector.objects.filter(nombre__exact = request.user.username).first()
    usuarioNum =Reservation.objects.filter(usuario_reservador__pk = usuario.pk).count()
    if usuarioNum >=5 :

        messages.error(request, "No puedes reservar más de 5 libros")

    elif usuario.penalizado:
        messages.error(request, "No puedes reservar estas penalizado")


    elif usuario.leidos <= 12:
        messages.error(request, "No lees con frecuencia") 




    else: 
      
        Reservation.objects.create(usuario_reservador = usuario, book_instance = objetoEmplar)
       
    return redirect("panelReservas")


class PanelReservas(generic.ListView):
    model = Reservation
    template_name = "catalog/reservasPanel.html"
    paginate_by = 2
    
    def get_queryset(self):
        lector1 = lector.objects.filter(nombre__exact = self.request.user.username).first()
        return Reservation.objects.filter(usuario_reservador=lector1)


# -----------------------------------------------------------------------------
#                           VISTAS DE ADMINISTRACION Y BIBLIOTECARIOS
# -----------------------------------------------------------------------------

class PanelReservasAdmin(PermissionRequiredMixin,generic.ListView):
    """
    esta vista es para el admin , ve las reservas que estan pendientes de aprobar o rechazar 
    """
    model = Reservation
    template_name = "catalog/reservasAdminControl.html"
    paginate_by = 4
    permission_required = "catalog.bibliotecario_poder"
    def get_queryset(self):
        return super().get_queryset().filter(estado__iexact="pendiente")
    
@login_required
@permission_required("catalog.bibliotecario_poder")
def controlReservas(request, pk):
    """
    esta funcion es la logica para aceptar o rechazar las reservas de los usuarios 
    """
    
    reserva = get_object_or_404(Reservation, pk= pk)
    objetoEjemplar = BookInstance.objects.get(pk = reserva.book_instance.pk)
    usuario = lector.objects.get(pk= reserva.usuario_reservador.pk)
    print()

    if  "rechazar" in request.POST: 
        print("hola")
        reserva.estado = "rechazada"
        

    elif "prestar" in request.POST: 
        print("adios")
        reserva.estado = "aprobada"
        objetoEjemplar.lector = usuario
        objetoEjemplar.status = "o"
        objetoEjemplar.due_back =  datetime.date.today() + datetime.timedelta(weeks=3)

    print(objetoEjemplar)
    objetoEjemplar.save()
    print(reserva)
    reserva.save()
    return redirect("adminReservas")


def renew_book_librarian(request, pk):
    """
    esta funcion es para que el bibliotecario renueve un libro , le cambia la fecha de devolucion 
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return  redirect("prestados")

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, "ampliacionFecha.html", {'form': form, 'bookinst':book_inst})


"""
Esta es funcion se encarga , de liberar los libros y ponerlos disponibles, y carga las reservas que tenian sobre este libro. 


"""
def  operacion(request, pk):
    objeto = get_object_or_404(BookInstance, pk=pk)

    if  "ampliar" in request.POST:
      
        return redirect("ampliarFecha", pk = objeto.id)


    elif "devolver" in request.POST: 
        # devolucion cambiamos el estado primero 

        objeto.status = "a"
        # vemos quien esta en la cola, de reservas 
        usuarios = Reservation.objects.filter(book_instance__pk = objeto.pk).order_by("fecha_reserva")
        primera_reserva = usuarios.first()
        if primera_reserva: 
            objeto.lector = primera_reserva.usuario_reservador
            objeto.status = "o"
            objeto.due_back = datetime.date.now() + datetime.timedelta(weeks=3)
            primera_reserva.estado = "Aprobada"
            primera_reserva.save()
        else: 
            objeto.lector = None
            objeto.status = "a"

        objeto.save() 
        return redirect("prestados")


def prestarEjemplar(request, pk):
    """
    esta funcion gestiona el prestamo fisico del ejemplar , si se lo lleva o se reserva o mantenimiento
    """
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
