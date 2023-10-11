from django import forms
from client.forms import StyleFormMixin
from service.models import NewsletterSettings, NewsletterMessage, LogsNewsletter


class NewsletterSettingsForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания модели NewsletterSettings """
    class Meta:
        model = NewsletterSettings
        fields = ['newsletter_start', 'newsletter_finish', 'frequency']
        widgets = {
            'newsletter_start': forms.SelectDateWidget(empty_label=("Выберите год", "Выберите месяц", "Выберите день")),
            'newsletter_finish': forms.SelectDateWidget(empty_label=("Выберите год", "Выберите месяц", "Выберите день")),
        }


class NewsletterMessageForm(StyleFormMixin, forms.ModelForm):
    """Форма для создания модели NewsletterMessage """
    class Meta:
        model = NewsletterMessage
        exclude = ('user',)
