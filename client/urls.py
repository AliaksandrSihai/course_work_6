from django.urls import path

from client.apps import ClientConfig
from client import views

app_name = ClientConfig.name


urlpatterns = [
  path('client_create/', views.ClientCreateView.as_view(), name='client_create'),
  path('client_update/<int:pk>', views.ClientUpdateView.as_view(), name='client_update'),
  path('client_delete/<int:pk>', views.ClientDeleteView.as_view(), name='client_delete'),
  path('client_all/', views.ClientListView.as_view(), name='client_all'),
  path('client/<int:pk>', views.ClientDetailView.as_view(), name='client'),
]
