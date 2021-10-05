from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import *


class GrowUserRegistrationForm(UserCreationForm):

    class Meta:
        model = GrowUser
        fields = ("email", "username", "first_name", "last_name", "password1", "password2")
        help_texts = {
            'email': "Entrez votre email ci-dessous",
            'username': "wadap yourself here pls",
            'first_name': "enter your grown-ass mf name",
            'last_name': "now the other half",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        try:
            user = GrowUser.objects.get(email=email)
        except:
            return email
        raise forms.ValidationError(_(f"Email {email} is already in use!"), code="in_use")
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = GrowUser.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError(_(f"User name {username} is already in use! Yuck!!!"), code="in_use")

class GrowUserLoginForm(forms.ModelForm):
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = GrowUser
        fields = ("email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get("email").lower()
            password = self.cleaned_data.get("password")
            try: 
                user = GrowUser.objects.get(email=email)
            except:
                self.add_error("email", _("No user exists for given email"))
                return
            if not authenticate(email=email, password=password):
                self.add_error("password", _("Wrong password"))

            

