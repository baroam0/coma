

from django.db import models

from apps.materiales.models import Material


class DepositoCantidad(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, unique=True)
    cantidad = models.DecimalField(decimal_places=2, max_digits=10)
    cantidad_minima = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.cantidad) + " - " + str(self.material.description).upper()

    class Meta:
        verbose_name_plural = "Materiales en Deposito"


def agregamaterial(material_id, cantidadingresada):
    materialdeposito = DepositoCantidad.objects.get(material=material_id)
    materialdeposito.cantidad = float(materialdeposito.cantidad) + cantidadingresada
    materialdeposito.save()


def quitamaterial(material_id, cantidadingresada):
    materialdeposito = DepositoCantidad.objects.get(material=material_id)

    if float(materialdeposito.cantidad) < float(cantidadingresada):
        materialdeposito.cantidad = float(materialdeposito.cantidad) - cantidadingresada
        materialdeposito.save()       
        return False
    else:
        materialdeposito.cantidad = float(materialdeposito.cantidad) - cantidadingresada
        materialdeposito.save()
        return True

    

# Create your models here.
