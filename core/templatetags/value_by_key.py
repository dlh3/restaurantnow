from django import template

register = template.Library()

@register.filter
def key(item, key):
    return item.get(key)
