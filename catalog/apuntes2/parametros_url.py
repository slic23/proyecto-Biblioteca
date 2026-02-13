from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# =============================================================================
# 1. EN APIS (Django Rest Framework)
# Usamos request.query_params (Más limpio y recomendado en DRF)
# URL ejemplo: /api/libros/?titulo=Harry&autor=Rowling
# =============================================================================

@api_view(['GET'])
def buscar_libros_api(request):
    """
    Ejemplo de cómo obtener parámetros GET en una API.
    """
    # Método recomendado en DRF:
    titulo = request.query_params.get('titulo', None) # Devuelve None si no existe
    autor = request.query_params.get('autor', 'Desconocido') # Devuelve 'Desconocido' si no existe
    
    if titulo:
        return Response({"mensaje": f"Buscando libro: {titulo} de {autor}"})
    
    return Response({"mensaje": "No has enviado parámetros de búsqueda."})


# =============================================================================
# 2. EN VISTAS NORMALES (Django Clásico)
# Usamos request.GET.get() (Diccionario estándar de Python/Django)
# URL ejemplo: /catalog/buscar/?q=python
# =============================================================================

def buscar_libros_normal(request):
    """
    Ejemplo de cómo obtener parámetros GET en una vista normal (HTML).
    """
    # Diccionario request.GET estándar:
    query = request.GET.get('q', '') # Devuelve cadena vacía si no existe
    
    context = {
        'busqueda': query,
        'mensaje': f"Resultados para: {query}" if query else "Introduce un término."
    }
    
    return render(request, 'catalog/resultados.html', context)
