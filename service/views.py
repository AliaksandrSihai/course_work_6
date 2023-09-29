from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View

from client.models import Client
from service.forms import NewsletterMessageForm, NewsletterSettingsForm, LogsNewsletterForm

from service.models import NewsletterSettings, NewsletterMessage, LogsNewsletter
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from service.sevices import send_newsletter_to_email


# Create your views here.


class MainInfoView(View):
    """Отображение главной страницы"""

    def get(self, request):
        return render(request, 'service/main.html')


class NewsletterCreateView(CreateView):
    """Создание новой рассылки"""
    
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('service:newsletter_all')

    # def get(self, request, email):
    #     model = Client.objects.all()
    #     email = []
    #     for x in model.contact_email:
    #         email.append(x)
    #     return

    def form_valid(self, form):
        obj = form.save()
        send_newsletter_to_email(obj)
        return super().form_valid(form)



class NewsletterUpdateView(UpdateView):
    """Изменение существующей рассылки"""
    
    model = NewsletterMessage
    form_class = NewsletterMessageForm
    success_url = reverse_lazy('service:newsletter_all')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_all'] = Client.objects.values_list('contact_email', flat=True)
        return context

    # def form_valid(self, form):
    #     send_to_all = self.request.POST.get('send_to_all')
    #     if send_to_all:
    #         pass
    #     return super().form_valid(form)

    def form_valid(self, form):
        obj = form.save()
        send_newsletter_to_email(obj)
        model = NewsletterMessage
        model.newsletter_settings.status = "Запущена"
        return super().form_valid(form)


class NewsletterDeleteView(DeleteView):
    """Удаление существующей рассылки"""
    
    model = NewsletterMessage
    success_url = reverse_lazy('service:newsletter_all')


class NewsletterListView(ListView):
    """Просмотр всех созданных рассылок"""

    model = NewsletterMessage
    extra_context = {
        'title': "Созданные рассылки",
    }

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('service:newsletter_all'))


class NewsletterDetailView(DetailView):
    """Просмотр определённой рассылки"""

    model = NewsletterMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterMessage.objects.filter(pk=self.object.pk)
        return context


class NewsletterSettingsCreateView(CreateView):
    """Создание новой рассылки"""

    model = NewsletterSettings
    # emails = Client.objects.all().filter('contact_email')
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('service:newsletter_create')



    # Этот метод отвечает за редирект после успешного создания объекта
    def get_success_url(self):
        return reverse('service:newsletter_create')



class NewsletterSettingsUpdateView(UpdateView):
    """Создание новой рассылки"""

    model = NewsletterSettings
    form_class = NewsletterSettingsForm
    success_url = reverse_lazy('service:newslettersettings_list')

    # def post(self, request, *args, **kwargs):
    #     model = request.POST
    #     newsletter_settings = NewsletterSettings.objects.get(pk=self.kwargs['pk'])
    #     newsletter_settings.newsletter_month_start = model.get('newsletter_month_start')
    #     newsletter_settings.newsletter_month_finish = model.get('newsletter_month_finish')
    #     newsletter_settings.frequency = model.get('frequency')
    #     newsletter_settings.status = model.get('status')
    #     newsletter_settings.save()
    #     return redirect('service:newslettersettings_list')




class NewsletterSettingListView(ListView):
    """Просмотр настроек созданных рассылок """

    model = NewsletterSettings

    # def post(self, request, *args, **kwargs):
    #     return HttpResponseRedirect(reverse('service:newslettersettings_list'))

    def post(self, request, *args, **kwargs):
        model = request.POST
        newsletter_settings = NewsletterSettings.objects.get(pk=self.kwargs['pk'])
        newsletter_settings.newsletter_month_start = model.get('newsletter_month_start')
        newsletter_settings.newsletter_month_finish = model.get('newsletter_month_finish')
        newsletter_settings.frequency = model.get('frequency')
        newsletter_settings.status = model.get('status')
        newsletter_settings.save()
        return redirect('service:newslettersettings_list')


class NewsletterSettingDetailView(DetailView):
    """Просмотр конкретной рассылки"""

    model = NewsletterSettings

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

class NewsletterSettingsDeleteView(DeleteView):
    """Удаление настройки рассылки"""

    model = NewsletterSettings
    success_url = reverse_lazy('service:newslettersettings_list')

class LogsNewsletterCreateView(CreateView):
    """"""
    model = LogsNewsletter
    form_class = LogsNewsletterForm
    success_url = reverse_lazy('service:logs')
