import logging
from django.db import models
from accounts.models import GrowUser
from PIL import Image as Im
from django.core.files.uploadedfile import SimpleUploadedFile
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from django.utils.crypto import get_random_string
from django.db.models import Count, Case, When
import random
import os
from io import BytesIO
import time
from collections import defaultdict
from .library import *
from .recomai import get_similar_posts
from .templatetags.markdown_extras import unmark

logger = logging.getLogger(__name__)

class Media(models.Model):
    def user_directory_path(instance, filename):
        return time.strftime(f"user_{instance.author.id}/%d_%m_%Y/med/{filename}") 
    
    upload = models.FileField(upload_to=user_directory_path)
    author = models.ForeignKey(GrowUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="medias")
    
    @property
    def mime_type(self):
        return get_mime_type(self.upload.file)
    
    @classmethod
    def integrity_check(cls, **kwargs):
        for m in Media.objects.all():
            if not os.path.isfile(m.upload.path):
                logger.error(f"Object {m} has no media file at {m.upload.path}")
                
    @classmethod
    def clean(cls, **kwargs):
        from grow.settings import MEDIA_ROOT
        empty = [root for root, dirs, files, in os.walk(MEDIA_ROOT)
                   if not len(dirs) and not len(files)]
        for empty_dir in empty:
            os.removedirs(empty_dir)

    
class Image(models.Model):
    def user_directory_path(instance, filename):
        return time.strftime(f"user_{instance.author.id}/%d_%m_%Y/img/{filename}") 
    
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
    
    @property
    def mime_type(self):
        return get_mime_type(self.image.file)
    
    @classmethod
    def integrity_check(cls, **kwargs):
        for i in Image.objects.all():
            if not (os.path.isfile(i.image.path) and os.path.isfile(i.thumbnail.path)):
                logger.error(f"Object {i} has no image file at {i.image.path} or {i.thumbnail.path}")

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

# Deletes file from filesystem
# when corresponding `Media` object is deleted.
@receiver(models.signals.post_delete, sender=Media)
def auto_delete_media_on_delete(sender, instance, **kwargs):
    if instance.upload:
        if os.path.isfile(instance.upload.path):
            os.remove(instance.upload.path)
            
    Media.clean()
            
# Deletes old file from filesystem
# when corresponding `Media` object is updated
# with new file.
@receiver(models.signals.pre_save, sender=Media)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_media = Media.objects.get(pk=instance.pk).upload
    except Media.DoesNotExist:
        return False

    new_media = instance.upload
    if not old_media == new_media:
        if os.path.isfile(old_media.path):
            os.remove(old_media.path)
            
    Media.clean()


# Deletes file from filesystem
# when corresponding `Image` object is deleted.
@receiver(models.signals.post_delete, sender=Image)
def auto_delete_media_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)
    
    Media.clean()

# Deletes old file from filesystem
# when corresponding `Image` object is updated
# with new file.
@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = Image.objects.get(pk=instance.pk).image
        old_thumbnail = Image.objects.get(pk=instance.pk).thumbnail
    except Image.DoesNotExist:
        return False

    new_image = instance.image
    if not old_image == new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
        if os.path.isfile(old_thumbnail.path):
            os.remove(old_thumbnail.path)
    
    Media.clean()
    

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=10, unique=True)
    author = models.ForeignKey(GrowUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    updated_on = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    media_content = models.ForeignKey(Media, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="post")
    prequel = models.ForeignKey("self", on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="sequel")
    thumbnail = models.ForeignKey(Image, on_delete=models.SET_NULL, default=None, null=True, blank=True, related_name="post_parent")
    saved = models.ManyToManyField(GrowUser, default=None, blank=True, related_name="saved_posts")
    watchlist = models.ManyToManyField(GrowUser, default=None, blank=True, related_name="watchlist_posts")
    history = models.ManyToManyField(GrowUser, default=None, blank=True, through="PostHistoryManager", related_name="post_history")
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = TaggableManager(blank=True)
    
    class Meta:
        ordering = ['created_on']
        
    # Gets 'amount' most relevant posts to a user according to 'depth' most recent views
    @classmethod
    def get_recommended_posts(cls, user, amount=15, depth=15, noise=0.15):           
        def decision(probability):
            return random.random() < probability
        
        if Post.objects.count() < amount or amount <= 0:
            amount = Post.objects.count()
            
        if depth <= 0:
            depth = 15
            
        if user.post_history.all():
            # 1st row == similar posts to last viewed post
            historical_similarity = [get_similar_posts(post) for post in Post.get_user_history(user).reverse()[:depth]]
            historical_similarity = [queryset_diff(row, user.post_history.all()) for row in historical_similarity]
            
            average_indices = defaultdict(lambda: 0)
            
            for row in historical_similarity:
                for j, val in enumerate(row):
                    average_indices[val] += j
            
            average_indices = {post: i/len(historical_similarity) for post, i in average_indices.items()}
            average_indices = dict(sorted(average_indices.items(), key=lambda item: item[1]))
            recommendations = list(average_indices.keys())[:amount]
        else:
            recommendations = list(Post.order_by_popularity())[:amount]
            
        noise_data = list(queryset_diff((Post.objects.all().exclude(id__in=[post.id for post in recommendations])), user.post_history.all()).order_by("?"))
        
        for i, val in enumerate(recommendations[1:]):
            if noise_data and decision(noise):
                recommendations[i+1] = noise_data.pop()
            else:
                break    
        
        # for i in range(len(recommendations)):
        #     while recommendations[i].prequel:
        #         recommendations[i] = recommendations[i].prequel
            
        return recommendations    
    
    # Return user history ordered by ascending timestamp
    @classmethod
    def get_user_history(cls, user):
        pks = PostHistoryManager.objects.filter(user=user).values_list("post", flat=True)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
        return Post.objects.filter(pk__in=pks).order_by(preserved)      
        
    # Return ordered by distinct view count
    @classmethod
    def order_by_popularity(cls, ascending=False):
        return Post.objects.annotate(fame=Count("history")).order_by(("" if ascending else "-") + "fame")
    
    # Return ordered by saved count
    @classmethod
    def order_by_saved_count(cls, ascending=False):
        return Post.objects.annotate(saved_count=Count("saved")).order_by(("" if ascending else "-") + "saved_count")
    
    # Return ordered by count in "watch later"
    @classmethod
    def order_by_watchlist_count(cls, ascending=False):
        return Post.objects.annotate(watchlist_count=Count("watchlist")).order_by(("" if ascending else "-") + "watchlist_count")
    
    # Description without markdown tags
    @property
    def description_raw(self):
        return unmark(self.description)
    
    # Distinct view count (1 per each user)
    @property
    def popularity(self):
        return self.history.count()
    
    # How likely it is for a user to save the post
    @property
    def save_popularity_index(self):
        if self.popularity == 0:
            return 0
        return self.saved.count() / self.popularity
    
        
    def save(self, *args, **kwargs):    
        while True:
            self.slug = get_random_string(length=10)
            if not Post.objects.filter(slug=self.slug).exists():
                logger.info(f"Slug: {self.slug}")
                break
        
        super(Post, self).save(*args, **kwargs) 

    def __str__(self):
        return self.title
    
@receiver(models.signals.post_delete, sender=Post)
def auto_delete_media_on_delete(sender, instance, **kwargs):
    """
    Deletes files from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.media_content:
        instance.media_content.delete()
            
    if instance.thumbnail:
        instance.thumbnail.delete()
        
        
class PostHistoryManager(models.Model):
    user = models.ForeignKey(GrowUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_on']