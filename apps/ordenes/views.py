
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Orden, Unidad
from apps.contratistas.models import Contratista
from apps.materiales.models import Material
from apps.obras.models import Obra


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
    obras = Obra.objects.all().order_by("descripcion")

    return render(
        request,
        "ordenes/orden_edit.html",
        {
            "contratistas": contratistas,
            "materiales": materiales,
            "obras": obras,
            "unidades": unidades
        }
    )


@csrf_exempt
def ajaxgrabarorden(request):
    fecha = request.POST["fecha"]
    

# Create your views here.
