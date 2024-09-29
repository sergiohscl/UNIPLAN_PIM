from django.db import models
from accounts.models import Perfil


def is_medico(user):
    try:
        # Tenta acessar o perfil médico associado ao perfil do usuário
        perfil = Perfil.objects.get(user=user)
        return PerfilDoctor.objects.filter(perfil=perfil).exists()
    except Perfil.DoesNotExist:
        return False  # Caso o usuário não tenha um perfil associado


class Specialties(models.Model):
    specialty = models.CharField(max_length=100)
    icone = models.ImageField(upload_to="icones", null=True, blank=True)

    def __str__(self):
        return self.specialty


class PerfilDoctor(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    specialty = models.ForeignKey(
        Specialties, on_delete=models.CASCADE, null=True, blank=True
    )
    price = models.FloatField(default=100)
    crm = models.CharField(max_length=30)
    cpf = models.CharField(max_length=11, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.perfil.user.username} - Médico"


class AvailableDate(models.Model):
    doctor = models.ForeignKey(PerfilDoctor, on_delete=models.CASCADE)
    date = models.DateField()  # Data disponível
    scheduled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date)
