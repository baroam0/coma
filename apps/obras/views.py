
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import ObraForm
from .models import Obra


def listadoobra(request):
    resultados = None

    if "txtBuscar" in request.GET:
        parametro = request.GET.get("txtBuscar")
        resultados = Obra.objects.filter(descripcion__icontains=parametro)

    return render(
        request,
        "obras/listadoobra.html",
        {
            "resultados": resultados
        }
    )


def nuevaobra(request):
    if request.POST:
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA GRABADO LA OBRA")
            return redirect('/listadoobra')
        else:
            return render(request, 'obras/obra_edit.html', {"form": form})
    else:
        form = ObraForm()
        return render(request, 'obras/obra_edit.html', {"form": form})


def editarobra(request, pk):
    consulta = Obra.objects.get(pk=pk)
    if request.POST:
        form = ObraForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "SE HA ACTUALIZADO LA OBRA")
            return redirect('/listadoobra')
        else:
            return render(request, 'obras/obra_edit.html', {"form": form})
    else:
        form = ObraForm(instance=consulta)
        return render(request,
            'obras/obra_edit.html',
            {"form": form}
        )

# Create your views here.
