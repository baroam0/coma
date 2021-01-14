

from django import forms

from .models import Material


class MaterialForm(forms.ModelForm):
    descripcion = forms.CharField(
        label="Descripcion", required=True)

    def __init__(self, *args, **kwargs):
        super(MaterialForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'pure-input-1'
            })

    class Meta:
        model = Material
        fields = ['descripcion']
    
