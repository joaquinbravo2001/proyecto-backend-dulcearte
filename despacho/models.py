from django.db import models
from django.utils import timezone
from pedidos.models import Pedido

class RutaDespacho(models.Model):
    ESTADO_CHOICES = [
        ('planificada', 'Planificada'),
        ('en_ruta', 'En Ruta'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    nombre = models.CharField(max_length=200)
    fecha_despacho = models.DateField()
    repartidor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='rutas_despacho')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='planificada')
    notas = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Ruta de Despacho'
        verbose_name_plural = 'Rutas de Despacho'
        ordering = ['-fecha_despacho']
    
    def __str__(self):
        return f"{self.nombre} - {self.fecha_despacho}"

class EntregaPedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado'),
        ('fallido', 'Intento Fallido'),
    ]
    ruta = models.ForeignKey(RutaDespacho, on_delete=models.PROTECT, related_name='entregas')
    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT, related_name='entrega')
    orden_entrega = models.PositiveIntegerField(default=1)
    direccion_entrega = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    hora_entrega_real = models.DateTimeField(null=True, blank=True)
    firma_digital = models.ImageField(upload_to='firmas/', null=True, blank=True, help_text="Firma del receptor")
    comprobante_foto = models.ImageField(upload_to='comprobantes/', null=True, blank=True, help_text="Foto del comprobante")
    receptor_nombre = models.CharField(max_length=200, blank=True, help_text="Nombre de quien recibe")
    notas_entrega = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Entrega de Pedido'
        verbose_name_plural = 'Entregas de Pedidos'
        ordering = ['ruta', 'orden_entrega']
    
    def __str__(self):
        return f"Entrega {self.pedido.numero} - {self.get_estado_display()}"
    
    def confirmar_entrega(self, firma=None, foto=None, receptor=''):
        self.estado = 'entregado'
        self.hora_entrega_real = timezone.now()
        if firma:
            self.firma_digital = firma
        if foto:
            self.comprobante_foto = foto
        if receptor:
            self.receptor_nombre = receptor
        self.save()
        # Actualizar estado del pedido
        self.pedido.estado = 'entregado'
        self.pedido.save()
