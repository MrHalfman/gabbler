from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # first_name, last_name and username, password, email are already defined
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
    banner = models.ImageField(upload_to="banners/", blank=True)
    bio = models.TextField(max_length=300)
    birthdate = models.DateTimeField()
    place = models.ForeignKey("Place")
    privacy = models.BooleanField(default="true") # TODO : Voir avec Enguerrand pour des conseils d'utilisation

class Place(models.Model):
    city = models.CharField(max_length=163)
    country = models.CharField(max_length=200)

class UserLink(models.Model):
    user = models.ForeignKey("User", related_name="links")
    type = models.ForeignKey("UserLinkTypes")
    url = models.URLField()


class UserLinkTypes(models.Model):
    name = models.CharField(max_length = 255)
    icon = models.ImageField(upload_to="socialIcons/", blank=True)


