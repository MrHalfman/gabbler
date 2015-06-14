from django.db import models

class Gab(models.Model):
    user = models.ForeignKey("core.User", related_name="gabs")
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255)
    gif_id = models.CharField(max_length=64, blank=True, null=True, default=None)
    video = models.URLField(blank=True, null=True, default=None)
    picture = models.URLField(blank=True, null=True, default=None)

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


class Regab(models.Model):
    user = models.ForeignKey("core.User", related_name="regabs")
    gab = models.ForeignKey("Gab", related_name="regabs")
    type = "regab"
    date = models.DateTimeField(auto_now_add=True)


class UserRelationships(models.Model):
    user = models.ForeignKey("core.User", related_name="rel_following")
    following = models.ForeignKey("core.User", related_name="rel_followers")


class Notifications(models.Model):
    user = models.ForeignKey("core.User", related_name="notifications")
    text = models.CharField(max_length=200)
    link = models.URLField()
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class ModerationReport(models.Model):
    by = models.ForeignKey("core.User", related_name="moderation_reports")
    processed = models.BooleanField(default=False)
    gab = models.ForeignKey("Gab", related_name="reports")
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()