from rest_framework.permissions  import BasePermission
class TienesPermisoHola(BasePermission):
    def has_permissions(self, request, view):
        return request.user.has_perm("Catalog.usarHOla")



class TenesPermisoCalculadora(BasePermission):
    def has_permissions(self,request,view):
        return request.has_perm("Catalog.usarCalculadora")
        

class DenyAll(BasePermission):
    def has_permissions(self, request,view):
        return False
    
    