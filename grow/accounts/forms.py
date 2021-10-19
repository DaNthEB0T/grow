from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import *


class GrowUserRegistrationForm(UserCreationForm):
    error_messages = {
        'invalid_email': _("Email {} is already in use"),
        'invalid_username': _("Username {} is already in use! Yuck!!!")
    }

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
        raise forms.ValidationError(
            self.error_messages['invalid_email'].format(email),
            code="email_in_use",
        )
    
    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = GrowUser.objects.get(username=username)
        except:
            return username
        raise forms.ValidationError(
            self.error_messages['invalid_username'].format(username), 
            code="username_in_use",
        )

class GrowUserLoginForm(forms.ModelForm):
    error_messages = {
        'invalid_email': _("Invalid email"),
        'invalid_password': _("Invalid password")
    }
    email = forms.EmailField(label=_("Email address"),widget=forms.EmailInput(attrs={'placeholder': " "}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder': " "}))

    def __init__(self, *args, **kwargs):
        super(GrowUserLoginForm, self).__init__(*args, **kwargs)  
        self.label_suffix = ""

    class Meta:
        model = GrowUser
        fields = ("email", "password")

    def clean(self):
        email = self.cleaned_data.get("email").lower()
        password = self.cleaned_data.get("password")
        try: 
            user = GrowUser.objects.get(email=email)
        except:
            self.add_error("email", self.error_messages['invalid_email'])
            return
        if not authenticate(email=email, password=password):
            self.add_error("password", self.error_messages['invalid_password'])

class GrowUserForgotPasswordForm(PasswordResetForm):
    error_messages = {
        'invalid_email': _("Ding, dong, email is wrong"),
    }
    email = forms.EmailField(label=_('Email address'),
        max_length=255,
        required=True,
        widget=forms.TextInput(
         attrs={'placeholder': _('email address'),
                'type': 'text',
                'id': 'email_address'
                }
        ))
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            user = GrowUser.objects.get(email=email)
            return email
        except:
            raise forms.ValidationError(
                self.error_messages["invalid_email"],
                code="invalid_email",
                )   

class GrowUserPasswordChangeForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two passwords don't match."),
        'password_redundancy': _("Cannot set to previous password")
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(GrowUserPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code="password_mismatch",
                )

        if(authenticate(email=self.user.email, password=password2)):
            raise forms.ValidationError(
                self.error_messages['password_redundancy'],
                code="password_redundancy",
            )
        
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

            

