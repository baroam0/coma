

from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.listar_contratistas, name='listar_contratistas'),
    path('buscar', views.buscar_contratistas, name='buscar_contratistas'),
    path('crear/', views.crear_contratista, name='crear_contratista'),
    path('editar/<int:pk>', views.editar_contratista, name='editar_contratista'),
    #path('eliminar/<int:pk>', views.eliminar_paciente, name='eliminar_paciente'),
    #path('unificar/', views.unificar_paciente, name='unificar_paciente'),
    #path(
    #    'unificarbuscar', 
    #    views.unificar_buscar_pacientes, 
    #    name='unificar_buscar_pacientes'
    #),
    #path('unificarpaciente/', views.unificar_proceso_paciente, name='unificar_proceso_paciente'),
    #path('buscarpacienteturno', views.buscar_pacientes_tratamiento, name='buscar_pacientes_tratamiento'),
    #path('crearprecargar/<int:pk>', views.crear_paciente_precarga, name='crear_paciente_precarga'),
    #path('crearprecargar/<int:pk>', views.crear_paciente_precarga, name='crear_paciente_precarga'),
    #path("historiaclinica-ajax/", views.ajax_historia_clinica, name="ajax_historia_clinica"),
]
