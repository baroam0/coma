
from django.db import models

from contratistas.models import Contratista


class Documentacion(models.Model):
    
    ESTADO_CHOICES = (
        ('T', 'En tramite'),
        ('P', 'Pagado'),
        ('N', 'Notificado'),
        ('A', 'Archivado'),
    )

    TIPO_CHOICES = (
        ('V', 'Varios'),
        ('M', 'Materiales'),
        ('C', 'Certificado'),
        ('A', 'Contrato o Alquiler'),
        ('P', 'Pago Servicios'),
    )

    estado = models.CharField(
        max_length=1,
        choices=ESTADO_CHOICES,
        default='T',
        null=True,
        blank=True
    )

    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CHOICES,
        default='V',
        null=True,
        blank=True
    )

    contratista = models.ForeignKey(
        Contratista, on_delete=models.CASCADE, null=True, blank=True)

    fechanota = models.DateField(null=True, blank=True)
    nota = models.CharField(
        max_length=10, unique=True, null=True, blank=True, default=None)

    fechaexpediente = models.DateField(null=True, blank=True)
    nomenclatura = models.CharField(max_length=100, unique=True, null=True, blank=True, default=None)
    descripcion = models.CharField(max_length=500,blank=True, null=True)

    monto = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)

    decreto = models.CharField(max_length=100, unique=True, null=True, blank=True, default=None)
    fechadecreto = models.DateField(null=True, blank=True)
    observaciones = models.CharField(max_length=5000, null=True, blank=True, default=None)


    
    def __str__(self):
        if self.nomenclatura and self.descripcion:
            return self.nomenclatura + "-" + self.descripcion
        else:
            return str(self.pk)


    class Meta:
        verbose_name_plural = "Documentaciones"


# Create your models here.
