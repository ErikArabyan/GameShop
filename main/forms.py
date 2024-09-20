from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email']

class CreateUserF(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_username(self):
    #     return self.cleaned_data.get("username")
    
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['img' ,'username']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            return self.instance.username
        if len(username)<3:
            raise ValidationError('Username length should be greater than 3')
        return username

    