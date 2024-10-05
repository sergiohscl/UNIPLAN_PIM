from django.urls import path
from . import views

urlpatterns = [
    path('marcar_consulta/', views.marcar_consulta, name='marcar_consulta'),
    path('my_queries/', views.my_queries, name="my_queries"),
]
