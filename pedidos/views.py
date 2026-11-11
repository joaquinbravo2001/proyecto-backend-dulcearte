from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Pedido, Cliente, ProductoBase
from .forms import PedidoForm, ClienteForm
from inventario.models import Insumo
from cocina.models import TareaKanban
from cuentas.decorators import rol_requerido

@login_required
def dashboard(request):
    hoy = timezone.now().date()
    total_pedidos = Pedido.objects.exclude(estado__in=['entregado', 'cancelado']).count()
    pedidos_hoy = Pedido.objects.filter(fecha_entrega__date=hoy).exclude(estado__in=['entregado', 'cancelado']).count()
    insumos_bajos_count = sum(1 for i in Insumo.objects.filter(activo=True) if i.stock_bajo)
    tareas_listas = TareaKanban.objects.filter(estado='listo').count()
    proximas_entregas = Pedido.objects.exclude(estado__in=['entregado', 'cancelado']).order_by('fecha_entrega')[:5]
    alertas_inventario = [i for i in Insumo.objects.filter(activo=True) if i.stock_bajo][:5]
    return render(request, 'pedidos/dashboard.html', {
        'fecha_hoy': hoy,
        'total_pedidos': total_pedidos,
        'pedidos_hoy': pedidos_hoy,
        'insumos_bajos': insumos_bajos_count,
        'tareas_listas': tareas_listas,
        'proximas_entregas': proximas_entregas,
        'alertas_inventario': alertas_inventario,
    })

@login_required
@rol_requerido(['vendedor'])
def lista_pedidos(request):
    queryset = Pedido.objects.select_related('cliente', 'producto').all()
    q = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    if q:
        queryset = queryset.filter(Q(numero__icontains=q) | Q(cliente__nombre__icontains=q) | Q(producto__nombre__icontains=q))
    if estado:
        queryset = queryset.filter(estado=estado)
    return render(request, 'pedidos/lista.html', {
        'pedidos': queryset,
        'estados': Pedido.ESTADO_CHOICES,
    })

@login_required
@rol_requerido(['vendedor'])
def nuevo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.creado_por = request.user
            pedido.save()
            # Crear tarea cocina automáticamente al confirmar
            if pedido.estado == 'confirmado':
                TareaKanban.objects.get_or_create(pedido=pedido)
            messages.success(request, f'Pedido {pedido.numero} creado correctamente.')
            return redirect('pedidos:detalle', pk=pedido.pk)
    else:
        form = PedidoForm()
    return render(request, 'pedidos/form_pedido.html', {'form': form, 'titulo': 'Nuevo Pedido', 'boton_submit': 'Crear Pedido'})

@login_required
@rol_requerido(['vendedor', 'cocinero'])
def editar_pedido(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    estado_anterior = pedido.estado
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            pedido = form.save()
            # Crear tarea cocina si se confirma
            if pedido.estado == 'confirmado' and estado_anterior != 'confirmado':
                TareaKanban.objects.get_or_create(pedido=pedido)
            messages.success(request, f'Pedido {pedido.numero} actualizado.')
            return redirect('pedidos:detalle', pk=pedido.pk)
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'pedidos/form_pedido.html', {'form': form, 'titulo': f'Editar {pedido.numero}', 'boton_submit': 'Guardar Cambios', 'pedido': pedido})

@login_required
def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedido.objects.select_related('cliente', 'producto', 'creado_por'), pk=pk)
    return render(request, 'pedidos/detalle.html', {'pedido': pedido})

@login_required
@rol_requerido(['vendedor', 'bodeguero'])
def descontar_inventario(request, pk):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, pk=pk)
        try:
            if pedido.descontar_inventario():
                messages.success(request, f'Inventario descontado correctamente para {pedido.numero}.')
            else:
                messages.warning(request, 'Los insumos ya fueron descontados anteriormente.')
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('pedidos:detalle', pk=pk)

@login_required
@rol_requerido(['vendedor'])
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('nombre')
    return render(request, 'pedidos/lista_clientes.html', {'clientes': clientes})

@login_required
@rol_requerido(['vendedor'])
def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nombre} registrado.')
            return redirect('pedidos:lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'pedidos/form_cliente.html', {'form': form, 'titulo': 'Nuevo Cliente'})
