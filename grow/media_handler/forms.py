from django import forms
from django.forms.forms import Form
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from .models import *

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image",)

class PostUploadForm(forms.ModelForm):
    media_content = forms.FileField(required=False)
    prequel = forms.ModelChoiceField(queryset=Media.objects.none(), required=False)
    thumbnail = forms.ImageField(required=False)
    
    class Meta:
        model = Post
        fields = ("title", "slug", "description", "status", "tags")
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        self.author = user
        super(PostUploadForm, self).__init__(*args, **kwargs)
        if user.posts:
            self.fields["prequel"].queryset = user.posts
    
    def clean_media_content(self):
        media_content = self.cleaned_data["media_content"]
        
        #todo: media_content cannot be an image 
        
        return media_content
            
    def save(self, commit=True):
        instance = super(PostUploadForm, self).save(commit=False)
        instance.author = self.author
        
        if self.cleaned_data['media_content']:
            media, created = Media.objects.get_or_create(upload=self.cleaned_data['media_content'], author=self.author)
            instance.media_content = media
            
        if self.cleaned_data['thumbnail']:
            thumbnail, created = Image.objects.get_or_create(image=self.cleaned_data['thumbnail'], author=self.author)
            instance.thumbnail = thumbnail  
                      
        if commit:
            instance.save()
        return instance