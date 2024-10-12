from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from patient.models import Consulta


@receiver(post_save, sender=Consulta)
def enviar_email_cancelamento_consulta(sender, instance, **kwargs):
    # Verifica se a consulta foi cancelada e o médico foi o responsável
    if instance.status == 'C' and instance.available_time.available_date.doctor.perfil == instance.available_time.available_date.doctor.perfil: # noqa E501

        # Assunto e template do e-mail
        assunto = 'Consulta Cancelada'

        # Renderiza o conteúdo HTML do e-mail
        conteudo_html = render_to_string(
            'emails/email_cancelamento_consulta.html',
            {
                'paciente': instance.patient.user.first_name,
                'medico': instance.available_time.available_date.doctor.perfil.user.first_name, # noqa E501
                'data': instance.available_time.available_date.date,
                'hora': instance.available_time.time,
            }
        )
        conteudo_texto = strip_tags(conteudo_html)

        # Endereços de email do remetente e destinatário
        email_remetente = settings.EMAIL_HOST_USER
        email_destinatario = instance.patient.user.email

        # Cria o objeto EmailMultiAlternatives e envia o e-mail
        email = EmailMultiAlternatives(
            assunto, conteudo_texto, email_remetente, [email_destinatario]
        )
        email.attach_alternative(conteudo_html, 'text/html')
        email.send()
