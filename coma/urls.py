"""coma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from .views import inicio
from apps.materiales.views import editarmaterial, listadomaterial, nuevomaterial
from apps.contratistas.views import editarcontratista, listadocontratista, nuevocontratista
from apps.ordenes.views import listadoorden, nuevaorden


urlpatterns = [
    path('', inicio),
    path('admin/', admin.site.urls),
    path('editarmaterial/<int:pk>', editarmaterial),
    path('listadomaterial/', listadomaterial),
    path('nuevomaterial/', nuevomaterial),

    path('editarcontratista/<int:pk>', editarcontratista),
    path('listadocontratista/', listadocontratista),
    path('nuevocontratista/', nuevocontratista),

    path('listadoorden/', listadoorden),
    path('nuevaorden/', nuevaorden),
]
