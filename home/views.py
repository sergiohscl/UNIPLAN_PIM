from django.shortcuts import render
from doctors.models import PerfilDoctor


def home(request):
    medicos = PerfilDoctor.objects.all()[:6]
    medicos_grouped = list(group_queryset(medicos, 3))
    return render(request, 'home/home_live.html', {'medicos_grouped': medicos_grouped}) # noqa E501


def group_queryset(queryset, n):
    """Agrupa a queryset em blocos de tamanho n"""
    for i in range(0, len(queryset), n):
        yield queryset[i:i + n]


def carousel_view(request):
    # Busca os 6 primeiros médicos do banco de dados
    medicos = PerfilDoctor.objects.all()[:6]
    # Agrupa os médicos em grupos de 3
    medicos_grouped = list(group_queryset(medicos, 3))

    return render(request, 'partials/carousel.html', {'medicos_grouped': medicos_grouped}) # noqa E501
