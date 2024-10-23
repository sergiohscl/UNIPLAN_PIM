from django.urls import path
from . import views

urlpatterns = [
    path('perfil_doctor/', views.perfil_doctor_view, name='perfil_doctor'),
    path('perfil_doctor/editar/', views.editar_perfil_doctor, name='editar_perfil_doctor'), # noqa E501
    path('open_schedule/', views.open_schedule, name='open_schedule'),  # noqa E501
    path('list_specialty/<str:specialty>/', views.list_doctor_specialty, name='list_doctor_specialty'),  # noqa E501
    path('doctor/<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('doctor_queries/', views.doctor_queries, name='doctor_queries'),
    path('cancelar_consulta_medico/<int:consulta_id>/', views.cancelar_consulta_medico, name='cancelar_consulta_medico'), # noqa E501
    path('initialize_query/<int:consulta_id>/', views.initialize_query, name='initialize_query'), # noqa E501
    path('add_documento/<int:consulta_id>/',  views.add_documento, name="add_documento"), # noqa E501
    path('finalizar_consulta/<int:consulta_id>/', views.finalizar_consulta, name='finalizar_consulta'), # noqa E501
]
