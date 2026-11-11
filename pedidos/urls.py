from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('', views.lista_pedidos, name='lista'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('nuevo/', views.nuevo_pedido, name='nuevo'),
    path('<int:pk>/', views.detalle_pedido, name='detalle'),
    path('<int:pk>/editar/', views.editar_pedido, name='editar'),
    path('<int:pk>/descontar-inventario/', views.descontar_inventario, name='descontar_inventario'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/nuevo/', views.nuevo_cliente, name='nuevo_cliente'),
]
