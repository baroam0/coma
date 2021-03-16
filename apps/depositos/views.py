
from django.http import JsonResponse
from django.shortcuts import render

from .models import DepositoCantidad


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
    

# Create your views here.
