
from doctors.models import is_medico


def medico_context(request):
    if request.user.is_authenticated:
        return {'is_medico': is_medico(request.user)}
    return {'is_medico': False}
