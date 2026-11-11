from django.contrib import admin
from django.utils.html import format_html
from .models import RutaDespacho, EntregaPedido

class EntregaInline(admin.TabularInline):
    model = EntregaPedido
    extra = 0
    readonly_fields = ['hora_entrega_real']
    fields = ['pedido', 'orden_entrega', 'direccion_entrega', 'estado', 'receptor_nombre', 'hora_entrega_real']

@admin.register(RutaDespacho)
class RutaDespachoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_despacho', 'repartidor', 'estado_badge', 'total_entregas']
    list_filter = ['estado', 'fecha_despacho']
    search_fields = ['nombre', 'repartidor__username']
    date_hierarchy = 'fecha_despacho'
    inlines = [EntregaInline]
    
    def estado_badge(self, obj):
        colores = {'planificada': 'orange', 'en_ruta': 'blue', 'completada': 'green', 'cancelada': 'red'}
        color = colores.get(obj.estado, 'gray')
        return format_html('<span style="background:{}; color:white; padding:3px 8px; border-radius:4px;">{}</span>', color, obj.get_estado_display())
    estado_badge.short_description = 'Estado'
    
    def total_entregas(self, obj):
        return obj.entregas.count()
    total_entregas.short_description = 'Entregas'

@admin.register(EntregaPedido)
class EntregaPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'ruta', 'orden_entrega', 'estado', 'receptor_nombre', 'hora_entrega_real', 'tiene_firma', 'tiene_foto']
    list_filter = ['estado', 'ruta']
    search_fields = ['pedido__numero', 'receptor_nombre']
    readonly_fields = ['hora_entrega_real']
    
    def tiene_firma(self, obj):
        return bool(obj.firma_digital)
    tiene_firma.boolean = True
    tiene_firma.short_description = 'Firma'
    
    def tiene_foto(self, obj):
        return bool(obj.comprobante_foto)
    tiene_foto.boolean = True
    tiene_foto.short_description = 'Foto'
