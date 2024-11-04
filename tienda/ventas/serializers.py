from rest_framework import serializers
from .models import Cliente, Venta, VentaItems
from productos.models import Productos
from productos.serializers import ProductoSerializer


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
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = VentaItems
        fields = ['id', 'producto', 'cantidad', 'precio_unitario', 'total']

class VentaSerializer(serializers.ModelSerializer):
    items = VentaItemSerializer(many=True, read_only=True)

    class Meta:
        model = Venta
        fields = ['id', 'id_cliente', 'metodo_de_pago', 'metodo_de_venta', 'total', 'estado', 'fecha', 'items']