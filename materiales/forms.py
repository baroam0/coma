

from django import forms
from .models import Material

class MaterialForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
            super(MaterialForm, self).__init__(*args, **kwargs)
            
            for field in iter(self.fields):
                    self.fields[field].widget.attrs.update({
                        'class': 'form-control form-control-user'
                    })
    
    class Meta:
        model = Material
        fields = [
            'descripcion'
        ]

        widgets = {            
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion'}),
        }
