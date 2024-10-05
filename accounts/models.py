import random
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Perfil(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'M', 'Masculino'
        FEMININO = 'F', 'Feminino'
        OUTRO = 'O', 'Outro'

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True
    )
    foto = models.ImageField(
        blank=True, null=True, default='', upload_to='contas/imagens'
    )
    cpf = models.CharField(max_length=11, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    telefone = models.CharField(max_length=19)
    sexo = models.CharField(
        max_length=1,
        choices=Sexo.choices,
        default='',
        blank=True,
        null=True
    )
    data_nasc = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        cpf = gerar_cpf_unico()
        Perfil.objects.create(user=instance, cpf=cpf)


@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()


def gerar_cpf_unico():
    while True:
        # Gera um número de CPF com 11 dígitos
        cpf = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        # Verifica se já existe algum perfil com este CPF
        if not Perfil.objects.filter(cpf=cpf).exists():
            return cpf
