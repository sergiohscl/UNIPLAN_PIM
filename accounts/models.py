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
    sexo = models.CharField(
        max_length=1,
        choices=Sexo.choices,
        default='',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def salvar_perfil_usuario(sender, instance, **kwargs):
    instance.perfil.save()
