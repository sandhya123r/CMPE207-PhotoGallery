from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
import os
# Create your models here.


class User(models.Model) :
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, default="foo@gmail.com")
    password = models.CharField(max_length=100)


def images_path(instance, filename):
    return 'images/'.join([str(instance.album.user.user_id), str(instance.album.album_id), filename])


def thumbnail(instance, filename):
    return 'thumbs/'.join([str(instance.album.user.user_id), str(instance.album.album_id), filename])


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=100)
    album_id = models.AutoField(primary_key=True)


class Photo(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to=images_path)
    thumbnail = models.ImageField(upload_to=thumbnail, editable=False)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)


@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
