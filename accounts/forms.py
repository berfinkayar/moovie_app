from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.forms import TextInput

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            "username": TextInput(
                attrs={"class": "form-control", "style": "width:450px;",}
            ),
            "email": TextInput(
                attrs={"class": "form-control", "style": "width:450px;",}
            ),
            "password1": TextInput(
                attrs={"class": "form-control",}
            ),
            "password2": TextInput(
                attrs={"class": "form-control",}
            ),
        }
