from django.contrib import admin
from .models import Consulta, Document


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = (
        'patient', 'available_date', 'available_time', 'status', 'link'
    )
    list_filter = ('status', 'available_date', 'available_time')
    search_fields = (
        'patient__user__username',
        'available_date__date',
        'available_time__time'
    )
    list_editable = ('status', 'link')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'consulta', 'document')
    search_fields = ('title', 'consulta__patient__user__username')
