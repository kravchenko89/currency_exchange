from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email', 'phone', 'password', 'password_confirm')

    def clean(self):
        cleaned_data = super().clean()
        if not self.errors:
            if cleaned_data['password'] != cleaned_data['password_confirm']:
                raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.save()

        activation_code = user.activation_codes.create()
        activation_code.send_activation_code()

        # sms_code = user.sms_codes.create()
        # sms_code.send_activation_code_sms()
        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ActivateForm(forms.Form):
    sms_code = forms.CharField()
    # user_id = forms.CharField(widget=forms.HiddenInput())
