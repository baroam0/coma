

from datetime import datetime, time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone


@login_required(login_url='/login')
def home(request):
    anio_actual = datetime.now().year    
    return render(
        request, 
        'base.html', 
        {
            'anio_actual': anio_actual
        }
    )


def loginusuario(request):
    if request.POST:
        acceso = authenticate(
            username=request.POST['input-usuario'],
            password=request.POST['input-clave']
        )

        if acceso is not None:
            login(request, acceso)
            return redirect('/')
        else:
            mensaje = "Usuario o Clave invalida."
            return render(
                request,
                'login.html',
                {
                    'mensaje': mensaje,
                })
    else:
        return render(request, 'login.html')


def salir(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def modal_data(request):
    hoy = timezone.localdate()
    inicio_hoy = timezone.make_aware(datetime.combine(hoy, time.min))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, time.max))

    categorias = Categoria.objects.filter(excluirreporte=True)

    ingresoshoy = Ingreso.objects.filter(
        fecha__range=(inicio_hoy, fin_hoy),
        categoria__in=categorias
    ).order_by("-fecha")

    tmpingresoshoylist = list()
    tmpingresoshoydict = dict()

    totalingresos = 0
    totalegresos = 0
    total = 0

    for i in ingresoshoy:
        if i.monto > 0:
            tmpingresoshoydict = {
                "id": i.id,
                "fecha": i.fecha,
                "descripcion": i.descripcion,
                "monto": i.monto,
                "esingreso": True,
                "categoria": i.categoria or ""
            }
            tmpingresoshoylist.append(tmpingresoshoydict)
            tmpingresoshoydict = dict()
            totalingresos = totalingresos + i.monto
        else:
            tmpingresoshoydict = {
                "id": i.id,
                "fecha": i.fecha,
                "descripcion": i.descripcion,
                "monto": i.monto,
                "esingreso": False,
                "categoria": i.categoria or ""
            }
            tmpingresoshoylist.append(tmpingresoshoydict)
            tmpingresoshoydict = dict()
            totalegresos = totalegresos + i.monto
    
    total = totalingresos - totalegresos

    return render(request, "modal_content.html", {
        "ingresoshoy": tmpingresoshoylist,
        "totalingresos": totalingresos, 
        "totalegresos": totalegresos, 
        "total": total
    })
    

@login_required
def modal_ingreso(request):
    if request.method == "POST":
        form = IngresoForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.usuario = request.user
            ingreso.save()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "errors": form.errors})

    else:
        form = IngresoForm()
        return render(request, "modal_contentingresos.html", {"form": form})
