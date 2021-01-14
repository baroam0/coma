

from django import forms

from .models import Contratista


class ContratistaForm(forms.ModelForm):
    descripcion = forms.CharField(
        label="Descripcion", required=True)

    def __init__(self, *args, **kwargs):
        super(ContratistaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'pure-input-1'
            })

    class Meta:
        model = Contratista
        fields = ['descripcion']
    
