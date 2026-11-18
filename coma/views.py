

import json
from datetime import datetime, time
from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core import signing
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


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


API_TOKEN_MAX_AGE = 60 * 60 * 24  # 24 horas
API_TOKEN_SALT = 'coma.api.token'


def generar_token(user):
    """Genera un token firmado (con fecha) que contiene el id del usuario."""
    return signing.dumps({'user_id': user.pk}, salt=API_TOKEN_SALT, compress=True)


def usuario_desde_token(token):
    """Devuelve el usuario del token, o None si es invalido, expiro o el usuario esta inactivo."""
    try:
        data = signing.loads(token, salt=API_TOKEN_SALT, max_age=API_TOKEN_MAX_AGE)
    except signing.BadSignature:  # incluye SignatureExpired
        return None
    return User.objects.filter(pk=data.get('user_id'), is_active=True).first()


def token_required(view_func):
    """Decorador para vistas de API: exige el header 'Authorization: Token <token>'."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        auth = request.headers.get('Authorization', '')
        tipo, _, token = auth.partition(' ')
        user = usuario_desde_token(token.strip()) if tipo == 'Token' else None
        if user is None:
            return JsonResponse({'error': 'Token invalido o expirado.'}, status=401)
        request.user = user
        return view_func(request, *args, **kwargs)
    return _wrapped


@csrf_exempt
@require_POST
def api_login(request):
    """
    POST /api/login/  {"username": "...", "password": "..."}  (JSON o form-data)
    Devuelve un token valido por API_TOKEN_MAX_AGE segundos.
    Usar luego en el header: Authorization: Token <token>
    """
    if request.content_type == 'application/json':
        try:
            datos = json.loads(request.body or b'{}')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON invalido.'}, status=400)
        if not isinstance(datos, dict):
            return JsonResponse({'error': 'JSON invalido.'}, status=400)
    else:
        datos = request.POST

    username = datos.get('username')
    password = datos.get('password')
    if not username or not password:
        return JsonResponse({'error': 'Debe enviar username y password.'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Usuario o clave invalida.'}, status=401)

    return JsonResponse({
        'token': generar_token(user),
        'expira_en': API_TOKEN_MAX_AGE,
        'user_id': user.pk,
        'username': user.username,
        'email': user.email,
    })


def salir(request):
    logout(request)
    return redirect('/login')


#@login_required(login_url='/login')
def muestrajornal(request):
    # Prototipo: los registros de horarios se manejan solo en memoria con JavaScript
    return render(request, 'muestrajornal.html')


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
