from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TareaKanban, HistorialKanban
from .forms import TareaKanbanForm, CrearTareaKanbanForm
from cuentas.decorators import rol_requerido
from pedidos.models import Pedido

COLUMNAS = [
    {'key': 'recibido', 'nombre': 'Recibido', 'color': '#6c757d', 'icono': 'bi-inbox'},
    {'key': 'en_preparacion', 'nombre': 'En Preparación', 'color': '#fd7e14', 'icono': 'bi-tools'},
    {'key': 'horneado_decorado', 'nombre': 'Horneado / Decorado', 'color': '#c0392b', 'icono': 'bi-fire'},
    {'key': 'control_calidad', 'nombre': 'Control de Calidad', 'color': '#6f42c1', 'icono': 'bi-patch-check'},
    {'key': 'listo', 'nombre': 'Listo', 'color': '#198754', 'icono': 'bi-check-circle'},
]

@login_required
@rol_requerido(['cocinero'])
def kanban(request):
    tareas = TareaKanban.objects.select_related('pedido__cliente', 'pedido__producto', 'responsable').all()
    columnas = []
    for col in COLUMNAS:
        columnas.append({**col, 'tareas': [t for t in tareas if t.estado == col['key']]})
    
    pedidos_sin_tarea = Pedido.objects.filter(tarea_cocina__isnull=True).exclude(estado__in=['entregado', 'cancelado']).count()

    return render(request, 'cocina/kanban.html', {
        'columnas': columnas,
        'total_tareas': tareas.count(),
        'pedidos_sin_tarea': pedidos_sin_tarea,
    })

@login_required
@rol_requerido(['cocinero'])
def nueva_tarea(request):
    if request.method == 'POST':
        form = CrearTareaKanbanForm(request.POST)
        if form.is_valid():
            tarea = form.save()
            # Si el pedido estaba en cotización o confirmado, pasa a en_producción
            if tarea.pedido.estado in ['cotizacion', 'confirmado']:
                tarea.pedido.estado = 'en_produccion'
                tarea.pedido.save()
            messages.success(request, f'Tarea para pedido {tarea.pedido.numero} ingresada a cocina.')
            return redirect('cocina:kanban')
    else:
        form = CrearTareaKanbanForm()
    return render(request, 'cocina/form_tarea.html', {'form': form})

@login_required
@rol_requerido(['cocinero'])
def avanzar_tarea(request, pk):
    if request.method == 'POST':
        tarea = get_object_or_404(TareaKanban, pk=pk)
        estado_anterior = tarea.estado
        if tarea.avanzar_estado():
            HistorialKanban.objects.create(
                tarea=tarea, estado_anterior=estado_anterior,
                estado_nuevo=tarea.estado, usuario=request.user
            )
            messages.success(request, f'Tarea {tarea.pedido.numero} avanzada a: {tarea.get_estado_display()}')
        else:
            messages.warning(request, 'La tarea ya está en el último estado.')
    return redirect('cocina:kanban')

@login_required
@rol_requerido(['cocinero'])
def detalle_tarea(request, pk):
    tarea = get_object_or_404(TareaKanban.objects.select_related('pedido__cliente', 'pedido__producto'), pk=pk)
    form = TareaKanbanForm(instance=tarea)
    return render(request, 'cocina/detalle_tarea.html', {'tarea': tarea, 'form': form})

@login_required
@rol_requerido(['cocinero'])
def actualizar_tarea(request, pk):
    tarea = get_object_or_404(TareaKanban, pk=pk)
    if request.method == 'POST':
        form = TareaKanbanForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada.')
        return redirect('cocina:detalle_tarea', pk=pk)
    return redirect('cocina:kanban')
