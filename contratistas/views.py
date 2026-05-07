
import json

from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContratistaForm
from .models import Contratista


@login_required
def listar_contratistas(request):
    resultados = Contratista.objects.none()
    return render(request, 'contratistas/lista_contratistas.html', {'results': resultados})


@login_required
def buscar_contratistas(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        contratistas = Contratista.objects.filter(
            descripcion__icontains=parametro
        ).order_by("descripcion")
    else:
        contratistas = Contratista.objects.none()

    paginator = Paginator(contratistas, 250)
    page_obj = paginator.get_page(page_number)

    data = [{
        "id": p.pk,
        "descripcion": p.descripcion,
        "responsable": p.responsable or "",
        "domicilio": p.domicilio or ""
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
def crear_contratista(request):
    if request.method == 'POST':
        form = ContratistaForm(request.POST)
        if form.is_valid():
            contratista=form.save()
            nuevo_id=contratista.id
            messages.success(request, "Contratista grabado correctamente.") 
            return redirect('editar_contratista', pk=nuevo_id)
    else:
        form = ContratistaForm()

    return render(request, 'contratistas/crear_contratista.html', {
        'form': form, 'accion': 'Nuevo '})


@login_required
def editar_contratista(request, pk):
    contratista = get_object_or_404(Contratista, pk=pk)

    if request.method == 'POST':
        form = ContratistaForm(request.POST, instance=contratista)

        if form.is_valid():
            form.save()
            messages.success(request, "Contratista actualizado correctamente.") 
            return redirect('/contratistas/editar/' + str(pk))
        else:
            messages.error(request, "Hay errores en el formulario.") 
    
    else:
        form = ContratistaForm(instance=contratista)

    context = {
        'form': form,
        'accion': 'Editar',
        'pk': pk
    }
    return render(request, 'contratistas/crear_contratista.html', context)


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



# Create your views here.
