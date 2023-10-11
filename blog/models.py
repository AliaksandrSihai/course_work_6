from django.db import models

from service.models import NULLABLE


# Create your models here.
class Blog(models.Model):
    """Модель блога"""

    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое статьи', **NULLABLE)
    image = models.ImageField(upload_to='blog/', verbose_name='изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    publication_date = models.DateTimeField(auto_created=True, verbose_name='дата публикации')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блог'
