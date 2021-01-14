
from django import forms

from apps.contratistas.models import Contratista
from .models import Orden, DetalleOrden, Unidad


class OrdenForm(forms.ModelForm):
    fecha = forms.DateField(requireds=True)
    contratista = forms.ModelChoiceField(
        label="Contratista",
        queryset=Contratista.objects.all(),
        required=True
    )
    encargado = forms.CharField(label="Encagado", required=True)

    def __init__(self, *args, **kwargs):
        super(OrdenForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'pure-input-1'
            })

    class Meta:
        model = Orden
        fields = ['fecha', 'contratista', 'encargado']


class DetalleOrdenForm(forms.ModelForm):
    material = forms.ModelChoiceField(
        label="Material",
        queryset=Material.objects.all(),
    )
    cantidad = forms.DecimalField(label="Cantidad", required=True)
    unidad = forms.ModelChoiceField(
        label="Unidad",
        queryset=
    )

    def __init__(self, *args, **kwargs):
        super(DetalleOrdenForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'pure-input-1'
            })

    class Meta:
        model = Orden
        fields = ['material', 'cantidad', 'unidad']
    
