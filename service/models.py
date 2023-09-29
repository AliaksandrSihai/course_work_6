from django.db import models

import client.models
import calendar
# Create your models here.
NULLABLE = {'null': True, 'blank': True}


class NewsletterSettings(models.Model):
    """Модель для БД таблицы с данными о настройке рассылки"""

    FREQUENCY = [
        ('Раз в день', 'Раз в день'),
        ('Раз в неделю', 'Раз в неделю'),
        ('Раз в месяц', 'Раз в месяц')
    ]
    STATUS = [
        ('Запущена', 'Запущена'),
        ('Завершена', 'Завершена')
    ]
    MONTH = [(i, calendar.month_name[i]) for i in range(1, 13)]

    newsletter_month_start = models.IntegerField(choices=MONTH, verbose_name='месяц начала')
    newsletter_month_finish = models.IntegerField(choices=MONTH, verbose_name='месяц окончания')
    frequency = models.CharField(max_length=15, choices=FREQUENCY, verbose_name='периодичность')
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='статус рассылки', default='Создана',
                              **NULLABLE)

    def __str__(self):
        return f'Время рассылки c {self.newsletter_month_start} месяца до ' \
               f'{self.newsletter_month_finish} месяца,\n'\
               f'Периодичность - {self.frequency},\n' \
               f'Статус - {self.status}'

    class Meta:
        verbose_name = 'настройки рассылки'
        verbose_name_plural = 'настройки рассылок'


class NewsletterMessage(models.Model):
    """Модель для БД таблицы с данными о теме и сообщения рассылки"""

    newsletter_name = models.CharField(max_length=100, verbose_name='тема письма')
    newsletter_body = models.TextField(verbose_name='тело письма')
    newsletter_settings = models.ManyToManyField(to=NewsletterSettings, verbose_name='настройки рассылки')
    to_email = models.ManyToManyField(to=client.models.Client)

    def __str__(self):
        return (f'Тема - {self.newsletter_name}\n Email - {self.to_email}\n '
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
        return f'id рассылки - {self.newsletter_id}\n' \
               f'статус попытки - {self.attempt_status}\n' \
               f'ответ сервера - {self.server_response}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'
