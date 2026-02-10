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