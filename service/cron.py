import datetime

from service.models import NewsletterSettings, NewsletterMessage
from service.sevices import send_newsletter_to_email


def scheduled_day():
    models = NewsletterMessage.objects.all()
    for model in models:
        if model.status == "Запущена" and model.frequency == 'Раз в день':
            send_newsletter_to_email(NewsletterMessage)



def scheduled_week():
    models = NewsletterMessage.objects.all()
    for model in models:
        if model.status == "Запущена" and model.frequency == 'Раз в неделю':
            send_newsletter_to_email(NewsletterMessage)



def scheduled_month():
    models = NewsletterMessage.objects.all()
    for model in models:
        if model.status == "Запущена" and model.frequency == 'Раз в месяц':
            send_newsletter_to_email(NewsletterMessage)


# def start():
#    time = datetime.datetime.now()
#     if model.status == "Запущена":
#         if model.frequency == 'Раз в день':
#             scheduled_day()
#         elif model.frequency == 'Раз в неделю':
#             scheduled_week()
#         else:
#             scheduled_month()
