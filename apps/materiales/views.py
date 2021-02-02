

from django.contrib import messages
from django.http import JsonResponse 
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .models import Material
from .forms import MaterialForm


def listadomaterial(request):
    resultados = None
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        resultados = Material.objects.filter(descripcion__icontains=parametro)

    return render(
        request,
        "materiales/listadomaterial.html",
        {
            "resultados": resultados
        }
    )


def nuevomaterial(request):
    if request.POST:
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO EL MATERIAL")
            return redirect('/listadomaterial')
        else:
            return render(request, 'materiales/material_edit.html', {"form": form})
    else:
        form = MaterialForm()
        return render(request, 'materiales/material_edit.html', {"form": form})


def editarmaterial(request, pk):
    consulta = Material.objects.get(pk=pk)
    if request.POST:
        form = MaterialForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO EL MATERIAL")
            return redirect('/listadomaterial')
        else:
            return render(request, 'materiales/material_edit.html', {"form": form})
    else:
        form = MaterialForm(instance=consulta)
        return render(request,
            'materiales/material_edit.html',
            {"form": form}
        )


def ajaxmaterial(request):
    parametro = request.GET.get('term')
    material = Material.objects.filter(descripcion__icontains=parametro)

    dict_tmp = dict()
    list_tmp = list()

    if len(material) > 0:
        for i in material:
            dict_tmp["id"] = i.pk
            dict_tmp["text"] = i.descripcion.upper()
            list_tmp.append(dict_tmp)
            dict_tmp = dict()

    return JsonResponse(list_tmp, safe=False)


@csrf_exempt
def ajaxgrabamaterial(request):
    material = request.POST["material"]

    try:
        grabamaterial = Material(descripcion=material)
        grabamaterial.save()
        respuesta={
            "status": 200,
            "descripcion": "Se ha grabado el material"
        }
    except:
        respuesta={
            "status": 500,
            "descripcion": "No se puede guardar el material"
        }

    return JsonResponse(respuesta, safe=False)


# Create your views here.
