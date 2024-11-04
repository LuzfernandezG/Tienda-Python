from rest_framework import serializers
from .models import Venta, VentaItems

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = ['id', 'nombre', 'precio']

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