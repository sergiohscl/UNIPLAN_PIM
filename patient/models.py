from django.db import models
from accounts.models import Perfil
from doctors.models import AvailableDate


class Consulta(models.Model):
    status_choices = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada')

    )
    patient = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    available_date = models.ForeignKey(AvailableDate, on_delete=models.DO_NOTHING) # noqa E501
    available_time = models.TimeField()
    status = models.CharField(max_length=1, choices=status_choices, default='A') # noqa E501
    link = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'consulta_patient'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return self.patient.user.username


class Document(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=30)
    document = models.FileField(upload_to='documentos')

    class Meta:
        db_table = 'document'
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return self.title
