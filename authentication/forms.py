from django.forms import ModelForm
from django import forms
from .models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Enter Username"}),
            "email": forms.EmailInput(attrs={"placeholder": "Enter Email"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Enter Password"}),
        }
        exclude = ["refresh_token", "role"]


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"})
    )
