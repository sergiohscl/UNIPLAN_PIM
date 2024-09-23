# from django.shortcuts import render, redirect
# from django.contrib import messages, auth


# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = auth.authenticate(request, username=username, password=password) # noqa E501

#         if user is not None:
#             auth.login(request, user)
#             return redirect('home')
#         else:
#             context = {
#                 'username': username,
#                 'password': password
#             }
#             messages.add_message(
#                 request=request, message="Username ou senha incorretos.",
#                 level=messages.ERROR
#             )
#             return render(request, 'autentication/login.html', context)

#     return render(request, 'autentication/login.html')

from django.shortcuts import render, redirect
from django.contrib import messages, auth
# from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Autentica o usuário
            user = auth.authenticate(request, username=username, password=password) # noqa E501
        except MultipleObjectsReturned:
            # Se há múltiplos usuários com o mesmo username, exibe uma mensagem de erro # noqa E501
            messages.error(request, "Username ou senha incorretos.") # noqa E501
            return render(request, 'autentication/login.html', {'username': username}) # noqa E501

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context = {
                'username': username,
                'password': password
            }
            messages.add_message(
                request=request, message="Username ou senha incorretos.",
                level=messages.ERROR
            )
            return render(request, 'autentication/login.html', context)

    return render(request, 'autentication/login.html')


def processa_logout(request):

    # limpando mensagens do contexto antes do logout
    storage = messages.get_messages(request)
    for message in storage:
        pass

    auth.logout(request)
    return redirect('home')


def processa_redirect_home(request):
    return redirect('home')
