from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Perfil
from accounts.usuario_form import PerfilForm
from .models import AvailableDate, PerfilDoctor, is_medico
from .forms import PerfilDoctorForm
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime


# View para criar ou atualizar PerfilDoctor
@login_required
def perfil_doctor_view(request):
    perfil = request.user.perfil

    try:
        perfil_doctor, created = PerfilDoctor.objects.get_or_create(perfil=perfil) # noqa E501
    except PerfilDoctor.DoesNotExist:
        perfil_doctor = None

    if request.method == "POST":
        form = PerfilDoctorForm(
            request.POST, request.FILES, instance=perfil_doctor
        )
        if form.is_valid():
            perfil_doctor = form.save(commit=False)
            perfil_doctor.perfil = perfil
            perfil_doctor.save()
            return redirect('perfil_doctor')
    else:
        form = PerfilDoctorForm(instance=perfil_doctor)

    return render(
        request, 'doctors/perfil_doctor_form.html',
        {
            'form': form,
            'is_medico': is_medico(request.user),
            'perfil_doctor': perfil_doctor
        }
    )


@login_required
def editar_perfil_doctor(request):
    # Obtém o perfil do usuário logado
    user = request.user
    try:
        perfil = Perfil.objects.get(user=user)
        perfil_doctor = PerfilDoctor.objects.get(perfil=perfil)
    except (Perfil.DoesNotExist, PerfilDoctor.DoesNotExist):
        messages.error(request, "Perfil ou perfil de médico não encontrado.")
        return redirect('home')

    if request.method == 'POST':
        # Instancia os formulários com os dados do POST e arquivos
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        perfil_doctor_form = PerfilDoctorForm(request.POST, instance=perfil_doctor) # noqa E501

        # Verifica se os formulários são válidos
        if perfil_form.is_valid() and perfil_doctor_form.is_valid():
            perfil_form.save()
            perfil_doctor_form.save()

            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('perfil_doctor')
        else:
            messages.error(request, "Houve um erro ao atualizar o perfil. Verifique os campos.") # noqa E501
    else:
        # Instancia os formulários com os dados do objeto existente
        perfil_form = PerfilForm(instance=perfil)
        perfil_doctor_form = PerfilDoctorForm(instance=perfil_doctor)

    return render(request, 'doctors/perfil_doctor_form.html', {
        'perfil_form': perfil_form,
        'perfil_doctor_form': perfil_doctor_form
    })


@login_required
def open_schedule(request):
    if not is_medico(request.user):
        messages.add_message(
            request, constants.WARNING,
            'Somente médicos podem acessar essa página.'
        )
        return redirect('home')

    # Obtendo o perfil do usuário logado
    perfil = Perfil.objects.get(user=request.user)

    if request.method == "GET":
        try:
            dados_medicos = PerfilDoctor.objects.get(perfil=perfil)
        except PerfilDoctor.DoesNotExist:
            messages.add_message(
                request, constants.ERROR,
                'Perfil de médico não encontrado.'
            )
            return redirect('home')

        datas_abertas = AvailableDate.objects.filter(doctor=dados_medicos)
        return render(
            request, 'doctors/open_schedule.html',
            {
                'dados_medicos': dados_medicos,
                'datas_abertas': datas_abertas,
                'is_medico': is_medico(request.user)
            }
        )
    elif request.method == "POST":
        data = request.POST.get('data')

        data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")

        if data_formatada <= datetime.now():
            messages.add_message(
                request, constants.WARNING,
                'A data deve ser maior ou igual a data atual.'
            )
            return redirect('/doctors/open_schedule')

        try:
            dados_medicos = PerfilDoctor.objects.get(perfil=perfil)
        except PerfilDoctor.DoesNotExist:
            messages.add_message(
                request, constants.ERROR,
                'Perfil de médico não encontrado.'
            )
            return redirect('home')

        horario_abrir = AvailableDate(
            date=data_formatada.date(),          
            doctor=dados_medicos,
            scheduled=False 
        )

        horario_abrir.save()

        messages.add_message(
            request, constants.SUCCESS, 'Horário cadastrado com sucesso.'
        )
        return redirect('/doctors/open_schedule')


# @login_required
# def open_schedule(request):

#     if not is_medico(request.user):
#         messages.add_message(
#             request, constants.WARNING,
#             'Somente médicos podem acessar essa página.'
#         )
#         return redirect('home')

#     if request.method == "GET":
#         dados_medicos = PerfilDoctor.objects.get(user=request.user)
#         datas_abertas = AvailableDate.objects.filter(user=request.user)
#         return render(
#             request, 'open_schedule.html',
#             {
#                 'dados_medicos': dados_medicos,
#                 'datas_abertas': datas_abertas,
#                 'is_medico': is_medico(request.user)
#             }
#         )
#     elif request.method == "POST":
#         data = request.POST.get('data')

#         data_formatada = datetime.strptime(data, "%Y-%m-%dT%H:%M")

#         if data_formatada <= datetime.now():
#             messages.add_message(
#                 request, constants.WARNING,
#                 'A data deve ser maior ou igual a data atual.'
#             )
#             return redirect('/doctors/open_schedule')

#         horario_abrir = AvailableDate(
#             data=data,
#             user=request.user
#         )

#         horario_abrir.save()

#         messages.add_message(
#             request, constants.SUCCESS, 'Horário cadastrado com sucesso.'
#         )
#         return redirect('/doctors/open_schedule')
