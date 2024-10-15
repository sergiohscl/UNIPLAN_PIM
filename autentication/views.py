from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Tente autenticar normalmente primeiro
            user = auth.authenticate(
                request, username=username, password=password
            )
            if user is None:
                # Se não encontrar por username, tente pelo email
                try:
                    user = User.objects.get(email=username)
                    user = auth.authenticate(
                        request, username=user.username, password=password
                    )
                except User.DoesNotExist:
                    pass
        except MultipleObjectsReturned:
            messages.error(request, "Username ou senha incorretos.")
            return render(
                request, 'autentication/login.html', {'username': username}
            )

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
