#AQUI SE INCLUYEN LAS URLS DE LA APLICACIONES QUE SE CREAN-CONOCIDOS COMO MICROSERVICIOS
#DEBE IMPORTANSE AQUI T EN SETTINGS TAMBIEN SE DEBEN INCLUIR LA APLICACIONES PARA QUE EL ARCHIVO RAIZ PUEDA DIRECCIONARLOS
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from tienda import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', include('productos.urls')),
    path('ventas/', include('ventas.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATICFILES_DIRS}), 
