
import json

from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RemitoForm, DetalleRemitoForm
from .models import Remito, DetalleRemito
from documentaciones.models import Contratista, Documentacion
from materiales.models import Material, Unidad


@login_required
def listar_remitos(request):
    resultados = Remito.objects.order_by('-id')[:30]
    return render(request, 'remitos/lista_remitos.html', {'results': resultados})


@login_required
def buscar_remitos(request):
    parametro = request.GET.get('q', '')

    if parametro:

        resultados = Remito.objects.filter(
            Q(destinatario__nombre__icontains=parametro) |
            Q(textodestinatario__icontains=parametro) |
            Q(destino__descripcion__icontains=parametro) |
            Q(textodestino__icontains=parametro) |
            Q(detalleremito__material__descripcion__icontains=parametro)
        ).distinct().order_by('-id')
    else:
        resultados = Remito.objects.order_by('-fecha')[:50]

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
    if pk == 0:
        if request.method == "GET":
            unidades = list(Unidad.objects.values("id", "descripcion"))
            return JsonResponse({
                "unidades": unidades
            })

        if request.method == "POST":
            DetalleRemito.objects.create(
                remito_id=request.POST.get("remito"),
                material_id=request.POST.get("material"),
                unidad_id=request.POST.get("unidad"),
                cantidad=request.POST.get("cantidad")
            )
            return JsonResponse({"ok": True})
        return JsonResponse({"error": "Método no permitido"}, status=405)

    detalle = get_object_or_404(DetalleRemito, pk=pk)

    if request.method == "GET":
        unidades = list(Unidad.objects.values("id", "descripcion"))
        return JsonResponse({
            "id": detalle.id,
            "material": detalle.material.id,
            "material_text": detalle.material.descripcion,
            "unidad": detalle.unidad.id,
            "unidad_text": detalle.unidad.descripcion,
            "unidades": unidades,
            "cantidad": float(detalle.cantidad)
        })

    if request.method == "POST":
        detalle.material_id = request.POST.get("material")
        detalle.cantidad = request.POST.get("cantidad")
        if request.POST.get("remito"):
            detalle.remito_id = request.POST.get("remito")
        detalle.unidad_id = request.POST.get("unidad")
        detalle.save()
        return JsonResponse({"ok": True})
    return JsonResponse({"error": "Método no permitido"}, status=405)


def eliminar_detalle_remito(request, pk):
    if request.method == "POST":
        try:
            detalle = DetalleRemito.objects.get(pk=pk)
            detalle.delete()
            return JsonResponse({"ok": True})
        except DetalleRemito.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Detalle no encontrado"})
    return JsonResponse({"ok": False, "error": "Método no permitido"})


def imprimir_remito(request, remito_id):
    remito = get_object_or_404(Remito, pk=remito_id)
    detalles = DetalleRemito.objects.filter(remito=remito)

    return render(request, "remitos/imprimir_remito.html", {
        "remito": remito,
        "detalles": detalles
    })


@login_required
def reporte_materiales(request):
    fecha_desde = request.GET.get("desde")
    fecha_hasta = request.GET.get("hasta")
    destinatario_id = request.GET.get("destinatario")
    destino_id = request.GET.get("destino")

    qs = DetalleRemito.objects.select_related(
        "remito",
        "material"
    )

    if fecha_desde:
        qs = qs.filter(remito__fecha__gte=fecha_desde)

    if fecha_hasta:
        qs = qs.filter(remito__fecha__lte=fecha_hasta)

    if destinatario_id:
        qs = qs.filter(remito__destinatario_id=destinatario_id)

    if destino_id:
        qs = qs.filter(remito__destino_id=destino_id)

    reporte = qs.values(
        "remito__fecha",
        "material__descripcion",
        "remito__destinatario__descripcion",
        "remito__destino__descripcion",
        "remito__textodestino"
    ).annotate(
        total=Sum("cantidad")
    ).order_by("remito__fecha")

    if destinatario_id or destino_id:
        data = []
        for r in reporte:
            data.append({
                "fecha": r["remito__fecha"],
                "material": r["material__descripcion"],
                "total": float(r["total"]) if r["total"] else 0,
                "destinatario": r["remito__destinatario__descripcion"],
                "destino": r["remito__destino__descripcion"],
                "textodestino": r["remito__textodestino"],
            })

        return JsonResponse({"results": data})
    else:
        return render(request, "reportes/reporte_materiales.html", {
            "destinatarios": Contratista.objects.all(),
            "destinos": Documentacion.objects.all(),
        })


# Create your views here.

