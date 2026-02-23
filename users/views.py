from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import FormView

from config.settings import EMAIL_HOST_USER
from .forms import CustomUserCreationForm, ProfileForm
import secrets

from .models import User
class RegisterView(FormView):
    """Регистрация с подтверждением по email"""
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = '/users/login/'

    def form_valid(self, form):
        # Сохраняем пользователя, но не активируем
        user = form.save(commit=False)
        user.is_active = False
        # Генерируем токен для подтверждения
        user.token = secrets.token_urlsafe(16)
        user.save()

        # Отправляем письмо с подтверждением
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{user.token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(self.request, f'Аккаунт создан для {user.email}! Проверьте почту для подтверждения.')
        return super().form_valid(form)


def email_verification(request, token):
    """Подтверждение email по токену"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.token = None  # Очищаем токен после использования
    user.save()
    messages.success(request, 'Email успешно подтвержден! Теперь вы можете войти.')
    return redirect(reverse('users:login'))


def send_welcome_email(user_email):
    """Отправка приветственного письма"""
    subject = 'Добро пожаловать в наш сервис'
    message = 'Спасибо, что зарегистрировались в нашем сервисе!'
    from_email = EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


@login_required
def profile(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})
