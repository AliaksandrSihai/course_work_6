from django.conf import settings
from django.core.mail import send_mail

from service.models import NewsletterMessage

def send_newsletter_to_email(newsletter: NewsletterMessage):
    """ Функция для отправки рассылки на email"""
    send_mail(
        'Рассылка',
        f'{newsletter.newsletter_name}\n({newsletter.newsletter_body})',
        settings.EMAIL_HOST_USER,
        [newsletter.to_email.contact_email]
   )



