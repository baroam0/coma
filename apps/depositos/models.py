

from django.db import models

from apps.materiales.models import Material


class DepositoCantidad(models.Model):
    material = models.OneToOneField(Material, on_delete=models.CASCADE)
    cantidad = models.DecimalField(decimal_places=2, max_digits=10)
    cantidad_minima = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    def __str__(self):
        return str(self.cantidad) + " - " + str(self.material.description).upper()

    class Meta:
        verbose_name_plural = "Materiales en Deposito"    



# Create your models here.
