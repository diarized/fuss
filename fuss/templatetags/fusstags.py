from django import template

register = template.Library()

@register.filter
def get_name(argument):
    """Return string evaluation of the argument"""
    return str(argument)

