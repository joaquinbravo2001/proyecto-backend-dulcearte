from django.contrib import admin
from django.utils.html import format_html
from .models import TareaKanban, HistorialKanban

@admin.register(TareaKanban)
class TareaKanbanAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'estado_badge', 'prioridad', 'responsable', 'fecha_inicio_real', 'fecha_fin_real']
    list_filter = ['estado', 'prioridad', 'responsable']
    search_fields = ['pedido__numero', 'pedido__cliente__nombre']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    def estado_badge(self, obj):
        colores = {
            'recibido': '#6c757d', 'en_preparacion': '#fd7e14',
            'horneado_decorado': '#c0392b', 'control_calidad': '#6f42c1', 'listo': '#198754'
        }
        color = colores.get(obj.estado, 'gray')
        return format_html('<span style="background:{}; color:white; padding:3px 8px; border-radius:4px;">{}</span>', color, obj.get_estado_display())
    estado_badge.short_description = 'Estado'

@admin.register(HistorialKanban)
class HistorialKanbanAdmin(admin.ModelAdmin):
    list_display = ['tarea', 'estado_anterior', 'estado_nuevo', 'usuario', 'fecha']
    list_filter = ['estado_nuevo', 'fecha']
    search_fields = ['tarea__pedido__numero']
    readonly_fields = ['fecha']
    date_hierarchy = 'fecha'
