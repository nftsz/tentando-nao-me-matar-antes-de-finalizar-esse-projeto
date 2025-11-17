from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='CPF', max_length=11)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    error_messages = {
        "invalid_login": "CPF ou senha incorretos.",
        "inactive": "Esta conta está inativa.",
    }

