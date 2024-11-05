from django.contrib import admin

# Register your models here.
from .models import Cliente, Venta, VentaItems
# Register your models here.

@admin.register(Cliente)
class categoriasAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "telefono",
        "cedula",
        "correo",
    ]
    
@admin.register(Venta)
class ProductosAdmin(admin.ModelAdmin):
    list_display = [
        "id_cliente",
        "metodo_de_pago",
        "metodo_de_venta",
        "total",
        "estado",
        "fecha",
    ]


@admin.register(VentaItems)
class ProductosAdmin(admin.ModelAdmin):
    list_display = [
        "id_producto",
        "cantidad",
        "total",
        "id_venta",
    ]