from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, ProductoBase, BOM, Pedido, ItemPedidoPersonalizado

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email', 'total_pedidos', 'fecha_registro']
    search_fields = ['nombre', 'telefono', 'email']
    
    def total_pedidos(self, obj):
        return obj.pedidos.count()
    total_pedidos.short_description = 'Pedidos'

class BOMInline(admin.TabularInline):
    model = BOM
    extra = 1

@admin.register(ProductoBase)
class ProductoBaseAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio_base', 'tiempo_preparacion_horas', 'activo', 'miniatura']
    list_filter = ['activo']
    search_fields = ['nombre']
    list_editable = ['activo']
    inlines = [BOMInline]
    
    def miniatura(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="height:40px; border-radius:4px;">', obj.imagen.url)
        return '-'
    miniatura.short_description = 'Imagen'

class ItemPersonalizadoInline(admin.TabularInline):
    model = ItemPedidoPersonalizado
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'producto', 'cantidad', 'fecha_entrega', 'precio_total', 'estado_badge', 'insumos_descontados']
    list_filter = ['estado', 'insumos_descontados', 'fecha_entrega']
    search_fields = ['numero', 'cliente__nombre', 'producto__nombre']
    readonly_fields = ['numero', 'fecha_creacion', 'fecha_actualizacion']
    date_hierarchy = 'fecha_entrega'
    inlines = [ItemPersonalizadoInline]
    fieldsets = (
        ('Identificación', {'fields': ('numero', 'estado', 'insumos_descontados')}),
        ('Datos del Pedido', {'fields': ('cliente', 'producto', 'cantidad', 'descripcion_personalizada')}),
        ('Fechas y Precios', {'fields': ('fecha_entrega', 'precio_total', 'anticipo')}),
        ('Notas', {'fields': ('notas_adicionales', 'creado_por')}),
        ('Metadatos', {'fields': ('fecha_creacion', 'fecha_actualizacion'), 'classes': ('collapse',)}),
    )
    
    def estado_badge(self, obj):
        colores = {
            'cotizacion': 'orange', 'confirmado': 'blue', 'en_produccion': 'purple',
            'listo': 'green', 'despachado': 'teal', 'entregado': 'darkgreen', 'cancelado': 'red'
        }
        color = colores.get(obj.estado, 'gray')
        return format_html('<span style="background:{}; color:white; padding:3px 8px; border-radius:4px; font-size:0.85em;">{}</span>', color, obj.get_estado_display())
    estado_badge.short_description = 'Estado'

@admin.register(BOM)
class BOMAdmin(admin.ModelAdmin):
    list_display = ['producto', 'insumo', 'cantidad']
    list_filter = ['producto']
    search_fields = ['producto__nombre', 'insumo__nombre']
