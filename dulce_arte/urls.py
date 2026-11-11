from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
import dulce_arte.admin_config  # Configurar títulos de admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('pedidos:dashboard'), name='home'),
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),
    path('inventario/', include('inventario.urls', namespace='inventario')),
    path('cocina/', include('cocina.urls', namespace='cocina')),
    path('despacho/', include('despacho.urls', namespace='despacho')),
    path('cuentas/', include('cuentas.urls', namespace='cuentas')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
