from django.db import models
from accounts.models import GrowUser
from PIL import Image as Im
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from io import BytesIO
import time



class Media(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return time.strftime("user_{0}/%d_%m_%Y/med/{1}".format(instance.author.id, filename)) 
    
    upload = models.FileField(upload_to=user_directory_path)
    author = models.ForeignKey(GrowUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="medias")

    
class Image(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return time.strftime("user_{0}/%d_%m_%Y/img/{1}".format(instance.author.id, filename)) 
    
    author = models.ForeignKey(GrowUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="images")    
    image = models.ImageField(
        upload_to=user_directory_path
    )

    thumbnail = models.ImageField(
        upload_to=user_directory_path,
        max_length=500,
        null=True,
        blank=True
    )

    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return


        # Set our max thumbnail size in a tuple (max width, max height)
        THUMBNAIL_SIZE = (256, 144)

        DJANGO_TYPE = self.image.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Im.open(BytesIO(self.image.read()))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Im.ANTIALIAS)

        # Save the thumbnail
        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.thumbnail.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def save(self, *args, **kwargs):

        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set 
        # force_update to True
        if self.id:
            force_update = True

        # Force an UPDATE SQL query if we're editing the image to avoid integrity exception
        super(Image, self).save(force_update=force_update)    

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(GrowUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    media_content = models.ForeignKey(Media, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="post")
    prequel = models.ForeignKey("self", on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="sequel")
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="post_parent")
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title