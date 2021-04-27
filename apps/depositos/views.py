
from django.http import JsonResponse
from django.shortcuts import render

from .models import DepositoCantidad
from apps.contratistas.models import Contratista
from apps.obras.models import Obra
from apps.ordenes.models import Unidad


def listadodeposito(request):
    resultados = None
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro!="":
            if parametro.isnumeric():
                try:
                    resultados = DepositoCantidad.objects.filter(
                        pk=int(parametro)
                    )
                except:
                    resultados=None
            else:
                resultados = DepositoCantidad.objects.filter(
                    material__iconatains=parametro).order_by("material")
        else:
            resultados = DepositoCantidad.objects.all().order_by("material")
    return render(
        request,
        "depositos/listadodeposito.html",
        {
            "resultados": resultados
        }
    )


def nuevaordendeposito(request):
    contratistas = Contratista.objects.all()
    unidades = Unidad.objects.all().order_by("descripcion")
    obras = Obra.objects.all().order_by("descripcion")

    return render(
        request,
        "depositos/ordendeposito_nueva.html",
        {
            "contratistas": contratistas,
            "obras": obras,
            "unidades": unidades
        }
    )


def editarordendeposito(request, pk):
    deposito = DepositoCantidad.objects.get(pk=pk)
    contratistas = Contratista.objects.all()
    unidades = Unidad.objects.all().order_by("descripcion")
    obras = Obra.objects.all().order_by("descripcion")

    return render(
        request,
        "depositos/ordendeposito_editar.html",
        {
            "contratistas": contratistas,
            "obras": obras,
            "unidades": unidades
        }
    )


# Create your views here.
