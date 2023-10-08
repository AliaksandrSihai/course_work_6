from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogDetailView, BlogListView # BlogCreateView, BlogUpdateView, BlogDeleteView,

app_name = BlogConfig.name

urlpatterns = [
    # path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    # path('blog_update/<int:pk>', BlogUpdateView.as_view(), name='blog_update'),
    # path('blog_delete/<int:pk>', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog_all/', BlogListView.as_view(), name='blog_all'),
    path('blog_detail/<int:pk>', BlogDetailView.as_view(), name='blog_detail'),
]
