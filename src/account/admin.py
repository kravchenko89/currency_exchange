from django.contrib import admin

from account.forms import UserCreationForm
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    model = User


# admin.site.register(User, UserAdmin)
