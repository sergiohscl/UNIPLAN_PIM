from django.urls import path
from . import views


urlpatterns = [
    path('', views.contato, name='contact'),
    path('mensagem', views.processa_contato, name='mensagem'),
]
