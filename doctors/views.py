from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Perfil
from accounts.usuario_form import PerfilForm
from patient.models import Consulta
from .models import (
    AvailableDate, AvailableTime, PerfilDoctor, Specialties, is_medico
)
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
        horario = request.POST.get('horario')

        if not data or not horario:
            messages.add_message(
                request, constants.WARNING,
                'Data e horário são obrigatórios.'
            )
            return redirect('/doctors/open_schedule')

        data_formatada = datetime.strptime(data, "%Y-%m-%d")
        horario_formatado = datetime.strptime(horario, "%H:%M").time()

        # Validar se a data é maior ou igual à data atual
        if data_formatada.date() < datetime.now().date():
            messages.add_message(
                request, constants.WARNING,
                'A data deve ser maior ou igual à data atual.'
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

        # Cria ou obtém a data disponível
        horario_abrir, created = AvailableDate.objects.get_or_create(
            date=data_formatada.date(), doctor=dados_medicos
        )

        # Verifica se o horário já está cadastrado
        if AvailableTime.objects.filter(
            available_date=horario_abrir, time=horario_formatado
        ).exists():
            messages.add_message(
                request, constants.WARNING,
                f'Já existe um horário cadastrado para {data_formatada.strftime("%d/%m/%Y")} às {horario_formatado}.' # noqa E501
            )
            return redirect('/doctors/open_schedule')

        # Cria o horário específico para a data
        AvailableTime.objects.create(
            available_date=horario_abrir,
            time=horario_formatado,
            scheduled=False
        )

        messages.add_message(
            request, constants.SUCCESS,
            f'Horário cadastrado com sucesso para {data_formatada.strftime("%d/%m/%Y")} às {horario_formatado}.'  # noqa E501
        )
        return redirect('/doctors/open_schedule')


def list_doctor_specialty(request, specialty):
    # Busca a especialidade pelo nome
    specialty_obj = get_object_or_404(Specialties, specialty=specialty)

    # Filtra os médicos com essa especialidade
    medicos = PerfilDoctor.objects.filter(specialty=specialty_obj)

    # Renderiza o template com os médicos filtrados
    return render(
        request,
        'doctors/list_doctor_specialty.html',
        {'medicos': medicos, 'specialty': specialty_obj.specialty}
    )


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(PerfilDoctor, id=doctor_id)

    return render(
        request,
        "doctors/doctor_detail.html",
        {'medico': doctor}
    )


@login_required
def doctor_queries(request):
    if not is_medico(request.user):
        messages.warning(request, "Somente médicos podem acessar essa página.")
        return redirect('home')

    # Obtém o perfil e o perfil de médico do usuário logado
    perfil = Perfil.objects.get(user=request.user)
    try:
        perfil_doctor = PerfilDoctor.objects.get(perfil=perfil)
    except PerfilDoctor.DoesNotExist:
        messages.error(request, "Perfil de médico não encontrado.")
        return redirect('home')

    # Filtra as consultas marcadas para as datas disponíveis do médico
    consultas = Consulta.objects.filter(available_time__available_date__doctor=perfil_doctor) # noqa E501

    return render(
        request,
        'doctors/doctor_queries.html',
        {
            'consultas': consultas,
            'is_medico': True
        }
    )
