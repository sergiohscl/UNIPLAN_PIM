from django.urls import path
from . import views

urlpatterns = [
    path('choose_time/<int:id_dados_medicos>/', views.choose_time, name="choose_time"), # noqa E501
    path('schedule_time/<int:id_data_aberta>/', views.schedule_time, name="schedule_time"), # noqa E501
    path('my_queries/', views.my_queries, name="my_queries"),
    path('consulta/<int:id_consulta>/', views.consulta, name="consulta"),
    path('cancel_consulta/<int:id_consulta>/', views.cancel_consulta, name="cancel_consulta"), # noqa E501
]
