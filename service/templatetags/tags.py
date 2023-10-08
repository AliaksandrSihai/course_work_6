from django import template

from client.models import Client
from service.models import NewsletterMessage, NewsletterSettings

register = template.Library()

@register.filter()
def count_newsletters(object):
    models = NewsletterMessage.objects.all()
    model_active = []
    for model in models:
        info = model.newsletter_settings
        if info is None:
            continue
        elif info.status == "Запущена":
            model_active.append(info)
    return f'Активные/Всего: {len(model_active)}/{len(models)}'

@register.filter()
def client_all(object):
    model = Client.objects.all()
    return f'Всего: {len(model)}'


@register.filter()
def start_newsletter(object):
    model = NewsletterSettings.object.get(pk=object)

@register.filter()
def settings_all(object):
    model = NewsletterSettings.objects.all()
    return f'Всего: {len(model)}'
