from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

urlpatterns = [
    # Renders
    path('', views.Categorias.as_view(), name="Categorias"),
    path('inventario/', views.Producticos.as_view(), name="Producticos"),

    
    # path('manual/', views.manual, name="manual"),
     
]
