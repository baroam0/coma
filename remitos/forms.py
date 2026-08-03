
from django import forms
from .models import Remito, DetalleRemito

from contratistas.models import Contratista
from documentaciones.models import Documentacion
from materiales.models import Material


class RemitoForm(forms.ModelForm):
    class Meta:
        model = Remito
        fields = [
            'fecha',
            'destinatario',
            'numerosop',
            'textodestinatario',
            'destino',
            'textodestino',
        ]

        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'numerosop': forms.NumberInput(
                        attrs={'class': 'form-control'}
                        ),
            'destinatario': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'textodestinatario': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'destino': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'textodestino': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['destino'].queryset = Documentacion.objects.filter(
            tipo__in=['M', 'A']
        ).order_by('-id')

        self.fields['destinatario'].queryset = Contratista.objects.all().order_by('-descripcion')


class DetalleRemitoForm(forms.ModelForm):
    class Meta:
        model = DetalleRemito
    
        fields = [
            'material',
            'unidad',
            'cantidad'
        ]

        widgets = {
            'material': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'unidad': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'cantidad': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].queryset = Material.objects.none()
