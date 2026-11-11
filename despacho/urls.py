from django.urls import path
from . import views

app_name = 'despacho'

urlpatterns = [
    path('', views.lista_rutas, name='lista_rutas'),
    path('nueva/', views.nueva_ruta, name='nueva_ruta'),
    path('<int:pk>/', views.detalle_ruta, name='detalle_ruta'),
    path('<int:ruta_pk>/agregar/', views.agregar_entrega, name='agregar_entrega'),
    path('entrega/<int:pk>/confirmar/', views.confirmar_entrega, name='confirmar_entrega'),
]
