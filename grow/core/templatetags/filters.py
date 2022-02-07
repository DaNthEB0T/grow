from django import template
import markdown as md

register = template.Library()


@register.filter(name='dict_key')
def dict_key(d, k):
    return d[k]