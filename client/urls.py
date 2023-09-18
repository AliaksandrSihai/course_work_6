from django.urls import path

from client.apps import ClientConfig
from client.views import ClientCreateView, ClientUpdateView, ClientDeleteView, \
  ClientListView, ClientDetailView

app_name = ClientConfig.name


urlpatterns = [
  path('client_create/', ClientCreateView.as_view(), name='client_create'),
  path('client_update/<int:pk>', ClientUpdateView.as_view(), name='client_update'),
  path('client_delete/<int:pk>', ClientDeleteView.as_view(), name='client_delete'),
  path('client_all/', ClientListView.as_view(), name='client_all'),
  path('client/<int:pk>', ClientDetailView.as_view(), name='client'),
]
