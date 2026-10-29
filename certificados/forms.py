from django import forms
from .models import Certificado

class CertificadoForm(forms.ModelForm):

    class Meta:
        model = Certificado
        fields = [
            'fecha',
            'numero',
            'descripcion',
            'monto',
            'expediente_madre',
        ]

        widgets = {
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-user'
            }, format='%Y-%m-%d'),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nro Expediente'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto'}),
            'expediente_madre': forms.Select(attrs={'class': 'form-control'}),
        }
