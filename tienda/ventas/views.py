from django.shortcuts import render
from django.http import HttpResponse,response,JsonResponse
from django.db.models import Sum
from rich.console import Console
console = Console()

from .models import (
    Cliente,
    Venta,
    VentaItems
)
from productos.models import Productos
# Django Rest Framework
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated

from .serializers import ClienteSerializer, VentaSerializer


class Clientes(APIView):

    def get(self, request ):
        listado_clientes = Cliente.objects.all()
        serializer = ClienteSerializer(listado_clientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request ):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
class Ventas(APIView):

    def get(self, request):
        cedula_cliente = request.query_params.get('cc')
        
        # Filtrar cliente por cédula
        consulta = Cliente.objects.filter(cedula=cedula_cliente).values()
        print(consulta)  # Usa print para depurar

        if consulta.exists():
            cliente_data = consulta.first()
            # Filtrar ventas relacionadas al cliente
            consulta2 = Venta.objects.filter(id_cliente_id=cliente_data['id']).values()
            print(consulta2)  # Debug output

            if consulta2.exists():
                # Verificar si hay deudas (metodo_de_pago == 3)
                pendientes = Venta.objects.filter(id_cliente_id=cliente_data['id'], metodo_de_pago=3).values()
                print("Deudas:", list(pendientes))  # Obtén la lista de deudas
                pendientes_total = pendientes.aggregate(total_sum=Sum('total'))
                total_general = pendientes_total['total_sum'] or 0  # Maneja el caso de None

               
                # if pendientes.total >= ['cantidad']:
                #     producto.existencia -= item['cantidad']  # Resta la cantidad vendida
                #     producto.save()  # Guarda los cambios
                # else:
                #     return Response({"error": "No hay suficiente existencia para el producto con id {}".format(item["id_producto"])}, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                    "Cliente": cliente_data,
                    "Deudas": list(pendientes),
                    "Total deuda":total_general  # Incluye deudas en la respuesta
                }, status=status.HTTP_200_OK)

        return Response({"error": "Cliente sin ventas"}, status=status.HTTP_404_NOT_FOUND)
           
    def post(self, request ):
        
        console.log(request.data)
        # console.log(usuario)

        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():

            # console.log(serializer.data)
            console.log("Si SAlio SO")
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        # return Response({"response" : "creado"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # console.log(request.data)
        # data = request.data['venta']
        
        # creacion_cliente = Venta (
        #         metodo_de_pago=data['metodo_de_pago'],
        #         metodo_de_venta=data['metodo_de_venta'],
        #         total=data['total_venta'],
        #         estado=data['estado'],
        #         id_cliente_id=data['id_cliente']
        #     )  
        # creacion_cliente.save()
        
        # for item in request.data['items']:
        #         VentaItems.objects.create(
        #             cantidad=item['cantidad'],
        #             total=item['total'],
        #             id_producto_id=item['id_producto'],
        #             id_venta_id= creacion_cliente.id
        #         )
        #         producto = Productos.objects.get(id=item["id_producto"]) 
               
        #         if producto.existencia >= item['cantidad']:
        #             producto.existencia -= item['cantidad']  # Resta la cantidad vendida
        #             producto.save()  # Guarda los cambios
        #         else:
        #             return Response({"error": "No hay suficiente existencia para el producto con id {}".format(item["id_producto"])}, status=status.HTTP_400_BAD_REQUEST)
                
          

        # return Response({"recibido" : "ok"}, status=status.HTTP_200_OK)


    
    # def delete(self, request ):
       
        
    #     return Response({"error" : "no se puede eliminar la categoria"}, status=status.HTTP_400_BAD_REQUEST
