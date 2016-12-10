from django import template
from django.core.urlresolvers import reverse, resolve

register = template.Library()


@register.simple_tag(takes_context=True)
def active(context, name, by_path=False):
    """ Return the string 'active' current request.path is same as name

    Keyword aruguments:
    context  -- Django context object
    name     -- name of the url or the actual path
    by_path  -- True if name contains a url instead of url name
    """
    if by_path:
        path = name
    else:
        path = reverse(name)

    if context['request'].path == path:
        return ' active '

    return ''
