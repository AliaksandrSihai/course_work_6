import random
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from blog.models import Blog
from client.models import Client
from service.cron import newsletter
from service.forms import NewsletterMessageForm, NewsletterSettingsForm
from service.models import NewsletterSettings, NewsletterMessage
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class MainInfoView(View):
    """Отображение главной страницы"""

    def get(self, request):
        blog = Blog.objects.all()
        if len(blog) > 3:
            context = {
                'context': random.sample(list(blog), 3),
            }
            return render(request, 'service/main.html', context)
        else:
            context = {
                'context': blog,
            }
            return render(request, 'service/main.html', context)


class NewsletterCreateView(LoginRequiredMixin,  CreateView):
    """Создание новой рассылки"""
    
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('service:newsletter_all')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        selected_clients_ids = self.request.POST.getlist('to_email')
        selected_clients = Client.objects.filter(pk__in=selected_clients_ids, from_user=self.request.user)
        self.object.save()
        for client in selected_clients:
            self.object.to_email.add(client)
            newsletter()
        return super().form_valid(form)


class NewsletterUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение существующей рассылки"""
    
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('service:newsletter_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_all'] = Client.objects.values_list('contact_email', flat=True)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class NewsletterDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление существующей рассылки"""
    
    model = NewsletterMessage
    success_url = reverse_lazy('service:newsletter_all')


class NewsletterListView(ListView):
    """Просмотр всех созданных рассылок"""

    model = NewsletterMessage
    extra_context = {
        'title': "Созданные рассылки",
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterMessage.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('service:newsletter_all'))


class NewsletterDetailView(LoginRequiredMixin, DetailView):
    """Просмотр определённой рассылки"""

    model = NewsletterMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterMessage.objects.filter(pk=self.object.pk, user=self.request.user)
        return context


class NewsletterSettingsCreateView(LoginRequiredMixin, CreateView):
    """Создание новой рассылки"""

    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class NewsletterSettingsUpdateView(LoginRequiredMixin, UpdateView):
    """Создание новой рассылки"""

    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('service:newslettersettings_list')


class NewsletterSettingListView(ListView):
    """Просмотр настроек созданных рассылок """

    model = NewsletterSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterSettings.objects.filter(user=self.request.user)
        return context


class NewsletterSettingDetailView(LoginRequiredMixin, DetailView):
    """Просмотр конкретной рассылки"""

    model = NewsletterSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterSettings.objects.filter(pk=self.object.pk, user=self.request.user)
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


class NewsletterSettingsDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление настройки рассылки"""

    model = NewsletterSettings
    success_url = reverse_lazy('service:newslettersettings_list')
