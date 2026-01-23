from rest_framework.permissions  import BasePermission
class TienesPermisoHola(BasePermission):
    def has_permissions(self, request, view):
        return request.user.has_perm("Catalog.usarHOla")


class DenyAll(BasePermission):
    def has_permissions(self, request,view):
        return False
    
    