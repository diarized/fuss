from django import template
import lunch.models as models

register = template.Library()

@register.filter
def vendor_name(argument):
    """Return name of the event vendor"""
    if type(argument) == models.Event:
        return argument.vendor.name

