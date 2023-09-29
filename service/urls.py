from django.urls import path

from service.apps import ServiceConfig
from service import views

app_name = ServiceConfig.name


urlpatterns = [
  path('register_user/', views.register_user, name='register_user'),
  path('newsletter_create/', views.NewsletterCreateView.as_view(), name='newsletter_create'),
  path('newsletter_update/<int:pk>', views.NewsletterUpdateView.as_view(), name='newsletter_update'),
  path('newsletter_delete/<int:pk>', views.NewsletterDeleteView.as_view(), name='newsletter_delete'),
  path('newsletter_all/', views.NewsletterListView.as_view(), name='newsletter_all'),
  path('newsletter/<int:pk>', views.NewsletterDetailView.as_view(), name='newsletter'),
  path('newslettersettings_create/', views.NewsletterSettingsCreateView.as_view(), name='newslettersettings_create'),
  path('newslettersettings_update/<int:pk>', views.NewsletterSettingsUpdateView.as_view(), name='newslettersettings_update'),
  path('newslettersettings_list/', views.NewsletterSettingListView.as_view(), name='newslettersettings_list'),
  path('newslettersettings/<int:pk>', views.NewsletterSettingDetailView.as_view(), name='newslettersettings'),
  path('newslettersettings_delete/<int:pk>', views.NewsletterSettingsDeleteView.as_view(), name='newslettersettings_delete'),
]
