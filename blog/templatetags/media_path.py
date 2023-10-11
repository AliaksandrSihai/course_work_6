from django import template

register = template.Library()

@register.filter()
def to_media(val):
    """Тег пути к папке media"""
    if val:
        return f'/media/blog/{val}'
