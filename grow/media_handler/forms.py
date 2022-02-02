from django import forms
from django.utils.translation import gettext_lazy as _
from .validators import MimeTypeValidator
from .models import *
import grow.settings as settings

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image",)

class PostUploadForm(forms.ModelForm):
    media_content = forms.FileField(required=False, validators=[MimeTypeValidator(settings.ALLOWED_MEDIA_FILE_TYPES, settings.MAX_MEDIA_FILE_SIZE)])
    prequel = forms.ModelChoiceField(queryset=Post.objects.none(), required=False)
    thumbnail = forms.ImageField(required=False, validators=[MimeTypeValidator(settings.ALLOWED_IMAGE_FILE_TYPES, settings.MAX_IMAGE_FILE_SIZE)])
    
    class Meta:
        model = Post
        fields = ("title", "description", "status", "tags")
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(PostUploadForm, self).__init__(*args, **kwargs)
        self.author = user
        self.label_suffix = ""
        if user.posts:
            self.fields["prequel"].queryset = user.posts        
        
            
    def save(self, commit=True):
        instance = super(PostUploadForm, self).save(commit=False)
        instance.author = self.author
        
        if self.cleaned_data['media_content']:
            media, created = Media.objects.get_or_create(upload=self.cleaned_data['media_content'], author=self.author)
            instance.media_content = media
            
        if self.cleaned_data['thumbnail']:
            thumbnail, created = Image.objects.get_or_create(image=self.cleaned_data['thumbnail'], author=self.author)
            instance.thumbnail = thumbnail  
            
        instance.prequel = self.cleaned_data['prequel']
                      
        if commit:
            instance.save()
        return instance