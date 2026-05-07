

from django import forms
from .models import Documentacion

class DocumentacionForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
            super(DocumentacionForm, self).__init__(*args, **kwargs)
            
            for field in iter(self.fields):
                    self.fields[field].widget.attrs.update({
                        'class': 'form-control form-control-user'
                    })
    
    class Meta:
        model = Documentacion
        fields = [
            'fechanota',
            'nota',
            'tipo',
            'fechaexpediente',
            'nomenclatura',
            'descripcion',
            'monto',
            'decreto',
            'fechadecreto',
            'observaciones',
            'estado'
        ]

        widgets = {            
            'fechanota': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-user'
            }),
            'nota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nro Nota'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fechaexpediente': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-user'
            }),
            'nomenclatura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nro Expediente'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto'}),
            'decreto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Decreto'}),
            'fechadecreto': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-user'
            }),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observaciones'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
