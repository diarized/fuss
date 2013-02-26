from django import template
#import sys
#import os
#parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
#sys.path.append(parent_dir)
import fuss.models as models

register = template.Library()

@register.filter
def get_name(argument):
    """Return string evaluation of the argument"""
    return str(argument)

@register.filter
def get_match_type(argument):
    """Returns s or d, depends on match type"""
    if type(argument) == models.SingleMatch:
        return 's'
    elif type(argument) == models.DoublesMatch:
        return 'd'


