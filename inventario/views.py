from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Insumo, Categoria, MovimientoInventario
from .forms import InsumoForm, AjusteStockForm
from cuentas.decorators import rol_requerido

@login_required
@rol_requerido(['bodeguero'])
def lista_inventario(request):
    insumos = Insumo.objects.select_related('categoria').filter(activo=True)
    alertas = sum(1 for i in insumos if i.stock_bajo)
    return render(request, 'inventario/lista.html', {'insumos': insumos, 'alertas': alertas})

@login_required
@rol_requerido(['bodeguero'])
def nuevo_insumo(request):
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            insumo = form.save()
            messages.success(request, f'Insumo "{insumo.nombre}" creado.')
            return redirect('inventario:lista')
    else:
        form = InsumoForm()
    return render(request, 'inventario/form_insumo.html', {'form': form, 'titulo': 'Nuevo Insumo'})

@login_required
@rol_requerido(['bodeguero'])
def editar_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=insumo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Insumo "{insumo.nombre}" actualizado.')
            return redirect('inventario:lista')
    else:
        form = InsumoForm(instance=insumo)
    return render(request, 'inventario/form_insumo.html', {'form': form, 'titulo': f'Editar: {insumo.nombre}'})

@login_required
@rol_requerido(['bodeguero'])
def ajuste_stock(request):
    if request.method == 'POST':
        form = AjusteStockForm(request.POST)
        if form.is_valid():
            insumo = form.cleaned_data['insumo']
            tipo = form.cleaned_data['tipo']
            cantidad = form.cleaned_data['cantidad']
            motivo = form.cleaned_data['motivo']
            stock_ant = insumo.stock_actual
            if tipo == 'entrada':
                insumo.stock_actual += cantidad
            elif tipo == 'salida':
                if insumo.stock_actual < cantidad:
                    messages.error(request, f'Stock insuficiente. Disponible: {insumo.stock_actual}')
                    return render(request, 'inventario/ajuste_stock.html', {'form': form})
                insumo.stock_actual -= cantidad
            else:
                insumo.stock_actual = cantidad
            insumo.save()
            MovimientoInventario.objects.create(
                insumo=insumo, tipo=tipo, cantidad=cantidad,
                stock_anterior=stock_ant, stock_posterior=insumo.stock_actual,
                motivo=motivo, usuario=request.user
            )
            messages.success(request, f'Stock de "{insumo.nombre}" actualizado: {stock_ant} → {insumo.stock_actual}')
            return redirect('inventario:lista')
    else:
        form = AjusteStockForm()
    return render(request, 'inventario/ajuste_stock.html', {'form': form})

@login_required
@rol_requerido(['bodeguero'])
def historial_insumo(request, pk):
    insumo = get_object_or_404(Insumo, pk=pk)
    movimientos = MovimientoInventario.objects.filter(insumo=insumo).order_by('-fecha')
    return render(request, 'inventario/historial.html', {'insumo': insumo, 'movimientos': movimientos})
