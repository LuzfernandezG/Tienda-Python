from django.contrib import admin

from .models import Categoria, Productos
# Register your models here.



@admin.register(Categoria)
class categoriasAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre"]
    
@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = [
        "id", 
        "nombre",
        "descripcion",
        "precio",
        "existencia",
        "id_categoria",
        "estado",
        "imagen",
    ]