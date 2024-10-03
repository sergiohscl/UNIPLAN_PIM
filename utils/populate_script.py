from django.contrib.auth.models import User
# from django.db import models
from django.db.models.signals import post_save
# from django.dispatch import receiver
from faker import Faker
from validate_docbr import CPF
import os
import django
import random

from accounts.models import Perfil, criar_perfil_usuario, salvar_perfil_usuario
from doctors.models import PerfilDoctor, Specialties

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

fake = Faker('pt-BR')
Faker.seed(10)
cpf_generator = CPF()


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
        # Definir senha fixa para todos os usuários
        password = "Django13$"

        # Criar usuários comuns
        for _ in range(qtd_users):
            username = get_unique_username()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{username}@{fake.free_email_domain()}".replace(' ', '')
            sexo = random.choice(['M', 'F'])

            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password # noqa E501
            )

            # Criar um perfil associado ao usuário (sem avatar)
            cpf = cpf_generator.generate()
            city = fake.city()
            country = fake.country()
            telefone = fake.phone_number()
            data_nasc = fake.date_of_birth()

            Perfil.objects.create(user=user, foto=" ", sexo=sexo, cpf=cpf, city=city, country=country, telefone=telefone, data_nasc=data_nasc) # noqa E501

        # Criar médicos
        for _ in range(qtd_medicos):
            username = get_unique_username()
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{username}@{fake.free_email_domain()}".replace(' ', '')
            sexo = random.choice(['M', 'F'])

            user = User.objects.create_user(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password # noqa E501
            )

            # Criar um perfil associado ao usuário (sem avatar)
            cpf = cpf_generator.generate()
            city = fake.city()
            country = fake.country()
            telefone = fake.phone_number()
            data_nasc = fake.date_of_birth()

            perfil = Perfil.objects.create(user=user, foto=" ", sexo=sexo, cpf=cpf, city=city, country=country, telefone=telefone, data_nasc=data_nasc) # noqa E501

            # Criar um perfil de médico associado ao perfil do usuário
            specialty = random.choice(specialties)
            crm = fake.bothify(text="#######")
            description = fake.paragraph(nb_sentences=3)

            PerfilDoctor.objects.create(
                perfil=perfil, specialty=specialty, price=random.uniform(100, 500), # noqa E501
                crm=crm, description=description
            )

            # # Gerar algumas datas de disponibilidade
            # for _ in range(random.randint(1, 5)):
            #     AvailableDate.objects.create(
            #         doctor=doctor_profile,  # PerfilDoctor do médico
            #         date=fake.date_this_year(),
            #     )

        print(f'{qtd_users} usuários comuns e {qtd_medicos} médicos criados com sucesso!') # noqa E501

    finally:
        # Reativar sinais automáticos após a criação
        post_save.connect(criar_perfil_usuario, sender=User)
        post_save.connect(salvar_perfil_usuario, sender=User)


if __name__ == "__main__":
    create_users_and_doctors(30, 30)
