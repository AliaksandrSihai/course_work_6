from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path('blog_all/', BlogListView.as_view(), name='blog_all'),
    path('blog_detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
]
