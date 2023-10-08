from django import forms

from blog.models import Blog
from client.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    """Форма для работы с блогом"""
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image')
       # exclude = ('views_count', 'publication_date')
