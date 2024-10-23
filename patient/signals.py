import mimetypes
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from .models import Consulta, Document
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


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


@receiver(post_save, sender=Consulta)
def email_inicio_consulta(sender, instance, **kwargs):
    # Verifica se a consulta foi inicializada
    if instance.status == 'I' and instance.link:
        # Dados para o e-mail
        assunto = 'Sua consulta foi iniciada!'
        paciente_nome = instance.patient.user.first_name
        medico_nome = instance.available_time.available_date.doctor.perfil.user.first_name # noqa E501
        link_consulta = instance.link
        data_consulta = instance.available_time.available_date.date
        hora_consulta = instance.available_time.time

        # Renderiza o conteúdo HTML do e-mail
        conteudo_html = render_to_string(
            'emails/email_inicio_consulta.html',
            {
                'paciente': paciente_nome,
                'medico': medico_nome,
                'link': link_consulta,
                'data': data_consulta,
                'hora': hora_consulta,
            }
        )
        conteudo_texto = strip_tags(conteudo_html)

        # Endereços de e-mail do remetente e destinatário
        email_remetente = settings.EMAIL_HOST_USER
        email_destinatario = instance.patient.user.email

        # Cria o objeto EmailMultiAlternatives e envia o e-mail
        email = EmailMultiAlternatives(
            assunto, conteudo_texto, email_remetente, [email_destinatario]
        )
        email.attach_alternative(conteudo_html, 'text/html')
        email.send()


@receiver(post_save, sender=Document)
def email_documento_paciente(sender, instance, created, **kwargs):
    if created:
        consulta = instance.consulta
        paciente_email = consulta.patient.user.email

        # Dados para o e-mail
        assunto = 'Consulta médica documento disponível'
        paciente_nome = consulta.patient.user.first_name
        titulo_documento = instance.title

        # Renderiza o conteúdo HTML do e-mail
        conteudo_html = render_to_string(
            'emails/email_documento_paciente.html',
            {
                'paciente': paciente_nome,
                'documento': titulo_documento,
                'consulta': consulta,
            }
        )
        conteudo_texto = strip_tags(conteudo_html)

        # Cria o objeto EmailMultiAlternatives
        email = EmailMultiAlternatives(
            assunto, conteudo_texto, settings.EMAIL_HOST_USER, [paciente_email]
        )

        # Adiciona o documento como anexo, utilizando o mimetype correto
        if instance.document:
            file_path = instance.document.path
            mime_type, _ = mimetypes.guess_type(file_path)
            with open(file_path, 'rb') as doc_file:
                email.attach(instance.title, doc_file.read(), mime_type)

        # Envia o e-mail
        email.attach_alternative(conteudo_html, 'text/html')
        email.send(fail_silently=False)
