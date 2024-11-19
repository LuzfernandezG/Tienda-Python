from django.shortcuts import render
from django.http import HttpResponse,response,JsonResponse
from django.db.models import Sum
from django.db import models

from django.db.models.expressions import RawSQL
from django.views.decorators.http import require_http_methods
from rich.console import Console
from django.db.models import Q, Max, QuerySet

console = Console()
from ventas.models import Venta

# Django Rest Framework

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from django.db import connection

class passTable(models.Model):
    pass

class Reporte(APIView):
    def get(self, request):
        
        with connection.cursor() as cursor:
            cursor.execute('''
      SELECT 
        'Más vendido' AS tipo, 
        nombre, 
        cantidad_total
      FROM (
        SELECT 
          p.nombre, 
          SUM(v.cantidad) AS cantidad_total
        FROM 
          ventas_ventaitems v
          INNER JOIN tienda.productos_productos p ON v.id_producto_id = p.id
        GROUP BY 
          v.id_producto_id, p.nombre
        ORDER BY 
          cantidad_total DESC
        LIMIT 3
      ) AS max_vendido

      UNION ALL

      SELECT 
        'Menos vendido' AS tipo, 
        nombre, 
        cantidad_total
      FROM (
        SELECT 
          p.nombre, 
          SUM(v.cantidad) AS cantidad_total
        FROM 
          ventas_ventaitems v
          INNER JOIN tienda.productos_productos p ON v.id_producto_id = p.id
        GROUP BY 
          v.id_producto_id, p.nombre
        ORDER BY 
          cantidad_total ASC
        LIMIT 1
      ) AS min_vendido

      UNION ALL

      SELECT 
        'Mejores_clientes' AS tipo, 
        nombre, 
        cantidad_ventas
      FROM (
        SELECT 
          p.nombre, 
          COUNT(v.id_cliente_id) AS cantidad_ventas
        FROM 
          ventas_venta v
          INNER JOIN tienda.ventas_cliente p ON v.id_cliente_id = p.id
        GROUP BY 
          p.nombre
        ORDER BY 
          cantidad_ventas DESC
        LIMIT 3
      ) AS subconsulta

      UNION ALL

      SELECT 
        'Mejores_categorias' AS tipo, 
        nombre, 
        cantidad_total
      FROM (
        SELECT 
          pc.nombre AS nombre, 
          COUNT(vvi.id_producto_id) AS cantidad_total
        FROM 
          ventas_ventaitems vvi
          INNER JOIN productos_productos pp ON vvi.id_producto_id = pp.id
          INNER JOIN productos_categoria pc ON pp.id_categoria_id = pc.id
        GROUP BY 
          pc.nombre
        LIMIT 3
      ) AS subcategoria
      ORDER BY tipo;


      ''')
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            # result = list(cursor.fetchall())

        # queryset = QuerySet(model=passTable, using='default')
        # queryset._result_cache = list(result)
            
        console.log(results)
        return Response(results,status=status.HTTP_200_OK)
      
    def post(self, request):
      console.log(request.data)
      tipo = request.data['tipo']
      fecha = request.data['fecha']

      with connection.cursor() as cursor:
          if tipo == 'week':
              query = '''
                  SELECT * FROM ventas_venta
                  WHERE WEEK(fecha) = WEEK(%s)
              '''
          elif tipo == 'month':
              query = '''
                  SELECT * FROM ventas_venta
                  WHERE MONTH(fecha) = MONTH(%s)
              '''
          elif tipo == 'day':
              query = '''
                 select * from tienda.ventas_venta
                where fecha = (%s);
                 
              '''
          else:
              return Response({"mensaje": "Tipo no válido"}, status=status.HTTP_400_BAD_REQUEST)

          cursor.execute(query, [fecha])

          if cursor.rowcount > 0:
              columns = [col[0] for col in cursor.description]
              results = [dict(zip(columns, row)) for row in cursor.fetchall()]
              console.log(results)
              return Response(results, status=status.HTTP_200_OK)
          else:
              return Response({"mensaje": "No se encontraron resultados"}, status=status.HTTP_200_OK)

         
      
      
      
        
      
      



