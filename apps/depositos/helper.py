
from django.http import JsonResponse

from .models import DepositoCantidad
from apps.materiales.models import Material


def agregamaterial(material_id, cantidadingresada):
    try:
        material = Material.objects.get(pk=material_id)
        materialdeposito = DepositoCantidad.objects.get(material=material)
        materialdeposito.cantidad = float(materialdeposito.cantidad) + cantidadingresada
    except:
        materialdeposito = DepositoCantidad(
            material=material,
            cantidad=cantidadingresada
        )
    materialdeposito.save()


def quitamaterial(material_id, cantidadingresada):
    materialdeposito = DepositoCantidad.objects.get(material=material_id)

    if float(materialdeposito.cantidad) < float(cantidadingresada):
        materialdeposito.cantidad = float(materialdeposito.cantidad) - cantidadingresada
        materialdeposito.save()
        data = {
            "alerta": 1
        }
    else:
        materialdeposito.cantidad = float(materialdeposito.cantidad) - cantidadingresada
        materialdeposito.save()
        data = {
            "alerta": 0
        }
    return JsonResponse(data)