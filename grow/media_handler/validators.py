from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from .library import get_mime_type
import magic

@deconstructible
class MimeTypeValidator(object):
    error_messages = {
        'media_bad_file': _("File type not supported ({})"),
        'media_exceeds_max_size': _("File exceeds maximum allowed size"),
    }
    
    def __init__(self, mime_types, max_size):
        self.mimetypes = mime_types
        self.max_size = max_size
        
    def __call__(self, file):
        if file.size > self.max_size:
            raise ValidationError(
                self.error_messages['media_exceeds_max_size'],
                code="wrong_size",
                )
        try:
            mime = get_mime_type(file)
            if not mime in self.mimetypes:
                raise ValidationError(
                    self.error_messages['media_bad_file'].format(mime),
                    code="bad_file",
                )        
        except AttributeError as e:
            raise ValidationError('This value could not be validated for file type' % file)

    def __eq__(self, other):
        return isinstance(other, MimeTypeValidator) and self.mimetypes == other.mime_types and self.max_size == other.max_size