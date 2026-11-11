from django.urls import path
from . import views

app_name = 'cocina'

urlpatterns = [
    path('', views.kanban, name='kanban'),
    path('nueva/', views.nueva_tarea, name='nueva_tarea'),
    path('<int:pk>/avanzar/', views.avanzar_tarea, name='avanzar'),
    path('<int:pk>/', views.detalle_tarea, name='detalle_tarea'),
    path('<int:pk>/actualizar/', views.actualizar_tarea, name='actualizar_tarea'),
]
