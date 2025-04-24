from django.contrib.auth import forms
from django.contrib.auth.forms import AuthenticationForm



class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(
        label='Ваш пароль',  # Указываем свою метку
        widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'})
    )