import random
from datetime import timedelta, date
from doctors.models import PerfilDoctor, AvailableDate


# Função para gerar uma lista de datas
def generate_dates(start_date, num_days):
    return [start_date + timedelta(days=i) for i in range(num_days)]


# Função para popular AvailableDate
def populate_available_dates():
    # Recupera todos os médicos
    doctors = PerfilDoctor.objects.all()

    # Define a data inicial e a quantidade de dias a serem gerados
    start_date = date.today()
    num_days = 30  # Por exemplo, gerar datas para os próximos 30 dias

    # Itera por cada médico e associa um conjunto de datas
    for doctor in doctors:
        dates = generate_dates(start_date, num_days)

        for available_date in dates:
            # Cria e salva uma data disponível para o médico
            AvailableDate.objects.create(
                doctor=doctor,
                date=available_date,
                scheduled=random.choice([True, False])
            )

    print(f"Available dates populated for {doctors.count()} doctors.")


# Executa o script
populate_available_dates()
