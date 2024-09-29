from django.contrib import admin
from .models import PerfilDoctor, AvailableDate, Specialties


@admin.register(Specialties)
class SpecialtiesAdmin(admin.ModelAdmin):
    list_display = ('specialty',)


@admin.register(PerfilDoctor)
class PerfilDoctorAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'specialty', 'crm', 'city', 'country')
    search_fields = ('perfil__user__username', 'crm', 'city', 'country')
    list_filter = ('specialty', 'city', 'country')


@admin.register(AvailableDate)
class AvailableDateAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'date', 'scheduled')
    search_fields = ('doctor__perfil__user__username', 'date')
    list_filter = ('doctor', 'date')
    ordering = ('doctor', 'date')
