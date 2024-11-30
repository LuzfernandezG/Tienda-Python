from django.urls import path
from django.urls.resolvers import URLPattern


from . import views

urlpatterns = [
    # Renders
    path('', views.Clientes.as_view() , name="Clientes"),
    path('registro/', views.Ventas.as_view(), name="Registro"),
    path('administrar/', views.ManejoVentas.as_view(), name="Registro"),
  
    
]
