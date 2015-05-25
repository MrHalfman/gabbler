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