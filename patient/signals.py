from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from .models import Consulta


@receiver(post_save, sender=Consulta)
def update_consulta_status(sender, instance, **kwargs):
    agora = datetime.now()

    # Verifica a data e hora da consulta
    consulta_datetime = datetime.combine(
        instance.available_time.available_date.date,
        instance.available_time.time
    )

    # Atualiza o status se a consulta já passou
    if consulta_datetime < agora and instance.status == 'A':
        instance.status = 'F'  # Finalizada
        instance.save()
