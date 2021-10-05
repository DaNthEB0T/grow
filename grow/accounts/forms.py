from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import *


class GrowUserRegistrationForm(UserCreationForm):

    class Meta:
        model = GrowUser
        fields = ("email", "user_name", "first_name", "last_name", "password1", "password2")
        help_texts = {
            'email': "Entrez votre email ci-dessous",
            'user_name': "wadap yourself here pls",
            'first_name': "enter your grown-ass mf name",
            'last_name': "now the other half",
        }
