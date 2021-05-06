
from django.db import models

from apps.contratistas.models import Contratista
from apps.materiales.models import Material
from apps.obras.models import Obra
from apps.ordenes.models import Unidad


class DepositoCantidad(models.Model):
    material = models.OneToOneField(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField(decimal_places=2, max_digits=10)
    cantidad_minima = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return str(self.cantidad) + " - " + str(self.material.descripcion).upper()

    class Meta:
        verbose_name_plural = "Materiales en Deposito"    


class DepositoOrden(models.Model):
    fecha = models.DateField(null=False)
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    encargado = models.CharField(max_length=100, null=True, blank=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.pk) + " - " + str(self.fecha)

    class Meta:
        verbose_name_plural="Deposito Orden"


class DepositoDetalleOrden(models.Model):
    orden = models.ForeignKey(DepositoOrden, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    faltante = models.BooleanField(default=False)

    def __str__(self):
        return str(self.orden)

    class Meta:
        verbose_name_plural="Deposito Detalles Ordenes"


# Create your models here.
