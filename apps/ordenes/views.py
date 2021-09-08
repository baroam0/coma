

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import DetalleOrden, Orden, Unidad
from apps.contratistas.models import Contratista
from apps.materiales.models import Material
from apps.obras.models import Obra

from apps.libs.funcionfecha import revertirfecha
from apps.depositos.helper import agregamaterial


def listadoorden(request):
    resultados = None
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        if parametro!="":
            if parametro.isnumeric():
                try:
                    resultados = Orden.objects.filter(
                        pk=int(parametro)
                    )
                except:
                    resultados=None
            else:
                resultados = Orden.objects.filter(
                    Q(obra__descripcion__icontains=parametro) |
                    Q(contratista__descripcion__icontains=parametro)).order_by("-pk")
        else:
            resultados = Orden.objects.all().order_by("-pk")

    return render(
        request,
        "ordenes/listadoorden.html",
        {
            "resultados": resultados
        }
    )


def nuevaorden(request):
    contratistas = Contratista.objects.all()
    unidades = Unidad.objects.all().order_by("descripcion")
    obras = Obra.objects.all().order_by("descripcion")

    return render(
        request,
        "ordenes/orden_nueva.html",
        {
            "contratistas": contratistas,
            "obras": obras,
            "unidades": unidades
        }
    )


@csrf_exempt
def ajaxgrabarorden(request):
    fecha = request.POST["fecha"]
    fecha = revertirfecha(fecha)
    contratista= Contratista.objects.get(pk=int(request.POST["contratista"]))
    encargado = request.POST["encargado"]
    obra = Obra.objects.get(pk=int(request.POST["obra"]))

    arraymaterial = request.POST.getlist('arraymaterial[]')
    arrayunidad = request.POST.getlist('arrayunidad[]')
    arraycantidad = request.POST.getlist('arraycantidad[]')

    orden=Orden(
        fecha=fecha,
        contratista=contratista,
        encargado=encargado,
        obra=obra
    )

    orden.save()
    orden = Orden.objects.latest("pk")

    for (material, unidad, cantidad) in zip(arraymaterial, arrayunidad, arraycantidad):
        material = Material.objects.get(pk=int(material))
        unidad = Unidad.objects.get(pk=int(unidad))

        detalleorden = DetalleOrden(
            orden=orden,
            material=material,
            cantidad=cantidad,
            unidad=unidad
        )

        agregamaterial(material.pk, cantidad)

        detalleorden.save()

    data = {
        "status": 200
    }

    return JsonResponse(data)


def editarorden(request, pk):
    contratistas = Contratista.objects.all()
    unidades = Unidad.objects.all().order_by("descripcion")
    obras = Obra.objects.all().order_by("descripcion")

    orden = Orden.objects.get(pk=pk)
    detallesorden = DetalleOrden.objects.filter(
        orden=orden
    )

    return render(
        request,
        "ordenes/orden_edit.html",
        {
            "orden": orden,
            "detallesorden": detallesorden,
            "contratistas": contratistas,
            "unidades": unidades,
            "obras": obras
        }
    )


@csrf_exempt
def ajaxgrabareditarorden(request,pk):
    detalleorden=DetalleOrden.objects.filter(orden=pk)
    detalleorden.delete()

    fecha = request.POST["fecha"]
    fecha = revertirfecha(fecha)
    contratista= Contratista.objects.get(pk=int(request.POST["contratista"]))
    encargado = request.POST["encargado"]
    obra = Obra.objects.get(pk=int(request.POST["obra"]))

    arraymaterial = request.POST.getlist('arraymaterial[]')
    arrayunidad = request.POST.getlist('arrayunidad[]')
    arraycantidad = request.POST.getlist('arraycantidad[]')
    arrayfaltante = request.POST.getlist('arrayfaltante[]')

    orden = Orden.objects.get(pk=pk)

    orden = Orden.objects.filter(pk=pk).update(
        fecha=fecha,
        contratista=contratista,
        encargado=encargado,
        obra=obra
    )
    obra.save()

    orden = Orden.objects.get(pk=pk)

    for (material, unidad, cantidad, faltante) in zip(arraymaterial, arrayunidad, arraycantidad, arrayfaltante):
        material = Material.objects.get(pk=int(material))
        unidad = Unidad.objects.get(pk=int(unidad))

        detalleorden = DetalleOrden(
            orden=orden,
            material=material,
            cantidad=cantidad,
            unidad=unidad,
            faltante=faltante
        )
        print(detalleorden)

        detalleorden.save()

    data = {
        "status": 200
    }

    return JsonResponse(data)


def imprimirorden(request,pk):
    orden = Orden.objects.get(pk=pk)
    detallesorden = DetalleOrden.objects.filter(orden=orden)

    return render(
        request,
        "ordenes/imprimirorden.html",
        {
            "orden": orden,
            "detallesorden": detallesorden
        }
    )

# Create your views here.
