from django import forms
from .models import RutaDespacho, EntregaPedido
from pedidos.models import Pedido

class RutaDespachoForm(forms.ModelForm):
    class Meta:
        model = RutaDespacho
        fields = ['nombre', 'fecha_despacho', 'repartidor', 'notas']
        widgets = {'fecha_despacho': forms.DateInput(attrs={'type': 'date'})}

class EntregaForm(forms.ModelForm):
    class Meta:
        model = EntregaPedido
        fields = ['pedido', 'orden_entrega', 'direccion_entrega']
