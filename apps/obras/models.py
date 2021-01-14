from django.db import models


class Obra(models.Model):
    descripcion = models.CharField(max_length=150, null=False, blank=False, unique=True)

    def __str__(self):
        return self.descripcion.upper()




# Create your models here.