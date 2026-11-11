from django import forms
from .models import Pedido, Cliente, ProductoBase, BOM, ItemPedidoPersonalizado
from django.utils import timezone

class PedidoForm(forms.ModelForm):
    fecha_entrega = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        label='Fecha y Hora de Entrega'
    )
    class Meta:
        model = Pedido
        fields = ['cliente', 'producto', 'cantidad', 'descripcion_personalizada', 
                  'fecha_entrega', 'precio_total', 'anticipo', 'estado', 'notas_adicionales']
    
    def clean_fecha_entrega(self):
        fecha = self.cleaned_data.get('fecha_entrega')
        if fecha and fecha < timezone.now():
            raise forms.ValidationError("La fecha de entrega no puede ser en el pasado.")
        return fecha

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProductoBaseForm(forms.ModelForm):
    class Meta:
        model = ProductoBase
        fields = '__all__'

class BOMForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = '__all__'
