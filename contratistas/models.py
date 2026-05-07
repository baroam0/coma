from django.db import models


class Contratista(models.Model):
    descripcion = models.CharField(max_length=250, unique=True, blank=True)
    responsable = models.CharField(
        max_length=250, unique=True, blank=True, null=True
    )
    responsabledni = models.IntegerField(blank=True)
    domicilio = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Contratistas"


# Create your models here.
