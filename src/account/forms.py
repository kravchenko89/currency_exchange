from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'password')