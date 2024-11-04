from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    nombre = models.CharField(max_length=50)
 

class Productos(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="id")
    nombre = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=100,null=True, blank=True)
    precio = models.FloatField(max_length=10, null=True, blank=True) 
    existencia = models.IntegerField(max_length=10, null=True, blank=True)
    id_categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name="categoria", related_name='categoria')
    estado = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    



