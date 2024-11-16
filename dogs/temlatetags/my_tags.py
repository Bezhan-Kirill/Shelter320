"""
{% load %}
"""

from django import template

register = template.Library


@register.filter()
def mymedia(val):
    if val:
        return fr'/media/{val}'
    return '/static/dummydog.jpg'
