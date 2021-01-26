

from django.db.models import Count, Sum
from django.shortcuts import render

from apps.contratistas.models import Contratista
from apps.obras.models import Obra
from apps.ordenes.models import Orden, DetalleOrden


def listadomaterialporcooperativa(request):
    contratistas = Contratista.objects.all()
    return render(
        request,
        "reportes/listado_materialporcooperativa.html",
        {
            "contratistas": contratistas
        }
    )

def listadomaterialporobra(request):
    obras = Obra.objects.all()
    return render(
        request,
        "reportes/listado_materialporobra.html",
        {
            "obras": obras
        }
    )


def reportematerialporcooperativa(request, pk):
    contratista = Contratista.objects.get(pk=pk)
    orden = Orden.objects.filter(contratista=contratista.pk)
    detallesordenes = DetalleOrden.objects.filter(
        orden__in=orden).values(
            'orden__obra__descripcion', 'material__descripcion', 'unidad__descripcion').annotate(cant=Sum('cantidad'))

    return render(
        request,
        "reportes/imprimirreportematerialporcooperativa.html",
        {
            "contratista": contratista,
            "detallesordenes": detallesordenes,
        }
    )


def reportematerialporobra(request, pk):
    obra = Obra.objects.get(pk=pk)
    orden = Orden.objects.filter(obra=obra.pk)
    detallesordenes = DetalleOrden.objects.filter(orden=orden).exclude(faltante=True)

    detallesordenes = DetalleOrden.objects.filter(
        orden__in=orden).exclude(faltante=True).values(
            'unidad__descripcion','material__descripcion').annotate(
                cant=Sum('cantidad')).order_by('material')
    
    return render(
        request,
        "reportes/imprimirreportematerialporobra.html",
        {
            "detallesordenes": detallesordenes,
            "obra": obra
        }
    )
