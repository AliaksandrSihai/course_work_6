from django.db import models
import client.models
from config import settings

# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class NewsletterSettings(models.Model):
    """Модель для БД таблицы с данными о настройке рассылки"""

    FREQUENCY = [
        ('Раз в день', 'Раз в день'),
        ('Раз в неделю', 'Раз в неделю'),
        ('Раз в месяц', 'Раз в месяц')
    ]

    newsletter_start = models.DateField(verbose_name='начало рассылки')
    newsletter_finish = models.DateField(verbose_name='окончание рассылки')
    frequency = models.CharField(max_length=15, choices=FREQUENCY, verbose_name='периодичность')
    status = models.CharField(max_length=20, verbose_name='статус рассылки', default='Создана',
                              **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f'Время рассылки c {self.newsletter_start}  до ' \
               f'{self.newsletter_finish};\n'\
               f'Периодичность - {self.frequency};\n'

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылок'


class NewsletterMessage(models.Model):
    """Модель для БД таблицы с данными о теме и сообщения рассылки"""

    newsletter_name = models.CharField(max_length=100, verbose_name='тема письма')
    newsletter_body = models.TextField(verbose_name='тело письма')
    newsletter_settings = models.ForeignKey(NewsletterSettings, on_delete=models.CASCADE,
                                            verbose_name='настройки рассылки')
    to_email = models.ManyToManyField(to=client.models.Client)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return (f'Тема - {self.newsletter_name};\n '
                f'Настройки рассылки:{self.newsletter_settings}')

    class Meta:
        verbose_name = 'сообщение для рассылки'
        verbose_name_plural = 'сообщения для рассылок'


class LogsNewsletter(models.Model):
    """Модель для БД таблицы с данными о логах рассылок"""

    last_attempt = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    attempt_status = models.BooleanField(default=True, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    newsletter_id = models.ForeignKey(NewsletterMessage, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.newsletter_id}\n' \
               f'Статус попытки - {self.attempt_status};\n'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'
