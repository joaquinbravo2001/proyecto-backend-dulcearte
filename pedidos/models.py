from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from inventario.models import Insumo

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.telefono}"

class ProductoBase(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    tiempo_preparacion_horas = models.PositiveIntegerField(default=4, help_text="Tiempo estimado en horas")
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Producto Base'
        verbose_name_plural = 'Productos Base'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class BOM(models.Model):
    """Bill of Materials - Lista de Materiales por producto"""
    producto = models.ForeignKey(ProductoBase, on_delete=models.CASCADE, related_name='bom_items')
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, related_name='bom_items')
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(Decimal('0.001'))])
    notas = models.CharField(max_length=200, blank=True)
    
    class Meta:
        verbose_name = 'BOM - Item de Materiales'
        verbose_name_plural = 'BOM - Items de Materiales'
        unique_together = ('producto', 'insumo')
    
    def __str__(self):
        return f"{self.producto.nombre} → {self.insumo.nombre}: {self.cantidad} {self.insumo.unidad_medida}"

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('cotizacion', 'En Cotización'),
        ('confirmado', 'Confirmado'),
        ('en_produccion', 'En Producción'),
        ('listo', 'Listo'),
        ('despachado', 'Despachado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    numero = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    producto = models.ForeignKey(ProductoBase, on_delete=models.PROTECT, related_name='pedidos')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='cotizacion')
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    descripcion_personalizada = models.TextField(help_text="Descripción del diseño y personalización")
    fecha_entrega = models.DateTimeField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas_adicionales = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_creados')
    insumos_descontados = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['fecha_entrega']
    
    def save(self, *args, **kwargs):
        if not self.numero:
            from django.utils import timezone
            ultimo = Pedido.objects.order_by('-id').first()
            siguiente = (ultimo.id + 1) if ultimo else 1
            self.numero = f"DA-{timezone.now().year}-{siguiente:04d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.numero} - {self.cliente.nombre} - {self.producto.nombre}"
    
    @property
    def saldo_pendiente(self):
        return self.precio_total - self.anticipo
    
    def descontar_inventario(self):
        if self.insumos_descontados:
            return False
        bom_items = self.producto.bom_items.select_related('insumo').all()
        for item in bom_items:
            cantidad_total = item.cantidad * self.cantidad
            item.insumo.descontar_stock(cantidad_total)
        self.insumos_descontados = True
        self.save()
        return True

class ItemPedidoPersonalizado(models.Model):
    """Especificaciones personalizadas del pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='personalizaciones')
    campo = models.CharField(max_length=100, help_text="Ej: Color, Sabor, Texto, Figura")
    valor = models.TextField()
    
    class Meta:
        verbose_name = 'Item Personalizado'
        verbose_name_plural = 'Items Personalizados'
    
    def __str__(self):
        return f"{self.pedido.numero} - {self.campo}: {self.valor}"
