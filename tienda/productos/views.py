from django.shortcuts import render
from django.http import HttpResponse,response,JsonResponse
from rich.console import Console
console = Console()

from .models import (
    Categoria,
    Productos
)
# Django Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated

class Categorias(APIView):
    def get(self, request ):
        consulta=Categoria.objects.all().values()
        console.log(consulta)
        return Response({"Categorias":consulta}, status=status.HTTP_200_OK)
    
    def post(self, request ):
        console.log(request.data)
        
        if Categoria.objects.filter(nombre=request.data['nombre']).exists():
            return Response({"categoria" : "existente"}, status=status.HTTP_400_BAD_REQUEST)   
        categoria_ingresada=Categoria(
             nombre=request.data['nombre'],
        )
        categoria_ingresada.save()
        return Response({"recibido" : "ok"}, status=status.HTTP_200_OK)
    
    def delete(self, request ):
        console.log(request.query_params)
        
        if Categoria.objects.filter(id=request.query_params['id']).exists():
            item = Categoria.objects.get(id=request.query_params['id'])
            item.delete()
            return Response({"categoria" : "eliminada"}, status=status.HTTP_200_OK)   
        
        return Response({"error" : "no se puede eliminar la categoria"}, status=status.HTTP_400_BAD_REQUEST)



class Producticos(APIView):
    def get(self, request ):
        console.log(request.query_params)
        categoria=request.query_params['id']
        
        if Categoria.objects.filter(id=request.query_params['id']).exists():
            productos_existentes=Productos.objects.filter(id_categoria_id=categoria).values()
            consulta=Categoria.objects.filter(id=categoria).values()
            return Response({"Categoria":consulta,"Los productos que coinciden con la categoria seleccionada":productos_existentes}, status=status.HTTP_200_OK)
        return Response({"Error":"El valor a buscar no tiene informacion coincidente"}, status=status.HTTP_400_BAD_REQUEST)
      
    def post(self, request ):
        console.log(request.data)
        creacion_producto = Productos(
            nombre=request.data['nombre'],
            descripcion=request.data['descripcion'],
            precio=request.data['precio'],
            existencia=request.data['existencia'],
            id_categoria_id=request.data['id_categoria']
        )  
        console.log(creacion_producto)
        creacion_producto.save()
        return Response({"Producto Agregado" : "ok"}, status=status.HTTP_200_OK)
    
    def delete(self, request ):
        console.log(request.query_params)
        
        if Productos.objects.filter(id=request.query_params['id']).exists():
            item = Productos.objects.get(id=request.query_params['id'])
            item.delete()
            return Response({"Producto" : "eliminada"}, status=status.HTTP_200_OK)   
        
        return Response({"error" : "no se puede eliminar el producto"}, status=status.HTTP_400_BAD_REQUEST)
    
