from django.contrib import admin
from service.models import NewsletterSettings, NewsletterMessage, LogsNewsletter
# Register your models here.


@admin.register(NewsletterSettings)
class NewsletterSettingsAdmin(admin.ModelAdmin):
    """Админка для работы с настройками рассылки"""

    list_display = ('pk', 'newsletter_time_start', 'newsletter_time_finish', 'frequency',
                    'status', 'to_email', )
    search_fields = ('status',)
    ordering = ('to_email',)


@admin.register(NewsletterMessage)
class NewsletterMessageAdmin(admin.ModelAdmin):
    """Админка для работы с телом рассылки"""
    list_display = ('pk', 'newsletter_name', 'newsletter_body', 'newsletter_settings',)
    search_fields = ('newsletter_name',)
    ordering = ('newsletter_settings',)


@admin.register(LogsNewsletter)
class LogsNewsletterAdmin(admin.ModelAdmin):
    """Админка для работы с логами"""
    list_display = ('pk', 'last_attempt', 'attempt_status', 'server_response', 'newsletter_id',)
    search_fields = ('newsletter_id',)
    ordering = ('newsletter_id',)
