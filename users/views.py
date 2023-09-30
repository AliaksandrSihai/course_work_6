from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterForm, ProfileForm
from users.models import User


# Create your views here.
class UserRegisterView(CreateView):
    """Регистрация нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject='Успешная регистрация',
            message='Поздравляем с успешной регистрацией на нашей платформе!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    """Обновление профиля пользователя"""

    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
