from django import template
from django.conf import settings
from django.urls import reverse

from webpush.utils import get_templatetag_context

register = template.Library()


@register.filter
@register.inclusion_tag('webpush_button_custom.html', takes_context=True)
def webpush_button_custom(context):
    template_context = get_templatetag_context(context)
    return template_context
