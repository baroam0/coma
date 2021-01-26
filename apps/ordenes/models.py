
from django.db import models

from apps.contratistas.models import Contratista
from apps.materiales.models import Material
from apps.obras.models import Obra


class Unidad(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Unidades"


class Orden(models.Model):
    fecha = models.DateField(null=False)
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    encargado = models.CharField(max_length=100, null=True, blank=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.pk) + " - " + str(self.fecha)
    
    class Meta:
        verbose_name_plural="Orden"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    faltante = models.BooleanField(default=False)

    def __str__(self):
        return str(self.orden)
    
    class Meta:
        verbose_name_plural="Detalles Ordenes"

# Create your models here.
