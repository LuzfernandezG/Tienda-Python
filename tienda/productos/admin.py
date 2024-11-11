from django.contrib import admin
from .models import Categoria, Productos
from django.contrib import messages
from ventas.models import VentaItems,Venta

@admin.register(Categoria)
class categoriasAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre"]
    actions = ['delete_selected']
    list_editable = ["nombre"]

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "nombre",
        "descripcion",
        "precio",
        "existencia",
        "categoria",  # Cambiamos `id_categoria` por `categoria`
        "estado",
        "imagen",
    ]
    # actions = ['delete_selected']
    # list_editable = ["nombre,descripcion,estado,imagen,precio"]
    
    # Método personalizado para mostrar el nombre de la categoría
    def categoria(self, obj):
        return obj.id_categoria.nombre 
    # Mostramos el nombre de la categoría
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "id_categoria":
            kwargs["queryset"] = Categoria.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def delete_queryset(self, request, queryset):
        # Verifica si algún producto tiene ventas relacionadas
        productos_con_ventas = []
        for producto in queryset:
            if VentaItems.objects.filter(id_producto=producto).exists():
                productos_con_ventas.append(producto)

        # Si hay productos con ventas, muestra un mensaje de advertencia
        if productos_con_ventas:
            nombres_productos = ", ".join([str(p) for p in productos_con_ventas])
            self.message_user(
                request,
                f"No se pueden eliminar los siguientes productos porque tienen ventas relacionadas: {nombres_productos}",
                messages.ERROR
            )
        else:
            # Elimina los productos si no tienen ventas relacionadas
            super().delete_queryset(request, queryset)
    
    

    categoria.short_description = "Categoría"  # Nombre de la columna en el administrador
