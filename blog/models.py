import re
from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse

from django.db import models
from django.db.models.signals import pre_save

from instablog.validators import jpeg_validator
from instablog.image import receiver_with_image_field
from instablog.file import random_name_with_file_field
from instablog.thumbnail import make_thumbnail

from django.db.models.signals import post_delete
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    uuid = models.UUIDField(default=uuid4, editable=False, db_index=True)
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=100, db_index=True)
    content = models.TextField()
    photo = models.ImageField(blank=True, null=True, validators=[jpeg_validator],
                            upload_to=random_name_with_file_field)
    tags = models.ManyToManyField('Tag', blank=True)
    origin_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.author.username, self.uuid.hex])

    def get_thumbnail_url(self):
        return make_thumbnail(self.photo.path, 400, 400)

    class Meta:
        ordering = ['-created_at']

@receiver(post_delete, sender=Post)
def delete_attached_image(sender, **kwargs):
    instance = kwargs.pop('instance')
    instance.photo.delete(save=False)



receiver = receiver_with_image_field('photo', 800)
pre_save.connect(receiver, sender=Post)


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name
