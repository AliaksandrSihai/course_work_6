from django.db import models

# Create your models here.
class Client(models.Model):
    """Модель для БД таблицы с данными о клиентах"""

    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    contact_email = models.EmailField(unique=True, verbose_name='контактный email')
    feedback = models.TextField(verbose_name='комментарий')

    def __str__(self):
        return f'Клиент - {self.first_name}{self.last_name}\n' \
               f'(Эл. почта - {self.contact_email})\n' \
               f'Комментарий: {self.feedback}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
