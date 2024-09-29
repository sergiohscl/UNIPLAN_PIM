import os
import django
import random
from faker import Faker
from validate_docbr import CPF
from django.contrib.auth.models import User
from doctors.models import PerfilDoctor, Specialties, AvailableDate
from accounts.models import Perfil
from django.db.models.signals import post_save
from accounts.models import criar_perfil_usuario, salvar_perfil_usuario

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

fake = Faker('pt-BR')
Faker.seed(10)
cpf_generator = CPF()


# Função para gerar URLs de avatar baseados no nome do usuário
def generate_avatar_url(name):
    base_url = "https://ui-avatars.com/api/"
    return f"{base_url}?name={name.replace(' ', '+')}&size=256&background=random&rounded=true" # noqa E501


# Função para garantir que o username seja único, adicionando números se necessário # noqa E501
def get_unique_username():
    base_username = fake.user_name()
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    return username


def create_specialties():
    specialties = [
        "Cardiologia", "Dermatologia",
        "Ortopedia", "Pediatria",
        "Psiquiatria", "Neurologia",
        "Oftalmologia", "Pneumologia", "Otorrinolaringologia"
    ]
    specialty_objs = []
    for spec in specialties:
        specialty_obj, created = Specialties.objects.get_or_create(specialty=spec) # noqa E501
        specialty_objs.append(specialty_obj)
    return specialty_objs


def create_users_and_doctors(qtd_users, qtd_medicos):
    specialties = create_specialties()

    # Desativar sinais automáticos temporariamente
    post_save.disconnect(criar_perfil_usuario, sender=User)
    post_save.disconnect(salvar_perfil_usuario, sender=User)

    try:
        # Criar usuários comuns
        for _ in range(qtd_users):
            username = get_unique_username()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{username}@{fake.free_email_domain()}".replace(' ', '')
            password = fake.password()

            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password # noqa E501
            )

            # Gerar avatar usando o nome do usuário
            avatar_url = generate_avatar_url(first_name + " " + last_name)

            # Criar um perfil associado ao usuário (com avatar)
            Perfil.objects.create(user=user, foto=avatar_url)

        # Criar médicos
        for _ in range(qtd_medicos):
            username = get_unique_username()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{username}@{fake.free_email_domain()}".replace(' ', '')
            password = fake.password()

            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password # noqa E501
            )

            # Gerar avatar usando o nome do usuário
            avatar_url = generate_avatar_url(first_name + " " + last_name)

            # Criar um perfil associado ao usuário (com avatar)
            perfil = Perfil.objects.create(user=user, foto=avatar_url)

            # Criar um perfil de médico associado ao perfil do usuário
            specialty = random.choice(specialties)
            crm = fake.bothify(text="#######")
            cpf = cpf_generator.generate()
            city = fake.city()
            country = fake.country()
            telefone = fake.phone_number()
            description = fake.paragraph(nb_sentences=3)

            doctor_profile = PerfilDoctor.objects.create(
                perfil=perfil, specialty=specialty, price=random.uniform(100, 500), # noqa E501
                crm=crm, cpf=cpf, city=city, country=country, telefone=telefone, description=description # noqa E501
            )

            # Gerar algumas datas de disponibilidade
            for _ in range(random.randint(1, 5)):
                AvailableDate.objects.create(
                    doctor=doctor_profile,
                    date=fake.date_this_year(),
                )

        print(f'{qtd_users} usuários comuns e {qtd_medicos} médicos criados com sucesso!') # noqa E501

    finally:
        # Reativar sinais automáticos após a criação
        post_save.connect(criar_perfil_usuario, sender=User)
        post_save.connect(salvar_perfil_usuario, sender=User)


if __name__ == "__main__":
    create_users_and_doctors(30, 30)
    print("Script finalizado com sucesso!")
