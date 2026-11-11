from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class Insumo(models.Model):
    UNIDAD_CHOICES = [
        ('kg', 'Kilogramos'),
        ('g', 'Gramos'),
        ('l', 'Litros'),
        ('ml', 'Mililitros'),
        ('u', 'Unidades'),
        ('paq', 'Paquetes'),
    ]
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='insumos')
    unidad_medida = models.CharField(max_length=10, choices=UNIDAD_CHOICES, default='kg')
    stock_actual = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[MinValueValidator(Decimal('0'))])
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=3, default=0, validators=[MinValueValidator(Decimal('0'))])
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proveedor = models.CharField(max_length=200, blank=True)
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Insumo'
        verbose_name_plural = 'Insumos'
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} ({self.stock_actual} {self.unidad_medida})"
    
    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo
    
    def descontar_stock(self, cantidad):
        if self.stock_actual < cantidad:
            raise ValueError(f"Stock insuficiente para {self.nombre}. Disponible: {self.stock_actual}, Requerido: {cantidad}")
        self.stock_actual -= cantidad
        self.save()

class MovimientoInventario(models.Model):
    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
    ]
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, related_name='movimientos')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3)
    stock_anterior = models.DecimalField(max_digits=10, decimal_places=3)
    stock_posterior = models.DecimalField(max_digits=10, decimal_places=3)
    motivo = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-fecha']
    
    def __str__(self):
        return f"{self.tipo} - {self.insumo.nombre} - {self.cantidad} - {self.fecha.strftime('%d/%m/%Y')}"
