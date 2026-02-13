from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from catalog.models import Book # O el modelo que sea

def ejemplos_gestion_permisos():
    """
    Ejemplo de cómo buscar permisos y asignarlos a usuarios o grupos.
    """

    # 1. BUSCAR UN PERMISO ESPECÍFICO
    # Los permisos tienen un 'codename' (ej: 'add_book') y un 'content_type' (modelo asociado).
    # Formato codename standard: add_modelo, change_modelo, delete_modelo, view_modelo
    
    try:
        # Opción A: Buscar por codename directamente (si es único o sabes que es standard)
        # Ojo: Si hay varios apps con el mismo modelo, codename puede repetirse, mejor la opción B.
        permiso = Permission.objects.get(codename='add_book') 
        
        # Opción B: Buscar de forma segura usando el ContentType del modelo
        content_type = ContentType.objects.get_for_model(Book)
        permiso_seguro = Permission.objects.get(
            codename='add_book',
            content_type=content_type
        )
        
        print(f"Permiso encontrado: {permiso_seguro.name}")

    except Permission.DoesNotExist:
        print("El permiso no existe.")
        return


    # 2. ASIGNAR PERMISO A UN USUARIO (obj.user_permissions.add())
    try:
        user = User.objects.get(username='issam')
        
        # Añadir el permiso
        user.user_permissions.add(permiso_seguro)
        
        # Guardar (aunque .add() suele guardar la relación many-to-many al instante)
        user.save() 
        print(f"Permiso añadido al usuario {user.username}")

        # Comprobar si lo tiene
        if user.has_perm('catalog.add_book'): # app_label.codename
            print("Sí, tiene el permiso.")

    except User.DoesNotExist:
        print("Usuario no encontrado.")


    # 3. ASIGNAR PERMISO A UN GRUPO (obj.permissions.add())
    # Crear o obtener grupo
    grupo, created = Group.objects.get_or_create(name='Bibliotecarios')
    
    # Añadir permiso al grupo
    grupo.permissions.add(permiso_seguro)
    print(f"Permiso añadido al grupo {grupo.name}")
    
    
    # 4. CREAR UN PERMISO PERSONALIZADO (Manual)
    # A veces quieres un permiso que no sea los 4 por defecto (add, change, delete, view)
    content_type_book = ContentType.objects.get_for_model(Book)
    
    permiso_custom, created = Permission.objects.get_or_create(
        codename='puede_publicar_libros',
        name='Puede publicar libros en la web',
        content_type=content_type_book,
    )
    
    # Se asigna igual
    user.user_permissions.add(permiso_custom)
