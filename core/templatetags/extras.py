from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter
def superurlize(value):
    return mark_safe("<a href='/%s'>%s</a>" % (value, value))