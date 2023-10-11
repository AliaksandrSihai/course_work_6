import secrets
import string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
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


class ProfileView(LoginRequiredMixin, UpdateView):
    """Обновление профиля пользователя"""

    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def generate_new_password(request):
    """Генерация случайного пароля по запросу от пользователя """

    data = string.ascii_letters + string.digits + string.punctuation
    new_password = ''.join(secrets.choice(data) for i in range(12))
    request.user.set_password(new_password)
    send_mail(
        subject='Новый пароль',
        message=f'Здравствуйте, ваш новый пароль от нашего сервиса: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email],
    )
    request.user.save()
    return redirect(reverse('users:login'))


@login_required
def verification(request):
    """Верификация по почте нового пользователя """
    verification_link = secrets.token_urlsafe(34)
    request.user.verification_link = verification_link
    request.user.save()
    return verify_email(request, request.user.verification_link)


@login_required
def verify_email(request, verification_link):
    user = get_object_or_404(User, verification_link=verification_link)
    if user.verification_link == verification_link:
        user.is_verified = True
        user.verification_link = None
        send_mail(
            subject='Верификация успешно пройдена',
            message=f'Поздравляем,верификация {request.user.email} успешно пройдена',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )
    return redirect(reverse('users:profile'))
