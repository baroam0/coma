

from django.db.models import Sum
from django.shortcuts import render


from apps.obras.models import Obra
from apps.ordenes.models import Orden, DetalleOrden


def listadomaterialporobra(request):
    obras = Obra.objects.all()
    return render(
        request,
        "reportes/listado_materialporobra.html",
        {
            "obras": obras
        }
    )

def reportematerialporobra(request, pk):
    obra = Obra.objects.get(pk=pk)
    orden = Orden.objects.filter(obra=obra.pk)
    detallesordenes = DetalleOrden.objects.filter(orden=orden)

    detallesordenes = DetalleOrden.objects.values('unidad__descripcion','material__descripcion').annotate(cant=Sum('cantidad')).order_by('material')
    

    print(detallesordenes)

    return render(
        request,
        "reportes/imprimirreportematerialporobra.html",
        {
            "detallesordenes": detallesordenes,
            "obra": obra
        }
    )

    

