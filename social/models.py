from django.db import models


class FriendShip(models.Model):
    user1 = models.ForeignKey("core.User", related_name="user1")
    user2 = models.ForeignKey("core.User", related_name="user2")
    date = models.DateTimeField(auto_now_add=True)
    reciprocity = models.BooleanField(default=False)


class AdditionalContent(models.Model):
    video = models.URLField()
    gif = models.CharField(max_length=250)


class Gab(models.Model):
    user = models.ForeignKey("core.User", related_name="gabs")
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    extras = models.ForeignKey("AdditionalContent", related_name="extras", blank=True, null=True)
    reply = models.ForeignKey("Gab", related_name="replies", blank=True, null=True)


class PrivateMessage(models.Model):
    sender = models.ForeignKey("core.User", related_name="sender")
    receiver = models.ForeignKey("core.User", related_name="receiver")
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class Regab(models.Model):
    user = models.ForeignKey("core.User", related_name="regabs")
    gab = models.ForeignKey("Gab", related_name="regabs")


class Favorite(models.Model):
    user = models.ForeignKey("core.User", related_name="favorites")
    gab = models.ForeignKey("Gab", related_name="favorites")


class Notifications(models.Model):
    user = models.ForeignKey("core.User", related_name="notifications")
    text = models.CharField(max_length=200)
    link = models.URLField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
