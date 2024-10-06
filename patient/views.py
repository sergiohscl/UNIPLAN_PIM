from datetime import datetime
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from doctors.models import (
    AvailableDate, PerfilDoctor, Specialties
)
from django.contrib.messages import constants
from django.contrib import messages
from patient.models import Consulta


@login_required
def marcar_consulta(request):
    specialty_id = request.GET.get('specialty')
    selected_specialty = None
    doctors = None
    available_dates = {}

    if specialty_id:
        selected_specialty = get_object_or_404(Specialties, id=specialty_id)
        doctors = PerfilDoctor.objects.filter(specialty=selected_specialty)

        for doctor in doctors:
            available_dates[doctor.id] = AvailableDate.objects.filter(
                doctor=doctor, scheduled=False
            )

    # Processa o formulário de agendamento
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        selected_date_id = request.POST.get(f'selected_date_{doctor_id}')
        selected_time_str = request.POST.get(f'selected_time_{doctor_id}')

        if selected_date_id and selected_time_str:
            try:
                # Recupera a data disponível
                selected_date = AvailableDate.objects.get(id=selected_date_id)
                selected_time = datetime.strptime(
                    selected_time_str, '%H:%M'
                ).time()

                # Cria a consulta
                Consulta.objects.create(
                    patient=request.user.perfil,
                    available_date=selected_date,
                    available_time=selected_time,
                    status='A'
                )

                # Marcar a data como agendada
                selected_date.scheduled = True
                selected_date.save()

                # Mensagem de sucesso
                messages.add_message(request, constants.SUCCESS, f"Consulta agendada com o Dr. {selected_date.doctor.perfil.user.first_name} com sucesso!") # noqa E501
                return redirect('my_queries')

            except AvailableDate.DoesNotExist:
                messages.add_message(
                    request, constants.ERROR, "Data inválida."
                )
                return redirect('marcar_consulta')

    specialties = Specialties.objects.all()

    context = {
        'specialties': specialties,
        'selected_specialty': selected_specialty,
        'doctors': doctors,
        'available_dates': available_dates,
    }

    return render(request, 'patient/marcar_consulta.html', context)


@login_required
def my_queries(request):
    # Busca todas as consultas do paciente logado
    consultas = Consulta.objects.filter(
        patient=request.user.perfil
    ).order_by('available_date__date')

    context = {
        'consultas': consultas
    }

    return render(request, 'patient/my_queries.html', context)
