from django import forms
from django.core.exceptions import ValidationError

from mainapp.models import BaseUser


class UserFormMixin(forms.Form):
    username = forms.CharField()
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField()
    password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if BaseUser.objects.filter(username=username).exists():
            raise ValidationError('Company with this name already exist')

        return username
