
import datetime
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
            'orden__obra__descripcion',
            'material__descripcion',
            'unidad__descripcion').annotate(cant=Sum('cantidad'))

    return render(
        request,
        "reportes/imprimirreportematerialporcooperativa.html",
        {
            "contratista": contratista,
            "detallesordenes": detallesordenes,
        }
    )


def reportematerialporobra(request):

    if request.is_ajax():
        fechadesde = request.GET["fechadesde"]
        fechahasta = request.GET["fechahasta"]
        idobra = request.GET["idobra"]

        obra = Obra.objects.get(pk=int(idobra))
        
        listfechadesde = fechadesde.split("/")
        listfechahasta = fechahasta.split("/")

        orden = Orden.objects.filter(
            obra=obra.pk,
            fecha__gte=datetime.date(int(listfechadesde[2]), int(listfechadesde[1]), int(listfechadesde[0])),
            fecha__lte=datetime.date(int(listfechahasta[2]), int(listfechahasta[1]), int(listfechahasta[0])))

        detallesordenes = DetalleOrden.objects.filter(
            orden__in=orden).exclude(faltante=True).values(
                'unidad__descripcion','material__descripcion').annotate(cant=Sum('cantidad')).order_by('material')
        return render(
            request,
            "reportes/imprimirreportematerialporobra.html",
            {
                "detallesordenes": detallesordenes,
                "obra": obra
            }
        )


    """
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
    """
