from django.contrib import admin

# Register your models here.
from .models import Cliente, Venta, VentaItems
# Register your models here.

@admin.register(Cliente)
class categoriasAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "nombre",
        "telefono",
        "cedula",
        "correo",
    ]
    
@admin.register(Venta)
class ProductosAdmin(admin.ModelAdmin):
    list_display = [
        "cliente",
        "metodo_de_pago",
        "metodo_de_venta",
        "total",
        "estado",
        "fecha",
    ]

    def cliente(self, obj):
            return obj.id_cliente.nombre 

@admin.register(VentaItems)
class ProductosAdmin(admin.ModelAdmin):
    list_display = [
        "producto",
        "cantidad",
        "total",
        "venta",
    ]
    
    def producto(self, obj):
        return obj.id_producto.nombre 
    
    def venta(self, obj):
        return obj.id_venta.id