from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RutaDespacho, EntregaPedido
from .forms import RutaDespachoForm, EntregaForm
from pedidos.models import Pedido
from cuentas.decorators import rol_requerido

@login_required
@rol_requerido(['repartidor'])
def lista_rutas(request):
    rutas = RutaDespacho.objects.prefetch_related('entregas').order_by('-fecha_despacho')
    return render(request, 'despacho/lista_rutas.html', {'rutas': rutas})

@login_required
@rol_requerido(['repartidor'])
def nueva_ruta(request):
    if request.method == 'POST':
        form = RutaDespachoForm(request.POST)
        if form.is_valid():
            ruta = form.save()
            messages.success(request, f'Ruta "{ruta.nombre}" creada.')
            return redirect('despacho:detalle_ruta', pk=ruta.pk)
    else:
        form = RutaDespachoForm()
    return render(request, 'despacho/form_ruta.html', {'form': form})

@login_required
@rol_requerido(['repartidor'])
def detalle_ruta(request, pk):
    ruta = get_object_or_404(RutaDespacho.objects.prefetch_related('entregas__pedido__cliente'), pk=pk)
    pedidos_disponibles = Pedido.objects.filter(estado='listo').exclude(entrega__isnull=False)
    return render(request, 'despacho/detalle_ruta.html', {'ruta': ruta, 'pedidos_disponibles': pedidos_disponibles})

@login_required
@rol_requerido(['repartidor'])
def agregar_entrega(request, ruta_pk):
    ruta = get_object_or_404(RutaDespacho, pk=ruta_pk)
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido_id')
        direccion = request.POST.get('direccion_entrega', '')
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        orden = ruta.entregas.count() + 1
        EntregaPedido.objects.create(ruta=ruta, pedido=pedido, orden_entrega=orden, direccion_entrega=direccion or pedido.cliente.direccion)
        pedido.estado = 'despachado'
        pedido.save()
        messages.success(request, f'Pedido {pedido.numero} agregado a la ruta.')
    return redirect('despacho:detalle_ruta', pk=ruta_pk)

@login_required
@rol_requerido(['repartidor'])
def confirmar_entrega(request, pk):
    entrega = get_object_or_404(EntregaPedido, pk=pk)
    if request.method == 'POST':
        firma = request.FILES.get('firma_digital')
        foto = request.FILES.get('comprobante_foto')
        receptor = request.POST.get('receptor_nombre', '')
        entrega.confirmar_entrega(firma=firma, foto=foto, receptor=receptor)
        messages.success(request, f'Entrega de {entrega.pedido.numero} confirmada.')
    return redirect('despacho:detalle_ruta', pk=entrega.ruta.pk)
