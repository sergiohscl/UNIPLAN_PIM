from django import forms
from .models import PerfilDoctor


class PerfilDoctorForm(forms.ModelForm):
    class Meta:
        model = PerfilDoctor
        fields = [
            'specialty', 'price', 'crm', 'city',
            'country', 'telefone', 'description'
        ]

    def __init__(self, *args, **kwargs):
        super(PerfilDoctorForm, self).__init__(*args, **kwargs)
        # Aplica a classe 'form-control' do Bootstrap 5 a todos os campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
