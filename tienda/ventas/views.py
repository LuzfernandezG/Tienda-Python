from django.shortcuts import render
from django.http import HttpResponse,response,JsonResponse
from django.db.models import Sum
from rich.console import Console
console = Console()

from .models import (
    Cliente,
    Venta,
    VentaItems,
    AbonosCuentas
    
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

from .serializers import ClienteSerializer, VentaSerializer,AbonoSerializer


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
        consulta = Cliente.objects.filter(cedula=cedula_cliente).values()
        print(consulta) 

        if consulta.exists():
            cliente_data = consulta.first()
       
            consulta2 = Venta.objects.filter(id_cliente_id=cliente_data['id']).values()
            print(consulta2)  

            if consulta2.exists():
                
                pendientes = Venta.objects.filter(id_cliente_id=cliente_data['id'], metodo_de_pago=3).values()
                console.log(pendientes)
                if not pendientes.exists():
                    return Response({"error": "Cliente sin deudas"}, status=status.HTTP_200_OK)
        
                pendientes_total = pendientes.aggregate(total_sum=Sum('total'))
                total_general = pendientes_total['total_sum'] or 0  
                
                Abonos = AbonosCuentas.objects.filter(cedula_cliente_id=cedula_cliente).values()
                total_abonos = Abonos.aggregate(total_sum=Sum('valor'))
                total = total_abonos['total_sum'] or 0

                return Response({
                    "Cliente": cliente_data,
                    "Deudas": list(pendientes),
                    "Total deuda":total_general ,
                    "Total_abono":total
                }, status=status.HTTP_200_OK)

        return Response({"error": "Cliente sin ventas"}, status=status.HTTP_404_NOT_FOUND)
           
    def post(self, request ):
        
        console.log(request.data)

        serializer = VentaSerializer(data=request.data)
        if serializer.is_valid():
            console.log("Si SAlio SO")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        console.log(request.data)
        
        id=request.data['id']
        estado=request.data['estado']
        Venta.objects.filter(id=id).update(estado=estado)
        
        return Response({"peticion de edicion":"ok"}, status=status.HTTP_200_OK)
    

     
class ManejoVentas(APIView):

    def get(self, request):
        ventas = Venta.objects.all()
        serializer = VentaSerializer(ventas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request ):
        console.log(request.data)
        serializer = AbonoSerializer(data=request.data)
        if serializer.is_valid():
            console.log("abono agregado")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        console.log(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request):
        data = request.query_params
        id=data['id']
        cedula=data['cedula']
        console.log(id)
        console.log(data)
        console.log(cedula)
        abonos = AbonosCuentas.objects.filter(cedula_cliente_id=cedula)
        console.log(abonos)
       
        pendientes = Venta.objects.filter(id_cliente_id=id, metodo_de_pago=3)
        console.log("ventas del cliente",pendientes)
        if abonos:
            abonos.delete()

            return Response({"mensaje": "Abono eliminado con éxito y deuda "}, status=status.HTTP_200_OK)
        else:
            pendientes.update(metodo_de_pago=1)
            return Response({"mensaje": "deuda eliminada"}, status=status.HTTP_200_OK)
        
        return Response({"mensaje": "Abono no encontrado"}, status=status.HTTP_400_BAD_REQUEST)
    
    





        
    
        
     
         