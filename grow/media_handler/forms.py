from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
import grow.settings as settings
from .library import *

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("image",)

class PostUploadForm(forms.ModelForm):
    error_messages = {
        'media_bad_file': _("File type not supported ({})"),
        'media_exceeds_max_size': _("File exceeds max allowed size"),
    }
    media_content = forms.FileField(required=False)
    prequel = forms.ModelChoiceField(queryset=Post.objects.none(), required=False)
    thumbnail = forms.ImageField(required=False)
    
    class Meta:
        model = Post
        fields = ("title", "description", "status", "tags")
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        self.author = user
        super(PostUploadForm, self).__init__(*args, **kwargs)
        if user.posts:
            self.fields["prequel"].queryset = user.posts
    
    def clean_media_content(self):
        media_content = self.cleaned_data['media_content']
        
        if media_content:
            if media_content.size > settings.MAX_MEDIA_FILE_SIZE:
                raise forms.ValidationError(
                    self.error_messages['media_exceeds_max_size'],
                    code="wrong_size",
                    )
            
            mime_type = get_mime_type(media_content.file)
            if mime_type in settings.ALLOWED_MEDIA_FILE_TYPES:
                return media_content
            
            raise forms.ValidationError(
                self.error_messages['media_bad_file'].format(mime_type),
                code="bad_file",
            )
    
    def clean_thumbnail(self):
        thumbnail = self.cleaned_data['thumbnail']  
        
        if thumbnail:
            if thumbnail.size > settings.MAX_IMAGE_FILE_SIZE:
                raise forms.ValidationError(
                    self.error_messages['media_exceeds_max_size'],
                    code="wrong_size",
                    )
            
            mime_type = get_mime_type(thumbnail.file)
            if mime_type in settings.ALLOWED_IMAGE_FILE_TYPES:
                return thumbnail
            
            raise forms.ValidationError(
                self.error_messages['media_bad_file'].format(mime_type),
                code="bad_file",
            )          
        
            
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