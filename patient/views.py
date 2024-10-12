from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from doctors.models import (
    AvailableDate, AvailableTime, PerfilDoctor, Specialties
)
from django.contrib.messages import constants
from django.contrib import messages
from patient.models import Consulta
from django.utils import timezone


@login_required
def marcar_consulta(request):
    print(f"Tipo de request: {type(request)}")
    specialty_id = request.GET.get('specialty')
    selected_specialty = None
    doctors = None
    available_times = {}  # Armazena horários disponíveis
    available_dates = {}  # Armazena as datas disponíveis para cada médico

    if specialty_id:
        selected_specialty = get_object_or_404(Specialties, id=specialty_id)
        doctors = PerfilDoctor.objects.filter(specialty=selected_specialty)

        # Obter as datas e horários disponíveis para cada médico
        for doctor in doctors:
            available_dates[doctor.id] = AvailableDate.objects.filter(
                doctor=doctor, scheduled=False
            )
            # Associar horários a cada data disponível
            available_times[doctor.id] = {
                date.id: AvailableTime.objects.filter(
                    available_date=date, scheduled=False
                )
                for date in available_dates[doctor.id]
            }

    # Processar o formulário de agendamento
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        selected_date_id = request.POST.get(f'selected_date_{doctor_id}')
        selected_time_id = request.POST.get(f'selected_time_{doctor_id}')

        if selected_date_id and selected_time_id:
            try:
                # Recupera a data e horário disponíveis
                selected_date = AvailableDate.objects.get(id=selected_date_id)
                selected_time = AvailableTime.objects.get(id=selected_time_id)

                # Criar a consulta
                Consulta.objects.create(
                    patient=request.user.perfil,
                    available_time=selected_time,
                    status='A'
                )

                # Marcar a data e horário como agendados
                selected_time.scheduled = True
                selected_time.save()

                # Mensagem de sucesso
                messages.add_message(
                    request,
                    constants.SUCCESS,
                    f"Consulta agendada com o Dr. {
                        selected_date.doctor.perfil.user.first_name
                    } com sucesso!"
                )
                return redirect('marcar_consulta')

            except (AvailableDate.DoesNotExist, AvailableTime.DoesNotExist):
                messages.add_message(
                    request, constants.ERROR, "Data ou horário inválido."
                )
                return redirect('marcar_consulta')

    specialties = Specialties.objects.all()

    context = {
        'specialties': specialties,
        'selected_specialty': selected_specialty,
        'doctors': doctors,
        'available_dates': available_dates,
        'available_times': available_times,
    }

    return render(request, 'patient/marcar_consulta.html', context)


@login_required
def my_queries(request):
    # Pega a data e o horário atual
    current_time = timezone.now()

    # Filtra as consultas do paciente e exibe as que ainda não ocorreram
    consultas = Consulta.objects.filter(
        patient=request.user.perfil,
        available_time__available_date__date__gte=current_time.date(),
    ).order_by('available_time__available_date__date')

    context = {
        'consultas': consultas
    }

    return render(request, 'patient/my_queries.html', context)


@login_required
def cancelar_consulta(request, consulta_id):
    # Pega a consulta com o id fornecido
    consulta = get_object_or_404(Consulta, id=consulta_id)

    # Verifica se o usuário é o paciente associado à consulta
    if consulta.patient == request.user.perfil:
        # Atualiza o status da consulta para 'Cancelada'
        consulta.status = 'C'
        consulta.save()

        messages.add_message(
            request, constants.SUCCESS, "Consulta cancelada com sucesso."
        )
    else:
        messages.add_message(
            request,
            constants.ERROR,
            "Você não tem permissão para cancelar esta consulta."
        )

    return redirect('my_queries')
