from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2", "full_name", "phone_number", "country", "avatar")


class UserLoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1")

class UserUpdateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "phone_number", "country", "avatar")

class UserPasswordChangeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

class UserPasswordResetForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)

class UserPasswordResetConfirmForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

class UserDeleteForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

class UserProfileForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "phone_number", "country", "avatar")
