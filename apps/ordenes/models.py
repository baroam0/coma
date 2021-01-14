
from django.db import models

from apps.contratistas.models import Contratista
from apps.materiales.models import Material


class Unidad(models.Model):
    descripcion = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name_plural = "Unidades"


class Orden(models.Model):
    fecha = models.DateField(null=False)
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE)
    encargado = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return str(self.fecha)
    
    class Meta:
        verbose_name_plural="Operaciones"


class DetalleOrden(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.orden)
    
    class Meta:
        verbose_name_plural="Detalles Operaciones"

# Create your models here.
