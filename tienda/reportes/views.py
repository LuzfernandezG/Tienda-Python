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
            cursor.execute("SELECT * FROM ventas_venta")
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            # result = list(cursor.fetchall())

        # queryset = QuerySet(model=passTable, using='default')
        # queryset._result_cache = list(result)
            
            
        console.log(results)
        
        # for p in Venta.objects.raw("SELECT * FROM ventas_venta"):
        #  print(p)
         
        # for data in p:
        #  print(data)
         
        return Response({"hola":"ok"})



