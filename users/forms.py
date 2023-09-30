from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from client.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Форма для регистрации нового пользователя """
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class ProfileForm(StyleFormMixin, UserChangeForm):
    """Форма для профиля пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'country')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password'].widget = forms.HiddenInput()
