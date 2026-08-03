
from django.db import models

from contratistas.models import Contratista
from documentaciones.models import Documentacion
from materiales.models import Material, Unidad

class Remito(models.Model):
    fecha=models.DateField()
    numerosop = models.IntegerField(null=True, blank=True)
    destinatario = models.ForeignKey(
        Contratista, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    textodestinatario = models.CharField(
        max_length=250, null=True, blank=True)
    destino=models.ForeignKey(
        Documentacion, on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    textodestino=models.CharField(
        max_length=250, null=True, blank=True)
    
    def __str__(self):
        return str(self.fecha) + '-' + str(self.pk)
    
    class Meta:
        verbose_name_plural="Remitos"


class DetalleRemito(models.Model):
    remito=models.ForeignKey(Remito, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    unidad = models.ForeignKey(Unidad, null=True, blank=True, on_delete=models.CASCADE)
    cantidad = models.DecimalField(decimal_places=4, max_digits=10, null=True, blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name_plural = "Detalles Remito"
# Create your models here.
