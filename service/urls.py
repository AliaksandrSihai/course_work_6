from django.urls import path

from service.apps import ServiceConfig
from service.views import NewsletterListView, NewsletterCreateView, \
  NewsletterDeleteView, NewsletterUpdateView, NewsletterDetailView

app_name = ServiceConfig.name


urlpatterns = [
  path('newsletter_create/', NewsletterCreateView.as_view(), name='newsletter_create'),
  path('newsletter_update/<int:pk>', NewsletterUpdateView.as_view(), name='newsletter_update'),
  path('newsletter_delete/<int:pk>', NewsletterDeleteView.as_view(), name='newsletter_delete'),
  path('newsletter_all/', NewsletterListView.as_view(), name='newsletter_all'),
  path('newsletter/<int:pk>', NewsletterDetailView.as_view(), name='newsletter'),
]
