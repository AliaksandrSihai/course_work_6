from django import template

from client.models import Client
from service.models import NewsletterMessage, NewsletterSettings

register = template.Library()

@register.filter()
def count_newsletters(object,user):
    models = NewsletterMessage.objects.filter(user=user)
    model_active = []
    for model in models:
        info = model.newsletter_settings
        if info is None:
            continue
        elif info.status == "Запущена":
            model_active.append(info)
    return f'Активные/Всего: {len(model_active)}/{len(models)}'

@register.filter()
def client_all(object,from_user):
    model = Client.objects.filter(from_user=from_user)
    return f'Всего: {len(model)}'


@register.filter()
def start_newsletter(object):
    model = NewsletterSettings.object.get(pk=object)

@register.filter()
def settings_all(object, user):
    model = NewsletterSettings.objects.filter(user=user)
    return f'Всего: {len(model)}'
