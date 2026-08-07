

from django.urls import path
from . import views

from materiales.views import buscar_materiales

urlpatterns = [
    path('lista/', views.listar_remitos, name='listar_remitos'),
    path('buscar/', views.buscar_remitos, name='buscar_remitos'),
    path('buscarremitoajax', views.buscar_remitos, name='buscar_remitos'),
    path('crear/', views.crear_remito, name='crear_remito'),
    path('editar/<int:pk>', views.editar_remito, name='editar_remito'),
    path('ajaxdetalleremito/<int:pk>/', views.ajax_detalle_remito, name="ajax_detalle_remito"),
    path('eliminar-detalle/<int:pk>/', views.eliminar_detalle_remito, name='eliminar_detalle_remito'),
    path("buscar-materiales/", buscar_materiales, name="buscar_materiales"),
    path("imprimir/<int:remito_id>/", views.imprimir_remito, name="imprimir_remito"),
    path("imprimir/<int:remito_id>/", views.imprimir_remito, name="imprimir_remito"),
    path("reporte-materiales/", views.reporte_materiales, name="reporte_materiales"),
]
