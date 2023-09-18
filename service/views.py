from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from service.models import  NewsletterSettings, NewsletterMessage, LogsNewsletter
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here.


class MainInfoView(View):
    """Отображение главной страницы"""

    def get(self, request):
        return render(request, 'service/main.html')


class NewsletterCreateView(CreateView):
    """Создание новой рассылки"""
    
    model = NewsletterMessage
    fields = ('newsletter_name', 'newsletter_body', 'newsletter_settings')
    success_url = reverse_lazy('service:newsletter_all')

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_mat = form.save()
    #         new_mat.slug_name = slugify(new_mat.title)
    #         new_mat.save()
    #     return super().form_valid(form)


class NewsletterUpdateView(UpdateView):
    """Изменение существующей рассылки"""
    
    model = NewsletterMessage
    fields = ('newsletter_name', 'newsletter_body', 'newsletter_settings')
    success_url = reverse_lazy('service:newsletter_all')


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


class NewsletterDetailView(DetailView):
    """Просмотр определённой рассылки"""

    model = NewsletterMessage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = NewsletterMessage.objects.filter(pk=self.object.pk)
        return context


class NewsletterSettingsCreateView(CreateView):
    """Создание новой рассылки"""

    model = NewsletterMessage
    fields = ('newsletter_time_start', 'newsletter_time_finish', 'frequency', 'status', 'to_email')
    success_url = reverse_lazy('service:newsletter_all')

