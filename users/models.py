from django.contrib.auth.models import AbstractUser
from django.db import models

from service.models import NULLABLE


# Create your models here.
class User(AbstractUser):
    """Модель переопределения пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    verification_link = models.CharField(max_length=50, verbose_name='ссылка для верификации', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='статус верификации')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
