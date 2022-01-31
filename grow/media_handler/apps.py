from django.apps import AppConfig



class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media_handler'
    
    def ready(self):
        from .models import Image, Media
        Media.clean()
        Media.integrity_check()
        Image.integrity_check()
