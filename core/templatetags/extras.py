from django import template
from django.utils.safestring import mark_safe
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