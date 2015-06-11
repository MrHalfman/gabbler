from django import template
from django.utils.safestring import mark_safe
from core.models import User
import re
register = template.Library()


@register.filter
def userlink(user):
    return mark_safe("<a href='/user/%s'>%s</a>" % (user.username, user.username))


@register.filter
def toArray(object):
    return [object]


@register.filter
def userAvatar(user):
    return mark_safe("<img src='/media/%s'/>" % user.avatar)


@register.filter
def in_regabs(user, gab):
    return user.regabs.filter(gab=gab).count() == 1


@register.filter
def is_liking(user, gab):
    return user.opinions.filter(gab=gab, like=True).count() == 1


@register.filter
def is_disliking(user, gab):
    return user.opinions.filter(gab=gab, like=False).count() == 1


@register.filter
def replace_mentions(gab_text):
    regex = re.compile('(@\w+)')
    userlist = regex.findall(gab_text)

    for uname in userlist:
        try:
            user = User.objects.get(username=uname[1:])
            gab_text = gab_text.replace(uname, "<a href='/user/%s'>%s</a>" % (user.username, uname))
        except User.DoesNotExist:
            pass

    return mark_safe(gab_text)


@register.filter
def replace_hashtags(gab_text):
    regex = re.compile('(#\w+)')
    hashtags = regex.findall(gab_text)

    for tag in hashtags:
        tag_text = tag[1:]
        gab_text = gab_text.replace(tag, "<a href='/search/%s'>%s</a>" % (tag_text, tag))

    return mark_safe(gab_text)