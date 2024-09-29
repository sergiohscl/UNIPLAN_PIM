from django import forms
from .models import PerfilDoctor


class PerfilDoctorForm(forms.ModelForm):
    class Meta:
        model = PerfilDoctor
        fields = [
            'specialty', 'price', 'city',
            'country', 'telefone', 'description'
        ]
        widgets = {
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'crm': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), # noqa E501
        }
