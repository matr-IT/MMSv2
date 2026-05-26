import secrets

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from users.forms import UserRegisterForm
from users.models import User

from config.settings import EMAIL_HOST_USER


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет! Перейди по ссылке для подтверждения ссылки: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('mail_management_service:index')


def password_reset_complete(request):
    return render(request, "password_reset_complete.html")

def password_reset_confirm(request):
    return render(request, "password_reset_confirm.html")

def password_reset_done(request):
    return render(request, "password_reset_done.html")

def password_reset_email(request):
    return render(request, "password_reset_email.html")

def password_reset_form(request):
    return render(request, "password_reset_form.html")

class LogoutView(LoginView):
    template_name = 'users/logout.html'
    def get_success_url(self):
        return reverse_lazy('users:login')
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.contrib.auth import logout
            logout(request)
        return super().dispatch(request, *args, **kwargs)
