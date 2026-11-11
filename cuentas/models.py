from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('cocinero', 'Cocinero'),
        ('bodeguero', 'Bodeguero'),
        ('repartidor', 'Repartidor'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=15, choices=ROL_CHOICES, default='vendedor')
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()}"
