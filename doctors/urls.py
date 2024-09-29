from django.urls import path
from . import views

urlpatterns = [
    path('perfil_doctor/', views.perfil_doctor_view, name='perfil_doctor'),
    path('perfil_doctor/editar/', views.editar_perfil_doctor, name='editar_perfil_doctor'), # noqa E501
    # path('list_availability/', views.list_availability, name='list_availability'), # noqa E501
    path('open_schedule/', views.open_schedule, name='open_schedule'),  # noqa E501
]
