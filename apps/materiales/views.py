
from django.contrib import messages
from django.shortcuts import render, redirect

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


# Create your views here.
