

from django import forms
from .models import Contratista

class ContratistaForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
            super(ContratistaForm, self).__init__(*args, **kwargs)
            
            for field in iter(self.fields):
                    self.fields[field].widget.attrs.update({
                        'class': 'form-control form-control-user'
                    })
    
    class Meta:
        model = Contratista
        fields = [
            'descripcion',
            'responsable',
            'responsabledni',
            'domicilio'
        ]

        widgets = {            
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
            'responsabledni': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Numero Documento'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domicilio'}),
        }

