from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from users import views
from users.apps import UsersConfig
from users.views import UserCreateView, email_verification

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('mail_management_service:index')), name='logout'),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path("password-reset-complete/", views.password_reset_complete, name="password_reset_complete"),
    path("password-reset-confirm/", views.password_reset_confirm, name="password_reset_confirm"),
    path("password-reset-done/", views.password_reset_done, name="password_reset_done"),
    path("password-reset-email/", views.password_reset_email, name="password_reset_email"),
    path("password-reset-form/", views.password_reset_form, name="password_reset_form")]

