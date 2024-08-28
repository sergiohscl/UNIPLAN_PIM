from django.urls import path
from autentication import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login, name="login"),
    path('autentication/processa_logout/', views.processa_logout, name='logout'), # noqa E501
    path('autentication/processa_redirect_home/', views.processa_redirect_home, name='ir_home'), # noqa E501

    path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name="autentication/password_reset_form.html"
        ), name="password_reset"),

    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view( # noqa E501
            template_name="autentication/password_reset_confirm.html"
        ), name="password_reset_confirm"),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
            template_name="autentication/password_reset_done.html"
        ), name="password_reset_done"),

    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(  # noqa E501
            template_name='autentication/password_reset_complete.html'
        ), name="password_reset_complete")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
