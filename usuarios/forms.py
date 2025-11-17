from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Paciente, OCI

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='CPF', max_length=11)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "CPF ou senha incorretos.",
        "inactive": "Esta conta está inativa.",
    }


class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        widgets = {
            'data_agendamento_sisreg': forms.DateInput(attrs={'type': 'date'}),
        }


class OCIForm(forms.ModelForm):
    class Meta:
        model = OCI
        fields = [
            'codigo_oci', 'nome_oci', 'tipo', 'profissional_executante',
            'data_abertura', 'data_conclusao', 'observacoes'
        ]
        widgets = {
            'data_abertura': forms.DateInput(attrs={'type': 'date'}),
            'data_conclusao': forms.DateInput(attrs={'type': 'date'}),
        }
