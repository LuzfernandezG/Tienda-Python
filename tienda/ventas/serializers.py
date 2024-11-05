from rest_framework import serializers
from .models import Cliente, Venta, VentaItems
from productos.models import Productos
from productos.serializers import ProductoSerializer

from rich.console import Console
console = Console()


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre',
            'telefono',
            'cedula',
            'correo'
        ]

    def validate_cedula(self, value):
        if Cliente.objects.filter(cedula=value).exists():
            raise serializers.ValidationError("El cliente ya existe")
        return value
    
class VentaItemSerializer(serializers.ModelSerializer):
    # producto = ProductoSerializer(read_only=True)

    class Meta:
        model = VentaItems
        fields = [
            'id_producto',
            'cantidad',
            'total',
            # 'id_venta',
        ]

class VentaSerializer(serializers.ModelSerializer):
    # items = VentaItemSerializer(many=True, read_only=True)
    items = VentaItemSerializer(many=True,)

    class Meta:
        model = Venta
        fields = [
            'id_cliente',
            'metodo_de_pago',
            'metodo_de_venta',
            'total',
            'estado',
            'fecha',
            'items',
        ]
            
    
    # Sobrescribir el método create para manejar la creación de items
    def create(self, validated_data):

        console.log(validated_data)
        ventas_data = validated_data.pop('items')  # Remover detalles
        console.log(ventas_data)
        console.log(validated_data)
        
        total = 0
        venta = Venta.objects.create(**validated_data)  # Crear el pedido
        for item_data in ventas_data:
            # ImpresionTicketsItems.objects.create(id=pedido, **item_data)  # Crear cada detalle
            VentaItems.objects.create(id_venta=venta, **item_data)  # Crear cada detalle
            total += item_data["total"] * item_data["cantidad"]
        console.log(total)
            
        # Venta.objects.update(total=total)
        Venta.objects.filter(id=venta.id).update(total=total)
        # console.log(vars(venta))
        
        return venta
        
        
# class DetallePedidoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ImpresionTicketsItems
#         fields = [
#             'codigo', 
#             'referencia',
#             'cantidad_unidades',
#             'cantidad_stickers',
#             'barcode',
#             'unidad_de_medida',
#         ]


# class PedidoSerializer(serializers.ModelSerializer):
#     # Anidar el serializer de DetallePedido
#     Venta = DetallePedidoSerializer(many=True,)  # many=True para múltiples items

#     class Meta:
#         model = ImpresionTickets
#         fields = [
#             'ordenDeCompra',
#             'comentario',
#             'items',
#             'company',
#             'id',
#             'fechaCreacion',
#             'ususarioCreador',
#         ]

#         extra_kwargs = {
#             'items': {'required': False},
#             'id': {'required': False},
#             'fechaCreacion': {'required': False},
#         }

    