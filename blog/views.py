
from django.views.generic import DetailView, ListView

from blog.models import Blog
from blog.sevices import get_blogs


class BlogListView(ListView):
    """Просмотр блогов"""

    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = get_blogs()
        return context


class BlogDetailView(DetailView):
    """Детали блога"""

    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Blog.objects.filter(pk=self.object.pk)
        return context

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
