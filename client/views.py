from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.models import Client


# Create your views here.
class ClientCreateView(CreateView):
    """Создание нового клиента"""

    model = Client
    fields = ['first_name', 'last_name', 'contact_email', 'feedback']
    success_url = reverse_lazy('client:client_all')


class ClientUpdateView(UpdateView):
    """Изменение/обновление уже созданного клиента"""

    model = Client
    fields = ['first_name', 'last_name', 'contact_email', 'feedback']
    success_url = reverse_lazy('client:client_all')


class ClientDeleteView(DeleteView):
    """Удаление клиента"""

    model = Client
    success_url = reverse_lazy('client:client_all')

class ClientListView(ListView):
    """Просмотр всех созданных клиентов"""

    model = Client
    extra_context = {
        'title': "Созданные клиенты",
    }

class ClientDetailView(DetailView):
    """Просмотр одного клиента"""

    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Client.objects.filter(pk=self.object.pk)
        return context