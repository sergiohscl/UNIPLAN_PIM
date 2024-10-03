from django import forms
from .models import PerfilDoctor


class PerfilDoctorForm(forms.ModelForm):
    # first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) # noqa E501
    # last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) # noqa E501
    # cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) # noqa E501
    # city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) # noqa E501
    # country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) # noqa E501
    # telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})) # noqa E501

    class Meta:
        model = PerfilDoctor
        fields = [
            'specialty', 'price', 'crm', 'description'
        ]
        widgets = {
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'crm': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), # noqa E501
        }

    def __init__(self, *args, **kwargs):
        # Recebe o perfil associado ao médico no formulário
        self.perfil = kwargs.pop('perfil', None)
        super(PerfilDoctorForm, self).__init__(*args, **kwargs)

        if self.perfil:
            # Preenche os campos com os valores do perfil existente
            self.fields['first_name'].initial = self.perfil.first_name
            self.fields['last_name'].initial = self.perfil.last_name
            self.fields['cpf'].initial = self.perfil.cpf
            self.fields['city'].initial = self.perfil.city
            self.fields['country'].initial = self.perfil.country
            self.fields['telefone'].initial = self.perfil.telefone

    def save(self, commit=True):
        # Salva o perfil associado juntamente com o perfil do médico
        instance = super(PerfilDoctorForm, self).save(commit=False)

        if self.perfil:
            self.perfil.first_name = self.cleaned_data['first_name']
            self.perfil.last_name = self.cleaned_data['last_name']
            self.perfil.cpf = self.cleaned_data['cpf']
            self.perfil.city = self.cleaned_data['city']
            self.perfil.country = self.cleaned_data['country']
            self.perfil.telefone = self.cleaned_data['telefone']
            if commit:
                self.perfil.save()
                instance.save()

        return instance
