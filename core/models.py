from django.db import models
from django.contrib.auth.models import AbstractUser


class Place(models.Model):
    country = models.TextField(max_length=150, blank=True)
    city = models.TextField(max_length=100, blank=True)


class MailNotifications(models.Model):
    regab = models.BooleanField(default=True)
    like = models.BooleanField(default=True)
    private_message = models.BooleanField(default=True)
    citation = models.BooleanField(default=True)


class User(AbstractUser):
    # first_name, last_name and username, password, email are already defined in AbstractUser
    avatar = models.ImageField(upload_to="avatars/", default="avatars/default.png")
    banner = models.ImageField(upload_to="banners/", blank=True)
    bio = models.TextField(max_length=300, default="I'm true member of Gabbler and it's already not bad!", blank=True)
    birthdate = models.DateTimeField(default=None, blank=True, null=True)
    place = models.ForeignKey("Place", default=None, blank=True, null=True, related_name="place")
    mail_notifications = models.OneToOneField("MailNotifications", unique=True)

    @property
    def mixed_gabs(self):
        mixed = list(self.gabs.all()) + list(self.regabs.all())
        return sorted(mixed, key=lambda i: i.date, reverse=True)

    @property
    def followers(self):
        return [relation.user for relation in self.rel_followers.all()]

    @property
    def following(self):
        return [relation.following for relation in self.rel_following.all()]


class UserLink(models.Model):
    user = models.ForeignKey("User", related_name="links")
    type = models.ForeignKey("UserLinkTypes")
    url = models.URLField()


class UserLinkTypes(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to="socialIcons/", blank=True)
