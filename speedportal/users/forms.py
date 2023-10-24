from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес электронной почты'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите имя пользователя'
    }))
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Подтведите пароль'
    }))

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Введите адрес электронной почты'
    }))
    password = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')