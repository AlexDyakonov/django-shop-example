from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Никнейм"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder" : "Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = ['username','email']