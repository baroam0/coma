from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.listar_certificados, name='listar_certificados'),
    path('buscar', views.buscar_certificados, name='buscar_certificados'),
    path('crear/', views.crear_certificado, name='crear_certificado'),
    path('editar/<int:pk>', views.editar_certificado, name='editar_certificado'),
]
