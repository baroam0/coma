from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from .forms import CertificadoForm
from .models import Certificado


@login_required
def listar_certificados(request):
    resultados = Certificado.objects.none()
    return render(request, 'certificados/lista_certificados.html', {'results': resultados})


@login_required
def buscar_certificados(request):
    parametro = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    if parametro:
        certificados = Certificado.objects.select_related('expediente_madre').filter(
            Q(numero__icontains=parametro) |
            Q(descripcion__icontains=parametro) |
            Q(expediente_madre__nomenclatura__icontains=parametro) |
            Q(expediente_madre__descripcion__icontains=parametro) |
            Q(expediente_madre__contratista__descripcion__icontains=parametro)
        ).order_by("-fecha")
    else:
        certificados = Certificado.objects.none()

    paginator = Paginator(certificados, 500)
    page_obj = paginator.get_page(page_number)

    data = [
        {
            "id": e.pk,
            "fecha": e.fecha.strftime('%d/%m/%Y') if e.fecha else "",
            "numero": e.numero,
            "descripcion": e.descripcion or "",
            "monto": str(e.monto) if e.monto is not None else "",
            "expediente_madre": str(e.expediente_madre) if e.expediente_madre else "",
        } for e in page_obj
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
def crear_certificado(request):
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        if form.is_valid():
            certificado = form.save()
            messages.success(request, "Certificado grabado correctamente.")
            return redirect('editar_certificado', pk=certificado.id)
        else:
            messages.warning(request, "Hay errores en el formulario.")
    else:
        form = CertificadoForm()

    return render(request, 'certificados/crear_certificado.html', {
        'form': form, 'accion': 'Nuevo '})


@login_required
def editar_certificado(request, pk):
    certificado = get_object_or_404(Certificado, pk=pk)

    if request.method == 'POST':
        form = CertificadoForm(request.POST, instance=certificado)
        if form.is_valid():
            form.save()
            messages.success(request, "Certificado actualizado correctamente.")
            return redirect('editar_certificado', pk=pk)
        else:
            messages.warning(request, "Hay errores en el formulario.")
    else:
        form = CertificadoForm(instance=certificado)

    context = {
        'form': form,
        'accion': 'Editar ',
        'pk': pk
    }
    return render(request, 'certificados/crear_certificado.html', context)
