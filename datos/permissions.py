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
 
        