from enum import unique

from django.contrib.auth import forms, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, CharField, PasswordInput, TextInput, ImageField
from django.contrib.auth.models import User
from django import forms


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(ModelForm):
    username = CharField(label="Логин", )
    password = CharField(label="Пароль", widget=PasswordInput)
    password2 = CharField(label="Повтор пароля", widget=PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'password', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Пароли не совпадают!")
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.Form):
    email = CharField(disabled=False, label='E-mail', )
    avatar = ImageField(required=False)
    first_name = CharField()
