from django import forms
from .models import TareaKanban
from pedidos.models import Pedido
from django.contrib.auth.models import User

class UserModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        nombre_completo = obj.get_full_name().strip()
        if nombre_completo:
            return f"{nombre_completo} (@{obj.username})"
        return obj.username

class TareaKanbanForm(forms.ModelForm):
    responsable = UserModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label='Repostero / Cocinero Responsable'
    )
    class Meta:
        model = TareaKanban
        fields = ['responsable', 'prioridad', 'notas_cocina']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar usuarios con rol cocinero o superusuarios
        self.fields['responsable'].queryset = User.objects.filter(
            is_active=True
        ).filter(
            perfil__rol='cocinero'
        ) | User.objects.filter(is_superuser=True)
        self.fields['responsable'].queryset = self.fields['responsable'].queryset.distinct().order_by('first_name', 'username')

class CrearTareaKanbanForm(forms.ModelForm):
    pedido = forms.ModelChoiceField(
        queryset=Pedido.objects.filter(tarea_cocina__isnull=True).exclude(estado__in=['entregado', 'cancelado']),
        label='Pedido',
        help_text='Selecciona un pedido que aún no tenga tarea en cocina'
    )
    responsable = UserModelChoiceField(
        queryset=User.objects.none(),
        required=False,
        label='Repostero / Cocinero Asignado'
    )
    class Meta:
        model = TareaKanban
        fields = ['pedido', 'responsable', 'prioridad', 'notas_cocina']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsable'].queryset = User.objects.filter(
            is_active=True
        ).filter(
            perfil__rol='cocinero'
        ) | User.objects.filter(is_superuser=True)
        self.fields['responsable'].queryset = self.fields['responsable'].queryset.distinct().order_by('first_name', 'username')
