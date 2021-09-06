

from django import forms

from .models import DepositoCantidad
from apps.materiales.models import Material


class DepositoCantidadForm(forms.ModelForm):
    material = forms.ModelChoiceField(label="Material", queryset= Material.objects.all())
    cantidad = forms.DecimalField(label="Cantidad")
    cantidad_minima = forms.DecimalField(label="Cantidad Minima")

    def __init__(self, *args, **kwargs):
        super(DepositoCantidadForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'pure-input-1'
            })

    class Meta:
        model = DepositoCantidad
        fields = ['material', 'cantidad', 'cantidad_minima']

