from django.urls import path
from django.urls.resolvers import URLPattern


from . import views

urlpatterns = [
    # Renders
    path('', views.Reporte.as_view() , name="Reportes"),   
]
