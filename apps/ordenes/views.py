
from django.shortcuts import render

from .models import Orden, Unidad
from apps.contratistas.models import Contratista
from apps.materiales.models import Material


def listadoorden(request):
    resultados = None
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        resultados = Orden.objects.filter(pk=int(parametro)).order_by("fecha")

    return render(
        request,
        "ordenes/listadoorden.html",
        {
            "resultados": resultados
        }
    )


def nuevaorden(request):
    contratistas = Contratista.objects.all()
    materiales = Material.objects.all().order_by("descripcion")
    unidades = Unidad.objects.all().order_by("descripcion")

    return render(
        request,
        "ordenes/orden_edit.html",
        {
            "contratistas": contratistas,
            "materiales": materiales,
            "unidades": unidades
        }
    )
    

# Create your views here.
