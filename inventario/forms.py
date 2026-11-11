from django import forms
from .models import Insumo, Categoria, MovimientoInventario

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'categoria', 'unidad_medida', 'stock_actual', 'stock_minimo', 'costo_unitario', 'proveedor', 'activo']

class AjusteStockForm(forms.Form):
    insumo = forms.ModelChoiceField(queryset=Insumo.objects.filter(activo=True), label='Insumo')
    tipo = forms.ChoiceField(choices=[('entrada', 'Entrada'), ('salida', 'Salida'), ('ajuste', 'Ajuste')], label='Tipo')
    cantidad = forms.DecimalField(min_value=0.001, max_digits=10, decimal_places=3, label='Cantidad')
    motivo = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False, label='Motivo')
