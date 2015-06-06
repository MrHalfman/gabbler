from django.db import models


class FriendShip(models.Model):
    user1 = models.ForeignKey("core.User", related_name="user1")
    user2 = models.ForeignKey("core.User", related_name="user2")
    date = models.DateTimeField(auto_now_add=True)
    reciprocity = models.BooleanField(default=False)


class AdditionalContent(models.Model):
    video = models.URLField(blank=True, null=True)
    gif = models.CharField(max_length=250, blank=True, null=True)


class Gab(models.Model):
    user = models.ForeignKey("core.User", related_name="gabs")
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    extras = models.ForeignKey("AdditionalContent", related_name="extras", blank=True, null=True)
    reply = models.ForeignKey("Gab", related_name="replies", blank=True, null=True)

    @property
    def likes(self):
        return self.opinions.filter(like=True)

    @property
    def dislikes(self):
        return self.opinions.filter(like=False)

    class Meta:
        ordering = ['-date']


class GabOpinion(models.Model):
    user = models.ForeignKey("core.User", related_name="opinions")
    gab = models.ForeignKey("Gab", related_name="opinions")
    like = models.BooleanField(default=0)


class PrivateMessage(models.Model):
    sender = models.ForeignKey("core.User", related_name="sender")
    receiver = models.ForeignKey("core.User", related_name="receiver")
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class Regab(models.Model):
    user = models.ForeignKey("core.User", related_name="regabs")
    gab = models.ForeignKey("Gab", related_name="regabs")
    type = "regab"

    @property
    def date(self):
        return self.gab.date


class UserRelationships(models.Model):
    user = models.ForeignKey("core.User", related_name="rel_following")
    following = models.ForeignKey("core.User", related_name="rel_followers")


class Favorite(models.Model):
    user = models.ForeignKey("core.User", related_name="favorites")
    gab = models.ForeignKey("Gab", related_name="favorites")


class Notifications(models.Model):
    user = models.ForeignKey("core.User", related_name="notifications")
    text = models.CharField(max_length=200)
    link = models.URLField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class ModerationReport(models.Model):
    by = models.ForeignKey("core.User", related_name="moderation_reports")
    processed = models.BooleanField(default=False)
    gab = models.ForeignKey("Gab")
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()