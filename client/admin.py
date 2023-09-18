
from django.contrib import admin

from client.models import Client


# Register your models here.
@admin.register(Client)
class ClientAdmit(admin.ModelAdmin):
    """Админка для работы с клиентами"""

    list_display = ('pk', 'first_name', 'last_name', 'contact_email', 'feedback',)
    search_fields = ('contact_email',)
    ordering = ('first_name', 'last_name',)

