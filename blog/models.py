from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models import signals
from django.db.models.signals import pre_save, post_delete, post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

User = get_user_model()

def upload_location(instance, filename, **kwargs):
    filename = str(filename).split(".")[0]
    filepath = "blog-image/{author}/{title}-{filename}.jpg".format(author=instance.author.username, title=instance.title,filename=filename)
    return filepath

def upload_video(instance, filename, **kwargs):
    filename = str(filename).split(".")[0]
    path = "blog-video/{author}/{title}-{filename}.mp4".format(author=instance.author.username, title=instance.title, filename=filename)
    return path

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=1000)
    image_png = models.ImageField(upload_to="png",blank=True, null=True)
    image = models.ImageField(upload_to=upload_location,blank=True, null=True)
    video = models.FileField(upload_to=upload_video, blank=True, null=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    slug = models.CharField(max_length=100)
    author = models.ForeignKey(User,related_name="blogpost", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title    

@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

def add_slug_to_obj(sender, instance, *args, **kwargs):
    print(instance.author)
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + str(instance.title))

pre_save.connect(add_slug_to_obj, sender=BlogPost)