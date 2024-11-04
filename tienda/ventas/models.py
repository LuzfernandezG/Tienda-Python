from django.db import models
from django.contrib.auth.models import User
from productos.models import Productos

class Cliente(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    cedula = models.CharField(max_length=10, null=True, blank=True)
    correo = models.CharField(max_length=100, null=True, blank=True)
    
class Venta(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    id_cliente = models.ForeignKey(Cliente, on_delete=models.DO_NOTHING, verbose_name="cliente", related_name='cliente')
    metodo_de_pago = models.IntegerField( null=True, blank=True)
    metodo_de_venta = models.IntegerField(max_length=10, null=True, blank=True) 
    total = models.FloatField(max_length=10, null=True, blank=True) 
    estado = models.IntegerField(max_length=10, null=True, blank=True) 
    fecha = models.DateField(auto_now_add=True)
    cod_Venta = models.CharField(max_length=10, null=True, blank=True)
    
    
class VentaItems(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    id_producto = models.ForeignKey(Productos, on_delete=models.DO_NOTHING, verbose_name="cliente", related_name='cliente')
    cantidad = models.IntegerField(max_length=10, null=True, blank=True)
    total = models.IntegerField(max_length=10, null=True, blank=True)
    codigo_venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING, verbose_name="Venta", related_name='Venta')
