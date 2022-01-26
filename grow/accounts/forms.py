from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.forms import widgets
from django.forms.fields import EmailField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from .models import *


class GrowUserRegistrationForm(UserCreationForm):
    error_messages = {
        'invalid_email': _("Email {} is already in use"),
        'invalid_username': _("Username {} is already in use! Yuck!!!")
    }

    email = forms.EmailField(label=_("Email address"), widget=forms.EmailInput(attrs={'placeholder': " ", 'id': "register_email"}))
    username = forms.CharField(label=_("Username"), widget=forms.TextInput(attrs={'placeholder': " ", 'id': "register_username"}))
    first_name = forms.CharField(label=_("First name"), widget=forms.TextInput(attrs={'placeholder': " ", 'id': "register_first_name"}))
    last_name = forms.CharField(label=_("Last name"), widget=forms.TextInput(attrs={'placeholder': " ", 'id': "register_last_name"}))
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder': " ", 'id': "register_password1"}))
    password2 = forms.CharField(label=_("Confirm password"), widget=forms.PasswordInput(attrs={'placeholder': " ", 'id': "register_password2"}))
    class Meta:
        model = GrowUser
        fields = ("email", "username", "first_name", "last_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower()
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
    email = forms.EmailField(label=_("Email address"), widget=forms.EmailInput(attrs={'placeholder': " "}))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput(attrs={'placeholder': " "}))

    def __init__(self, *args, **kwargs):
        super(GrowUserLoginForm, self).__init__(*args, **kwargs)  
        self.label_suffix = ""

    class Meta:
        model = GrowUser
        fields = ("email", "password")
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email:
            email = email.lower()
        return email

    def clean(self):
        email = self.cleaned_data.get("email")
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
        if email:
            email = email.lower()
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

            

