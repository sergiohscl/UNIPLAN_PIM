import os
import django
from django.conf import settings
# from accounts.models import Perfil
from doctors.models import PerfilDoctor

# Configuração do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setrup.settings")
django.setup()

# Caminho dos avatares para médicos e médicas
AVATAR_PATH_MALE = os.path.join(settings.BASE_DIR, 'media/contas/imagens/medicos') # noqa E501
AVATAR_PATH_FEMALE = os.path.join(settings.BASE_DIR, 'media/contas/imagens/medicas') # noqa E501


def get_avatar_files(path):
    """Função para listar os arquivos de avatar no diretório"""
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))] # noqa E501


def update_perfil_avatars():
    avatars_male = get_avatar_files(AVATAR_PATH_MALE)
    avatars_female = get_avatar_files(AVATAR_PATH_FEMALE)

    total_avatars_male = len(avatars_male)
    total_avatars_female = len(avatars_female)

    if total_avatars_male == 0 and total_avatars_female == 0:
        print("Nenhum arquivo de avatar encontrado.")
        return

    # Filtrar apenas perfis que são médicos
    perfis_doctors = PerfilDoctor.objects.all()

    for idx, perfil_doctor in enumerate(perfis_doctors):
        perfil = perfil_doctor.perfil
        user_sexo = perfil.user.perfil.sexo  # Presumindo que existe um campo 'sexo' em Perfil # noqa E501

        if user_sexo == 'M' and total_avatars_male > 0:
            avatar_index = idx % total_avatars_male  # Distribuir ciclicamente os avatares masculinos # noqa E501
            avatar_file = avatars_male[avatar_index]
            avatar_path = f"contas/imagens/medicos/{avatar_file}"
        elif user_sexo == 'F' and total_avatars_female > 0:
            avatar_index = idx % total_avatars_female  # Distribuir ciclicamente os avatares femininos # noqa E501
            avatar_file = avatars_female[avatar_index]
            avatar_path = f"contas/imagens/medicas/{avatar_file}"
        else:
            continue  # Pular se não encontrar avatar para o sexo

        # Atualizar o campo 'foto' do perfil com o caminho do novo avatar
        perfil.foto = avatar_path
        perfil.save()

    print(f"Avatares atualizados para {len(perfis_doctors)} perfis de médicos!") # noqa E501


if __name__ == "__main__":
    update_perfil_avatars()
