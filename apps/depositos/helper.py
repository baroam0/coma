
from django.http import JsonResponse

from .models import DepositoCantidad
from apps.materiales.models import Material


def agregamaterial(material_id, cantidadingresada):
    try:
        material = Material.objects.get(pk=material_id)
        materialdeposito = DepositoCantidad.objects.get(material=material)
        materialdeposito.cantidad = float(materialdeposito.cantidad) + float(cantidadingresada)
    except:
        materialdeposito = DepositoCantidad(
            material=material,
            cantidad=cantidadingresada
        )
    materialdeposito.save()


def validacantidad(material_id, cantidad):
    material = Material.objects.get(pk=material_id)
    deposito = DepositoCantidad.objects.get(material=material)

    if float(cantidad) < float(deposito.cantidad):
        return 1
    else:
        return 0
