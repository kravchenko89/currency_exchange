from django.contrib import admin

from account.forms import UserCreationForm, UserChangeForm
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User


# admin.site.register(User, UserAdmin)
