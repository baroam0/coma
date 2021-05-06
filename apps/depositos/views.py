
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import DepositoCantidadForm

from .models import DepositoCantidad
from apps.contratistas.models import Contratista
from apps.materiales.models import Material
from apps.obras.models import Obra
from apps.ordenes.models import Unidad


def listadodepositomateriales(request):
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


def editardepositocantidad(request, pk):
    consulta = DepositoCantidad.objects.get(pk=pk)
    if request.POST:
        form = DepositoCantidadForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA LA CANTIDAD DEL MATERIAL")
            return redirect('/listadodepositomateriales')
        else:
            return render(request, 'depositos/depositocantidad_editar.html', {"form": form})
    else:
        form = DepositoCantidadForm(instance=consulta)
        return render(request,
            'depositos/depositocantidad_editar.html',
            {"form": form}
        )


def nuevaordendeposito(request):
    contratistas = Contratista.objects.all()
    unidades = Unidad.objects.all().order_by("descripcion")
    obras = Obra.objects.all().order_by("descripcion").exclude(descripcion="Deposito")

    return render(
        request,
        "depositos/ordendeposito_nueva.html",
        {
            "contratistas": contratistas,
            "obras": obras,
            "unidades": unidades
        }
    )


def ajaxordencantidadmaterial(request):
    parametro = request.GET.get('term')
    material = DepositoCantidad.objects.select_related('material').filter(material__descripcion__icontains=parametro)

    dict_tmp = dict()
    list_tmp = list()

    if len(material) > 0:
        for i in material:
            dict_tmp["id"] = i.pk
            dict_tmp["text"] = i.material.descripcion.upper()
            list_tmp.append(dict_tmp)
            dict_tmp = dict()

    return JsonResponse(list_tmp, safe=False)


def editarordendeposito(request, pk):
    deposito = DepositoCantidad.objects.get(pk=pk)
    contratistas = Contratista.objects.all()
    unidades = Unidad.objects.all().order_by("descripcion")
    obras = Obra.objects.all().order_by("descripcion").exclude(descripcion="Deposito")

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
