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
from .serializers import CategoriaSerializer, ProductoSerializer

class Categorias(APIView):

    def get(self, request):
        consulta = Categoria.objects.all()
        serializer = CategoriaSerializer(consulta, many=True)
        return Response({"Categorias":serializer.data}, status=status.HTTP_200_OK)
 
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request ):
        console.log(request.query_params)
        
        if Categoria.objects.filter(id=request.query_params['id']).exists():
            item = Categoria.objects.get(id=request.query_params['id'])
            item.delete()
            return Response({"categoria" : "eliminada"}, status=status.HTTP_200_OK)   
        
        return Response({"error" : "no existe"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if 'id' not in request.query_params:
            return Response({"Error": "Debes proporcionar el ID de la categoria"}, status=status.HTTP_400_BAD_REQUEST)
        
        id_categoria = request.query_params['id']
        
        if not Categoria.objects.filter(id=id_categoria).exists():
            return Response({"Error": "La categoria no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        categoria = Categoria.objects.get(id=id_categoria)
        
        serializer = CategoriaSerializer(categoria, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Producticos(APIView):
   
    def get(self, request):
        console.log(request.query_params)
        categoria = request.query_params['id']

        try:
            categoria_obj = Categoria.objects.get(id=categoria)
        except Categoria.DoesNotExist:
            return Response({"Error": "La categoría no existe"}, status=status.HTTP_404_NOT_FOUND)

        productos = Productos.objects.filter(id_categoria_id=categoria_obj)
        categoria_serializer = CategoriaSerializer(categoria_obj)
        productos_serializer = ProductoSerializer(productos, many=True)

        return Response({
            "Categoria": categoria_serializer.data,
            "Productos": productos_serializer.data
        }, status=status.HTTP_200_OK)

    
    def post(self, request):
        console.log(request.data)
        
        serializer = ProductoSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    #ELIMINA EL PRODUCTO TENIENDO EN CUENTA SU ID 
    def delete(self, request ):
        console.log(request.query_params)
        
        if Productos.objects.filter(id=request.query_params['id']).exists():
            item = Productos.objects.get(id=request.query_params['id'])
            item.delete()
            return Response({"Producto" : "eliminada"}, status=status.HTTP_200_OK)   
        
        return Response({"error" : "no se puede eliminar el producto"}, status=status.HTTP_400_BAD_REQUEST)
    
    #EDITA EL PRODUCTO TENIENDO EN CUENTA SU ID EN EL ENDPOINT Y SU BODY
    def put(self, request):
        if 'id' not in request.query_params:
            return Response({"Error": "Debes proporcionar el ID del producto"}, status=status.HTTP_400_BAD_REQUEST)
        
        id_producto = request.query_params['id']
        
        if not Productos.objects.filter(id=id_producto).exists():
            return Response({"Error": "El producto no existe"}, status=status.HTTP_404_NOT_FOUND)
        
        producto = Productos.objects.get(id=id_producto)
        
        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ListarProductos(APIView):

    def get(self, request):
        consulta = Productos.objects.all()
        serializer = ProductoSerializer(consulta, many=True)
        return Response({"Productos":serializer.data}, status=status.HTTP_200_OK)
   