

from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.listar_remitos, name='listar_remitos'),
    path('buscar/', views.buscar_remitos, name='buscar_remitos'),
    path('crear/', views.crear_remito, name='crear_remito'),
    #path('editar/<int:pk>', views.editar_material, name='editar_material'),
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
