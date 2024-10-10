from django.http import HttpResponse
from django.shortcuts import render
from contact.contact_form import FormContato
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from core import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def contato(request):
    return render(request, 'contact/contact.html', {'form': FormContato()})


def processa_contato(request):
    if request.method == 'POST':
        contato = FormContato(request.POST)
        print(contato)
        if contato.is_valid():
            try:
                # enviar_email(contato)
                enviar_email_template(contato)
                obj_contato = contato.save()
                obj_contato.save()
                messages.success(request, 'Mensagem encaminhada com sucesso!')
                return render(request, 'contact/contact.html', {'form': FormContato()}) # noqa E501
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
        else:
            return render(request, 'contact/contact.html', {'form': contato})

    return render(request, 'contact/contact.html', {'form': FormContato()})


def enviar_email(contato):
    send_mail(
        contato.cleaned_data['assunto'],
        contato.cleaned_data['mensagem'],
        settings.EMAIL_HOST_USER,
        [contato.cleaned_data['email']],
        fail_silently=False,
    )


def enviar_email_template(contato):
    # transformando conteúdo html em string
    html_content = render_to_string(
        'email_templates/confirmacao_mensagem.html',
        {'nome': contato.cleaned_data['nome'],
         'assunto': contato.cleaned_data['assunto']}
    )
    # removendo tags html do conteúdo de email
    text_content = strip_tags(html_content)

    # montando o email
    msg = EmailMultiAlternatives(
        contato.cleaned_data['assunto'],
        text_content,
        settings.EMAIL_HOST_USER,
        [contato.cleaned_data['email']]
    )

    # anexando código html/template ao email
    msg.attach_alternative(html_content, "text/html")

    # enviando o email
    msg.send()
