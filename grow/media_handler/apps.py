from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class MediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'media_handler'
    
    def ready(self):
        try:
            from .models import Image, Media
            Media.clean()
            Media.integrity_check()
            Image.integrity_check()
        except Exception as e:
            logger.warning(e)
