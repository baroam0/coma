
import json

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import DocumentacionForm
from .models import Documentacion


@login_required
def listar_documentaciones(request):
    resultados = Documentacion.objects.none()
    return render(request, 'documentaciones/lista_documentacion.html', {'results': resultados})


@login_required
def buscar_documentaciones(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        documentaciones = Documentacion.objects.filter(
            Q(descripcion__icontains=parametro) |
            Q(nomenclatura__icontains=parametro) |
            Q(observaciones__icontains=parametro)
        ).order_by("descripcion")
    else:
        documentaciones = Documentacion.objects.none()

    paginator = Paginator(documentaciones, 500)
    page_obj = paginator.get_page(page_number)

    data = [
        {
            "id": p.pk,
            "nomenclatura": p.nomenclatura or "",
            "descripcion": p.descripcion or "",
            "tipo": p.get_tipo_display() or "",
            "estado": p.get_estado_display() or "",
        } for p in page_obj
    ]

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
def crear_documentacion(request):
    if request.method == 'POST':
        form = DocumentacionForm(request.POST)
        if form.is_valid():
            material=form.save()
            nuevo_id=material.id
            messages.success(request, "Material grabado correctamente.") 
            return redirect('editar_material', pk=nuevo_id)
    else:
        form = DocumentacionForm()

    return render(request, 'documentaciones/crear_documentacion.html', {
        'form': form, 'accion': 'Nueva '})


@login_required
def editar_documentacion(request, pk):
    documentacion = get_object_or_404(Documentacion, pk=pk)

    if request.method == 'POST':
        form = DocumentacionForm(request.POST, instance=documentacion)

        if form.is_valid():
            form.save()
            messages.success(request, "Documentacion actualizada correctamente.") 
            return redirect('/documentaciones/editar/' + str(pk))
        else:
            messages.error(request, "Hay errores en el formulario.") 
    
    else:
        form = DocumentacionForm(instance=documentacion)

    context = {
        'form': form,
        'accion': 'Editar ',
        'pk': pk
    }
    return render(request, 'documentaciones/crear_documentacionº.html', context)


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

