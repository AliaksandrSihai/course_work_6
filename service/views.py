import random

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View

from blog.models import Blog
from client.models import Client
from service.cron import newsletter
from service.forms import NewsletterMessageForm, NewsletterSettingsForm, LogsNewsletterForm
from service.models import NewsletterSettings, NewsletterMessage, LogsNewsletter
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


# Create your views here.


class MainInfoView(View):
    """Отображение главной страницы"""

    def get(self, request):
        blog = Blog.objects.all()
        context = {
            'context': random.sample(list(blog), 3),
        }
        return render(request, 'service/main.html', context)




class NewsletterCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание новой рассылки"""
    
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    permission_required = 'service.add_newslettermessage'
    success_url = reverse_lazy('service:newsletter_all')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        selected_clients_ids = self.request.POST.getlist('to_email')
        selected_clients = Client.objects.filter(pk__in=selected_clients_ids)
        self.object.save()
        for client in selected_clients:
            self.object.to_email.add(client)
            newsletter()

        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Изменение существующей рассылки"""
    
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    permission_required = 'service.change_newslettermessage'
    success_url = reverse_lazy('service:newsletter_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_all'] = Client.objects.values_list('contact_email', flat=True)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление существующей рассылки"""
    
    model = NewsletterMessage
    permission_required = 'service.delete_newslettermessage'
    success_url = reverse_lazy('service:newsletter_all')


class NewsletterListView(PermissionRequiredMixin, ListView):
    """Просмотр всех созданных рассылок"""

    model = NewsletterMessage
    permission_required = 'service.view_newslettermessage'
    extra_context = {
        'title': "Созданные рассылки",
    }

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('service:newsletter_all'))


class NewsletterDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Просмотр определённой рассылки"""

    model = NewsletterMessage
    permission_required = 'service.view.newslettermessage'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterMessage.objects.filter(pk=self.object.pk)
        return context


class NewsletterSettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание новой рассылки"""

    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    permission_required = 'service.add.newslettersettings'
    success_url = reverse_lazy('main')


class NewsletterSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Создание новой рассылки"""

    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    permission_required = 'service.change_newslettersettings'
    success_url = reverse_lazy('service:newslettersettings_list')


class NewsletterSettingListView(PermissionRequiredMixin, ListView):
    """Просмотр настроек созданных рассылок """

    model = NewsletterSettings
    permission_required = 'service.view_newslettersettings'


class NewsletterSettingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Просмотр конкретной рассылки"""

    model = NewsletterSettings
    permission_required = 'service.view_newslettersettings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterSettings.objects.filter(pk=self.object.pk)
        return context

    def post(self, request, *args, **kwargs):
        model = request.POST
        newsletter_settings = NewsletterSettings.objects.get(pk=self.kwargs['pk'])
        newsletter_settings.newsletter_month_start = model.get('newsletter_month_start')
        newsletter_settings.newsletter_month_finish = model.get('newsletter_month_finish')
        newsletter_settings.frequency = model.get('frequency')
        newsletter_settings.status = model.get('status')
        newsletter_settings.save()
        return redirect('service:newslettersettings', pk=self.kwargs['pk'])


class NewsletterSettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление настройки рассылки"""

    model = NewsletterSettings
    permission_required = 'service.delete_newslettersettings'
    success_url = reverse_lazy('service:newslettersettings_list')
