from django import forms
from django.forms import ModelForm
from contact.models import Contact


class FormContato(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'assunto': forms.Select(attrs={'class': 'form-control form-select mb-3'}), # noqa E501
            'nome': forms.TextInput(attrs={'class': 'form-control mb-3'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control mb-3'}),
        }
        labels = {
            'assunto': 'Assunto',
            'nome': 'Nome',
            'email': 'Email',
            'mensagem': 'Mensagem',
        }
