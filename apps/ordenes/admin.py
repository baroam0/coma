from django.contrib import admin

from .models import DetalleOrden, Orden, Unidad

admin.site.register(DetalleOrden)
admin.site.register(Orden)
admin.site.register(Unidad)


# Register your models here.
