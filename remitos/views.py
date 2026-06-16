
import json

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RemitoForm, DetalleRemitoForm
from .models import Remito, DetalleRemito
from materiales.models import Material


@login_required
def listar_remitos(request):
    resultados = Remito.objects.order_by('-id')[:30]
    return render(request, 'remitos/lista_remitos.html', {'results': resultados})


@login_required
def buscar_remitos(request):
    parametro = request.GET.get('q', '')

    if parametro:
        resultados = Remito.objects.filter(
            descripcion__icontains=parametro
        ).order_by("descripcion")
    else:
        resultados = Remito.objects.order_by('-id')[:30]

    data = list()
    tmpdict = dict()

    for r in resultados:
        tmpdict = {
            "id": r.pk,
            "descripcion": r.descripcion
        } 

    return JsonResponse({
        "results": data,
    })


@login_required
def crear_remito(request):
    if request.method == 'POST':
        form = RemitoForm(request.POST)
        if form.is_valid():
            material=form.save()
            nuevo_id=material.id
            messages.success(request, "Remito  grabado correctamente.") 
            return redirect('editar_remito', pk=nuevo_id)
    else:
        form = RemitoForm()

    return render(request, 'remitos/crear_remito.html', {
        'form': form, 'accion': 'Nuevo '})


@login_required
def editar_remito(request, pk):
    remito = get_object_or_404(Remito, pk=pk)
    detallesremito = DetalleRemito.objects.filter(remito=remito)

    if request.method == 'POST':
        form = RemitoForm(request.POST, instance=remito)
        if form.is_valid():
            form.save()
            messages.success(request, "Remito actualizado correctamente.") 
            return redirect('/remitos/editar/' + str(pk))
        else:
            messages.error(request, "Hay errores en el formulario.") 
    
    else:
        form = RemitoForm(instance=remito)

    context = {
        'form': form,
        'detallesremito': detallesremito,
        'accion': 'Editar',
        'pk': pk
    }
    return render(request, 'remitos/crear_remito.html', context)


def ajax_detalle_remito(request, pk):
    detalle = get_object_or_404(DetalleRemito, pk=pk)

    if request.method == "GET":
        #materiales = list(Material.objects.values("id", "descripcion"))
        materiales = list(Material.objects.values("id", "descripcion"))
        return JsonResponse({
            "id": detalle.id,
            "material": detalle.material.id,
            "cantidad": float(detalle.cantidad),
            "materiales": materiales
        })

    # POST → guardar cambios
    if request.method == "POST":
        detalle.material_id = request.POST.get("material")
        detalle.cantidad = request.POST.get("cantidad")
        detalle.save()

        return JsonResponse({"ok": True})

    return JsonResponse({"error": "Método no permitido"}, status=405)




# Create your views here.

