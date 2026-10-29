from django.db import models

from documentaciones.models import Documentacion


class Certificado(models.Model):

    fecha = models.DateField(null=True, blank=True)
    numero = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    monto = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)

    # Solo documentaciones de tipo 'Contrato o Alquiler'
    expediente_madre = models.ForeignKey(
        Documentacion,
        on_delete=models.PROTECT,
        limit_choices_to={'tipo': 'A'},
        related_name='certificados',
        null=True,
        blank=True
    )

    def __str__(self):
        if self.descripcion:
            return self.numero + "-" + self.descripcion
        return self.numero

    class Meta:
        verbose_name_plural = "Certificados"
