from django.db import models


class Material(models.Model):
    descripcion = models.CharField(
        max_length=500,unique=True, blank=False, null=False
        )

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Materiales"


class Unidad(models.Model):
    descripcion = models.CharField(
        max_length=500,unique=True, blank=False, null=False
        )

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Unidades"


# Create your models here.
