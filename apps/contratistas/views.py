
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Contratista
from .forms import ContratistaForm


def listadocontratista(request):
    resultados = None
    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        resultados = Contratista.objects.filter(descripcion__icontains=parametro)

    return render(
        request,
        "contratistas/listadocontratista.html",
        {
            "resultados": resultados
        }
    )


def nuevocontratista(request):
    if request.POST:
        form = ContratistaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO LA CONTRATISTA")
            return redirect('/listadocontratista')
        else:
            return render(request, 'contratistas/contratista_edit.html', {"form": form})
    else:
        form = ContratistaForm()
        return render(request, 'contratistas/contratista_edit.html', {"form": form})


def editarcontratista(request, pk):
    consulta = Contratista.objects.get(pk=pk)
    if request.POST:
        form = ContratistaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO EL MATERIAL")
            return redirect('/listadocontratista')
        else:
            return render(request, 'contratistas/contratista_edit.html', {"form": form})
    else:
        form = ContratistaForm(instance=consulta)
        return render(request,
            'contratistas/contratista_edit.html',
            {"form": form}
        )


# Create your views here.
