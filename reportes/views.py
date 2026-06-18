from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse

from .models import Remito, DetalleRemito, Contratista, Documentacion
from openpyxl import Workbook


def reporte_materiales(request):
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")
    destino_id = request.GET.get("destino")
    destinatario_id = request.GET.get("destinatario")
    export = request.GET.get("export")

    filtros = {}

    if fecha_desde:
        filtros["remito__fecha__gte"] = fecha_desde

    if fecha_hasta:
        filtros["remito__fecha__lte"] = fecha_hasta

    if destino_id:
        filtros["remito__destino_id"] = destino_id

    if destinatario_id:
        filtros["remito__destinatario_id"] = destinatario_id

    resultados = (
        DetalleRemito.objects
        .filter(**filtros)
        .values("material__descripcion")
        .annotate(total=Sum("cantidad"))
        .order_by("material__descripcion")
    )

    # -------------------------
    # EXPORTACIÓN A EXCEL
    # -------------------------
    if export == "excel":
        wb = Workbook()
        ws = wb.active
        ws.title = "Reporte Materiales"

        ws.append(["Material", "Total utilizado"])

        for item in resultados:
            ws.append([
                item["material__descripcion"],
                float(item["total"]) if item["total"] else 0
            ])

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=reporte_materiales.xlsx"
        wb.save(response)
        return response

    # Vista normal
    context = {
        "resultados": resultados,
        "destinos": Documentacion.objects.all(),
        "destinatarios": Contratista.objects.all(),
    }

    return render(request, "reporte_materiales.html", context)


# Create your views here.
