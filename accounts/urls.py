from django.urls import path
from accounts import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.create_account, name='create_account'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
