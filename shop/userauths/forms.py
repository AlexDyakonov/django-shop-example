from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from django.utils.translation import gettext as _


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email'] 
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Никнейм'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('Email'), 
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': _('Пароль'),
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': _('Подтвердите пароль'),
            }),
        }