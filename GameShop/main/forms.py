from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']

class CreateUserF(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        return self.cleaned_data.get("username")