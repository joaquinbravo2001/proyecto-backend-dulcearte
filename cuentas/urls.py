from django.urls import path
from . import views

app_name = 'cuentas'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
]
