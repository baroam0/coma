
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect

from .forms import DepositoCantidadForm

from .models import DepositoCantidad, DepositoOrden, DepositoDetalleOrden
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


@csrf_exempt
def ajaxgrabarordendeposito(request):
    fecha = request.POST["fecha"]
    fecha = revertirfecha(fecha)
    contratista= Contratista.objects.get(pk=int(request.POST["contratista"]))
    encargado = request.POST["encargado"]
    obra = Obra.objects.get(pk=int(request.POST["obra"]))

    arraymaterial = request.POST.getlist('arraymaterial[]')
    arrayunidad = request.POST.getlist('arrayunidad[]')
    arraycantidad = request.POST.getlist('arraycantidad[]')


    depositoorden= DepositoOrden(
        fecha=fecha,
        contratista=contratista,
        encargado=encargado,
        obra=obra
    )

    depositoorden.save()
    depositoorden = DepositoOrden.objects.latest("pk")

    material = models.ForeignKey(Material, on_delete=models.CASCADE)


    faltante = models.BooleanField(default=False)


    for (material, unidad, cantidad) in zip(arraymaterial, arrayunidad, arraycantidad):
        material = Material.objects.get(pk=int(material))
        unidad = Unidad.objects.get(pk=int(unidad))

        depositodetalleorden = DepositoDetalleOrden(
            orden=depositoorden,
            material=material,
            cantidad=cantidad,
            unidad=unidad,

        )

        agregamaterial(material.pk, cantidad)

        detalleorden.save()

    data = {
        "status": 200
    }

    return JsonResponse(data)

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
