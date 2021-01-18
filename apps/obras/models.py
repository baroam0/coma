from django.db import models


class Obra(models.Model):
    descripcion = models.CharField(max_length=150, null=False, blank=False, unique=True)

    def __str__(self):
        return self.descripcion

    
    class Meta:
        verbose_name_plural = "Obras"

# Create your models here.
