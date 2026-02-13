from rest_framework.permissions  import BasePermission
class TienesPermisoHola(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("Catalog.usarHOla")



class TenesPermisoCalculadora(BasePermission):
    def has_permission(self,request,view):
        return request.user.has_perm("Catalog.usarCalculadora")
        

class DenyAll(BasePermission):
    def has_permission(self, request,view):
        return False
    
    


class EsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False
    

from datetime import datetime, date

class EsAdulto(BasePermission):
    def has_permission(self, request, view):
        dato = request.data.get("fecha_nacimiento")
        if not dato:
            return False

        datos = dato.split("-")
        fecha_actual = date.today()
        anio = int(datos[0])
        mes  = int(datos[1])
        dia  = int(datos[2])
        fecha_nac = date(anio, mes, dia)

        
        edad = fecha_actual.year - fecha_nac.year

        
        if (fecha_actual.month, fecha_actual.day) < (fecha_nac.month, fecha_nac.day):
            edad = edad - 1
            

        return edad > 18
 
        


"""
# permissions_examples.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

# 1️⃣ Permiso que permite TODO a cualquier usuario
class AllowAllPermission(BasePermission):
    def has_permission(self, request, view):
        # Devuelve True siempre
        return True


# 2️⃣ Permiso que deniega TODO a cualquier usuario
class DenyAllPermission(BasePermission):
    def has_permission(self, request, view):
        # Devuelve False siempre
        return False


# 3️⃣ Solo usuarios autenticados pueden acceder
class IsAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        # request.user.is_authenticated es True para usuarios autenticados
        return request.user and request.user.is_authenticated


# 4️⃣ Solo admins (is_staff) pueden acceder
class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        # request.user.is_staff True si es admin
        return request.user and request.user.is_staff


# 5️⃣ Permite GET a cualquiera, otras acciones solo a autenticados
class ReadOnlyOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_authenticated


# 6️⃣ Solo permite POST
class OnlyPostPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'


# 7️⃣ Solo permite PUT/PATCH (actualización)
class OnlyUpdatePermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['PUT', 'PATCH']


# 8️⃣ Permite todo excepto DELETE
class NoDeletePermission(BasePermission):
    def has_permission(self, request, view):
        return request.method != 'DELETE'


# 9️⃣ Permite solo si el usuario tiene un atributo personalizado
class HasPremiumPermission(BasePermission):
    def has_permission(self, request, view):
        # Supongamos que tu User tiene .is_premium
        return hasattr(request.user, 'is_premium') and request.user.is_premium

"""