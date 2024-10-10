import random
from datetime import timedelta, date, datetime
from doctors.models import PerfilDoctor, AvailableDate, AvailableTime


# Função para gerar uma lista de datas
def generate_dates(start_date, num_days):
    return [start_date + timedelta(days=i) for i in range(num_days)]


# Função para gerar horários aleatórios em um dia específico
def generate_times():
    # Defina os horários de início e término do expediente (por exemplo, das 9h00 às 18h00) # noqa E501
    start_time = datetime.strptime("09:00", "%H:%M").time()
    end_time = datetime.strptime("18:00", "%H:%M").time()

    # Defina o intervalo entre os horários (em minutos)
    interval = 60  # Intervalo de 60 minutos (1 hora)

    # Gera uma lista de horários dentro do intervalo especificado
    times = []
    current_time = start_time
    while current_time < end_time:
        times.append(current_time)
        # Adiciona o intervalo ao horário atual
        current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=interval)).time() # noqa E501

    # Retorna um subconjunto aleatório dos horários (entre 2 e 5 horários por dia) # noqa E501
    return random.sample(times, random.randint(2, 5))


# Função para popular AvailableDate e AvailableTime
def populate_available_dates_and_times():
    # Recupera todos os médicos
    doctors = PerfilDoctor.objects.all()

    # Define a data inicial e a quantidade de dias a serem gerados
    start_date = date.today()
    num_days = 10  # Por exemplo, gerar datas para os próximos 10 dias

    # Itera por cada médico e associa um conjunto de datas e horários
    for doctor in doctors:
        dates = generate_dates(start_date, num_days)

        for available_date in dates:
            # Cria e salva uma data disponível para o médico com `scheduled=False` por padrão # noqa E501
            date_instance = AvailableDate.objects.create(
                doctor=doctor,
                date=available_date,
                scheduled=False  # Definido como False por padrão
            )

            # Gera horários para a data disponível
            times = generate_times()
            for horario in times:
                # Cria e salva um horário para a data disponível com `scheduled=False` # noqa E501
                AvailableTime.objects.create(
                    available_date=date_instance,
                    time=horario,
                    scheduled=False  # Definido como False por padrão
                )

    print(f"Available dates and times populated for {doctors.count()} doctors.") # noqa E501


# Executa o script
populate_available_dates_and_times()
