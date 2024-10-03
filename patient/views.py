from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from doctors.models import AvailableDate, PerfilDoctor, Specialties, is_medico
from django.contrib.messages import constants
from django.contrib import messages

from patient.models import Consulta, Document


@login_required
def choose_time(request, id_dados_medicos):
    if request.method == "GET":
        medico = PerfilDoctor.objects.get(id=id_dados_medicos)
        available_date = AvailableDate.objects.filter(
            user=medico.perfil.user
        ).filter(data__gte=datetime.now()).filter(scheduled=False)
        return render(
            request, 'escolher_horario.html',
            {
                'medico': medico,
                'datas_abertas': available_date,
                'is_medico': is_medico(request.user)
            }
        )


@login_required
def schedule_time(request, id_data_aberta):
    if request.method == "GET":
        available_date = AvailableDate.objects.get(id=id_data_aberta)

        scheduled_time = Consulta(
            patient=request.user,
            available_date=available_date
        )

        scheduled_time.save()

        available_date.scheduled = True
        available_date.save()

        messages.add_message(
            request, constants.SUCCESS, 'Cosnulta agendada com sucesso.'
        )

        return redirect('patient/my_queries/')


@login_required
def my_queries(request):
    data = request.GET.get("data")
    specialty = request.GET.get("specialty")

    my_queries = Consulta.objects.filter(
        paciente=request.user
    ).filter(available_date__data__gte=datetime.now())

    if data:
        my_queries = my_queries.filter(data_aberta__data__gte=data)

    if specialty:
        my_queries = my_queries.filter(
            available_date__user__perfil_doctor__specialty__id=specialty
        )

    specialty = Specialties.objects.all()
    return render(
        request, 'my_queries.html',
        {
            'my_queries': my_queries,
            'specialty': specialty,
            'is_medico': is_medico(request.user)
        }
    )


@login_required
def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = PerfilDoctor.objects.get(user=consulta.data_aberta.user)
        documentos = Document.objects.filter(consulta=consulta)
        return render(
            request, 'consulta.html',
            {
                'consulta': consulta,
                'dado_medico': dado_medico,
                'documentos': documentos
            }
        )


@login_required
def cancel_consulta(request, id_consulta):
    consulta = Consulta.objects.get(id=id_consulta)
    if request.user != consulta.patient:
        messages.add_message(
            request, constants.ERROR, 'Essa consulta não é sua!'
        )
        return redirect('home')

    consulta.status = 'C'
    consulta.save()
    return redirect(f'/pactent/consulta/{id_consulta}')
