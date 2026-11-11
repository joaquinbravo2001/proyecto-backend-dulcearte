from django.db import models
from django.utils import timezone
from pedidos.models import Pedido

class TareaKanban(models.Model):
    ESTADO_CHOICES = [
        ('recibido', 'Recibido'),
        ('en_preparacion', 'En Preparación'),
        ('horneado_decorado', 'Horneado/Decorado'),
        ('control_calidad', 'Control de Calidad'),
        ('listo', 'Listo'),
    ]
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='tarea_cocina')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='recibido')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='normal')
    responsable = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='tareas_cocina')
    notas_cocina = models.TextField(blank=True)
    fecha_inicio_real = models.DateTimeField(null=True, blank=True)
    fecha_fin_real = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tarea de Cocina'
        verbose_name_plural = 'Tareas de Cocina'
        ordering = ['prioridad', 'pedido__fecha_entrega']
    
    def __str__(self):
        return f"Cocina: {self.pedido.numero} [{self.get_estado_display()}]"
    
    def avanzar_estado(self):
        estados = ['recibido', 'en_preparacion', 'horneado_decorado', 'control_calidad', 'listo']
        idx = estados.index(self.estado)
        if idx < len(estados) - 1:
            if self.estado == 'recibido':
                self.fecha_inicio_real = timezone.now()
            if idx + 1 == len(estados) - 1:
                self.fecha_fin_real = timezone.now()
            self.estado = estados[idx + 1]
            self.save()
            # Sincronizar con pedido
            if self.estado == 'listo':
                self.pedido.estado = 'listo'
                self.pedido.save()
            return True
        return False

class HistorialKanban(models.Model):
    tarea = models.ForeignKey(TareaKanban, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    notas = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Historial Kanban'
        verbose_name_plural = 'Historial Kanban'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.tarea.pedido.numero}: {self.estado_anterior} → {self.estado_nuevo}"
