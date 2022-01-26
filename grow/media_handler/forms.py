from django import forms
from django.forms.forms import Form
from django.utils.translation import gettext_lazy as _
from .models import *

class ImageUpload(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
