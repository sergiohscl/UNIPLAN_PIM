from django.db import models
from accounts.models import Perfil
from doctors.models import AvailableTime


class Consulta(models.Model):
    STATUS_CHOICES = (
        ('A', 'Agendada'),
        ('F', 'Finalizada'),
        ('C', 'Cancelada'),
        ('I', 'Iniciada'),
    )

    patient = models.ForeignKey(Perfil, on_delete=models.DO_NOTHING)
    available_time = models.ForeignKey(AvailableTime, on_delete=models.DO_NOTHING)  # Relaciona com o horário disponível # noqa E501
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')  # noqa E501
    link = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'consulta_patient'
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f"Consulta de {self.patient.user.username} em {self.available_time.available_date.date} às {self.available_time.time}" # noqa E501


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
