

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config.settings import CACHE_ENABLED
from service.models import NewsletterMessage


def send_newsletter_to_email(newsletter: NewsletterMessage):
    """ Функция для отправки рассылки на email"""
    send_mail(
        'Рассылка',
        f'{newsletter.newsletter_name}\n({newsletter.newsletter_body})',
        settings.EMAIL_HOST_USER,
        [newsletter.to_email.contact_email]
            )


def get_blogs():
    """Низкоуровневое кеширование модели блог"""

    if CACHE_ENABLED:
        key = 'blogs'
        blogs = cache.get(key)
        if blogs is None:
            blogs = Blog.objects.all()
            cache.set(key, blogs)
    else:
        blogs = Blog.objects.all()

    return blogs
