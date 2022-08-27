from django.contrib import admin

# Register your models here.
from .models import Libro

class LibroAdmin (admin.ModelAdmin):
    readonly_fields= ('created-at', 'updated-at')

admin.site.register(Libro)

