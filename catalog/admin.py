from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
# Register your models here.
#admin.site.register(Book)
#admin.site.register(BookInstance)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
@admin.register(Author)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","date_of_birth","date_of_death")


class BookInstanceInline(admin.TabularInline):
    model = BookInstance




@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title","author","display_genre")
    inlines = [BookInstanceInline]
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book","status","due_back")
    list_filter  = ("status","due_back")
    fieldsets = (
            (None, {"fields":("book","imprent","id")}),
            ("Availability",{"fields":("status","due_back")}),
                )

admin.site.register(Permission)
