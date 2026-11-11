from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.lista_inventario, name='lista'),
    path('nuevo/', views.nuevo_insumo, name='nuevo_insumo'),
    path('<int:pk>/editar/', views.editar_insumo, name='editar_insumo'),
    path('ajuste/', views.ajuste_stock, name='ajuste_stock'),
    path('<int:pk>/historial/', views.historial_insumo, name='historial_insumo'),
]
