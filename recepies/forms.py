from enum import unique

from django.contrib.auth import forms, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, CharField, PasswordInput, TextInput, ImageField

from django import forms

from recepies.models import User


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(ModelForm):
    username = CharField(label="Логин", required=False)
    password = CharField(label="Пароль", widget=PasswordInput)
    password2 = CharField(label="Повтор пароля", widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'password', 'password2']


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

    def clean_username(self):
        return self.cleaned_data['username']


class ProfileUserForm(forms.Form):
    email = CharField(disabled=False, label='E-mail', )
    avatar = ImageField(required=False)
    first_name = CharField()
