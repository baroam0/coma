
import json

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import MaterialForm
from .models import Material


@login_required
def listar_materiales(request):
    resultados = Material.objects.none()
    return render(request, 'materiales/lista_material.html', {'results': resultados})


@login_required
def buscar_materiales(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        pacientes = Material.objects.filter(
            descripcion__icontains=parametro
        ).order_by("descripcion")
    else:
        pacientes = Material.objects.none()

    paginator = Paginator(pacientes, 1000)
    page_obj = paginator.get_page(page_number)

    data = [{
        "id": p.pk,
        "descripcion": p.descripcion
    } for p in page_obj]

    return JsonResponse({
        "results": data,
        "page": page_obj.number,
        "total_pages": paginator.num_pages,
        "has_next": page_obj.has_next(),
        "has_previous": page_obj.has_previous(),
        "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
        "prev_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
    })


@login_required
def crear_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            material=form.save()
            nuevo_id=material.id
            messages.success(request, "Material grabado correctamente.") 
            return redirect('editar_material', pk=nuevo_id)
    else:
        form = MaterialForm()

    return render(request, 'materiales/crear_material.html', {
        'form': form, 'accion': 'Nuevo '})


@login_required
def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)

    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)

        if form.is_valid():
            form.save()
            messages.success(request, "Material actualizado correctamente.") 
            return redirect('/materiales/editar/' + str(pk))
        else:
            messages.error(request, "Hay errores en el formulario.") 
    
    else:
        form = MaterialForm(instance=material)

    context = {
        'form': form,
        'accion': 'Editar',
        'pk': pk
    }
    return render(request, 'materiales/crear_material.html', context)


"""
@login_required
def eliminar_paciente(request, pk):
    paciente = Paciente.objects.get(pk=pk)
    historiaclinica = HistoriaClinica.objects.filter(paciente=paciente)

    if request.method == "POST":
        historiaclinica.delete()
        paciente.delete()
        return redirect(
            reverse(
                "listar_pacientes"
            )
        )

    return render(
        request, 
        "pacientes/eliminar_paciente.html", 
        {
            "historiaclinica": historiaclinica,
            "paciente": paciente
        }
    )
"""


# Create your views here.
