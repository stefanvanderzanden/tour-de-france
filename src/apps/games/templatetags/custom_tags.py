# templatetags/custom_tags.py
from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def to(start, end):
    """Usage: {% for i in 1|to:10 %} ... {% endfor %}"""
    return range(start, end + 1)