from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Task


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user, self.cleaned_data["password"]


class AuthProfileForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class AuthorForm(ModelForm):
    class Meta:
        model = Task
        exclude = ('date', 'author', 'status', 'worker')