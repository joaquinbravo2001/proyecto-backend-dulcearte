from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Insumo, MovimientoInventario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'total_insumos']
    search_fields = ['nombre']
    
    def total_insumos(self, obj):
        return obj.insumos.count()
    total_insumos.short_description = 'Insumos'

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'stock_actual', 'stock_minimo', 'unidad_medida', 'costo_unitario', 'estado_stock', 'activo']
    list_filter = ['categoria', 'unidad_medida', 'activo']
    search_fields = ['nombre', 'proveedor']
    list_editable = ['activo']
    readonly_fields = ['fecha_ultima_actualizacion']
    fieldsets = (
        ('Información General', {'fields': ('nombre', 'categoria', 'proveedor', 'activo')}),
        ('Stock', {'fields': ('unidad_medida', 'stock_actual', 'stock_minimo', 'costo_unitario')}),
        ('Metadatos', {'fields': ('fecha_ultima_actualizacion',)}),
    )
    
    def estado_stock(self, obj):
        if obj.stock_bajo:
            return format_html('<span style="color: red; font-weight: bold;">⚠ Stock Bajo</span>')
        return format_html('<span style="color: green;">✓ OK</span>')
    estado_stock.short_description = 'Estado'

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['insumo', 'tipo', 'cantidad', 'stock_anterior', 'stock_posterior', 'usuario', 'fecha']
    list_filter = ['tipo', 'fecha', 'insumo__categoria']
    search_fields = ['insumo__nombre', 'motivo']
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
