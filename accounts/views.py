from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import re
from django.db import IntegrityError, transaction
from accounts.models import Perfil
from accounts.usuario_form import PerfilForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def validou_email(email):

    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' # noqa W605

    # Verifica se o email está no formato correto
    if re.match(regex, email):
        # Verifica se o email já está em uso
        if User.objects.filter(email=email).exists():
            return False, "Email já está em uso."
        return True, ""
    else:
        return False, "Email inválido."


def validou_senha(password):
    # Verifica o comprimento mínimo
    if len(password) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres."

    # Verifica se contém pelo menos uma letra maiúscula
    if not any(char.isupper() for char in password):
        return False, "A senha deve conter pelo menos uma letra maiúscula."

    # Verifica se contém pelo menos uma letra minúscula
    if not any(char.islower() for char in password):
        return False, "A senha deve conter pelo menos uma letra minúscula."

    # Verifica se contém pelo menos um dígito
    if not any(char.isdigit() for char in password):
        return False, "A senha deve conter pelo menos um número."

    # Verifica se contém pelo menos um caractere especial
    if not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password):
        return False, "A senha deve conter pelo menos um caractere especial."

    return True, ""


@transaction.atomic
def create_account(request):
    if request.method == 'POST':

        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST, request.FILES)

        if user_form.is_valid() and perfil_form.is_valid():

            email = user_form.cleaned_data['email']
            password = user_form.cleaned_data['password']

            # Valida o email
            email_valid, email_error = validou_email(email)
            if not email_valid:
                user_form.add_error('email', email_error)
                return render(
                    request, 'accounts/create_account.html',
                    {'form': user_form, 'form_perfil': perfil_form}
                )

            # Valida a senha
            password_valid, password_error = validou_senha(password)
            if not password_valid:
                user_form.add_error('password', password_error)
                return render(
                    request, 'accounts/create_account.html',
                    {'form': user_form, 'form_perfil': perfil_form}
                )

            # Cria o usuário
            try:
                usr = User.objects.create_user(
                    first_name=user_form.cleaned_data['first_name'],
                    last_name=user_form.cleaned_data['last_name'],
                    username=user_form.cleaned_data['username'],
                    email=user_form.cleaned_data['email'],
                    password=user_form.cleaned_data['password']
                )

                # Cria o perfil
                perfil, created = Perfil.objects.get_or_create(user=usr)
                perfil.foto = perfil_form.cleaned_data['foto']
                perfil.save()

                return redirect('login')

            except IntegrityError as e:
                if 'UNIQUE constraint failed: auth_user.username' in str(e):
                    user_form.add_error('username', "Este nome de usuário já está em uso. Por favor, escolha outro.") # noqa E501
                else:
                    user_form.add_error(None, "Ocorreu um erro inesperado. Por favor, tente novamente.") # noqa E501

        return render(request, 'accounts/create_account.html', {'form': user_form, 'form_perfil': perfil_form}) # noqa E501
    else:
        return render(request, 'accounts/create_account.html', {'form': UserForm(), 'form_perfil': PerfilForm()}) # noqa E501


# @login_required
# def edit_profile(request):
#     user = request.user
#     perfil = user.perfil  # Perfil associado ao usuário logado

#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=user)
#         perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil) # noqa E501

#         if user_form.is_valid() and perfil_form.is_valid():
#             user_form.save()
#             perfil_form.save()
#             messages.success(request, "Perfil atualizado com sucesso.")
#             return redirect('edit_profile')

#         else:
#             messages.error(
#                 request,
#                 "Houve um erro ao atualizar o perfil. Verifique os campos."
#             )

#     else:
#         user_form = UserForm(instance=user)
#         perfil_form = PerfilForm(instance=perfil)

#     return render(request, 'accounts/edit_profile.html', {
#         'user_form': user_form,
#         'perfil_form': perfil_form
#     })

@login_required
def edit_profile(request):
    user = request.user
    perfil = user.perfil  # Perfil associado ao usuário logado

    if request.method == 'POST':
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)

        if perfil_form.is_valid():
            perfil_form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('edit_profile')

        else:
            messages.error(
                request,
                "Houve um erro ao atualizar o perfil. Verifique os campos."
            )

    else:
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'accounts/edit_profile.html', {
        'perfil_form': perfil_form
    })
