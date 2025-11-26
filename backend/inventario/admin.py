from django.contrib import admin
from .models import Equipo

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'modelo', 'fecha_adquisicion')
    search_fields = ('nombre', 'marca', 'modelo')
