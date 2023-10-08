from django import template

register = template.Library()

@register.filter()
def to_media(val):
    if val:
        return f'/media/blog/{val}'
