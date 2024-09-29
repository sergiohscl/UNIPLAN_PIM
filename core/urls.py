from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('contact/', include('contact.urls')),
    path('auth/', include('autentication.urls')),
    path('create_account/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('doctors/', include('doctors.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
