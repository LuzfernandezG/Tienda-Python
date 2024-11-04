# serializers.py
from rest_framework import serializers
from .models import Categoria, Productos

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

    def validate_nombre(self, value):
        if Categoria.objects.filter(nombre=value).exists():
            raise serializers.ValidationError("La categoría ya existe")
        return value
    
    def validate_id(self, value):
        if not Categoria.objects.filter(id=value).exists():
            raise serializers.ValidationError("La categoría no existe")
        return value



class ProductoSerializer(serializers.ModelSerializer):
    id_categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())

    class Meta:
        model = Productos
        fields = [
            'id',
            'nombre',
            'descripcion',
            'precio',
            'existencia',
            'id_categoria',
            'estado',
            'imagen'
        ]

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return value

    def validate_existencia(self, value):
        if not isinstance(value, int) or value < 0:
            raise serializers.ValidationError("La existencia debe ser un número entero no negativo")
        return value

    def validate_nombre(self, value):
        if Productos.objects.filter(nombre=value).exists():
            raise serializers.ValidationError("Este producto ya existe")
        return value
    
    def validate_imagen(self, value):
        if not value.content_type.startswith('image/'):
            raise serializers.ValidationError("La imagen debe ser un archivo de imagen válido")
        return value