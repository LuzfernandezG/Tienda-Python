from django.shortcuts import render
from django.http import HttpResponse,response,JsonResponse
from rich.console import Console
console = Console()

from .models import (
    Cliente,
    Venta,
    VentaItems
)
# Django Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated


class Clientes(APIView):
    
    def get(self, request ):
        listado_clientes=Cliente.objects.all().values()
        return Response({"clientes":listado_clientes}, status=status.HTTP_200_OK)
    
    def post(self, request ):
        console.log(request.data)
        if Cliente.objects.filter(cedula=request.data['cedula'] ).exists():
           return Response({"Este cliente ya existe"}, status=status.HTTP_400_BAD_REQUEST)
        creacion_cliente = Cliente (
                nombre=request.data['nombre'],
                telefono=request.data['telefono'],
                cedula=request.data['cedula'],
                correo=request.data['correo'],
            )  
        console.log(creacion_cliente)
        creacion_cliente.save()
        return Response({"Cliente agregado":"ok"}, status=status.HTTP_200_OK)

  
class Ventas(APIView):
    def get(self, request ):
        console.log(request.query_params)
        consulta=Venta.objects.filter(cod_Venta=request.query_params['cod']).values()
        items_venta=VentaItems.objects.filter(id_producto_id=consulta.id).values()
     
        return Response({"venta":consulta,"productos":items_venta}, status=status.HTTP_200_OK)
      
    def post(self, request ):
        # console.log(request.data)
        data = request.data['venta']
        creacion_cliente = Venta (
                metodo_de_pago=data['metodoPago'],
                metodo_de_venta=data['metodoVenta'],
                total=data['total_venta'],
                estado=data['estado'],
                id_cliente_id=data['id_cliente'],
                cod_Venta=data['codVenta']
            )  
        creacion_cliente.save()
        
        for item in data['items']:
                VentaItems.objects.create(
                    cantidad=item['cantidad'],
                    total=item['total'],
                    id_producto_id=item['id_producto'],
                    codigo_venta_id= creacion_cliente.id
                )
        return Response({"recibido" : "ok"}, status=status.HTTP_200_OK)
    
    def delete(self, request ):
       
        
        return Response({"error" : "no se puede eliminar la categoria"}, status=status.HTTP_400_BAD_REQUEST)


