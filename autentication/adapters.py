from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):

        user_email = sociallogin.account.extra_data.get('email')
        user_given_name = sociallogin.account.extra_data.get('given_name')
        user_family_name = sociallogin.account.extra_data.get('family_name')

        # Se o e-mail não estiver disponível, tenta buscar pelo nome
        if user_email is None and user_given_name and user_family_name:
            user = User.objects.filter(
                Q(first_name__iexact=user_given_name) &
                Q(last_name__iexact=user_family_name)
            ).first()

            if user:
                user_email = user.email
                sociallogin.connect(request, user)
            else:
                return

        # Se o e-mail estiver disponível, tente a unificação normalmente
        elif user_email:
            try:
                user = User.objects.get(email=user_email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                pass
