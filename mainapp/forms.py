from django import forms

from .utils.model_utils import UserChoices
from .models import BaseUser, Feedback


class SelectTypeUser(forms.Form, UserChoices):
    user_type = forms.ChoiceField(choices=UserChoices.USER_CHOICES)


class AuthForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.PasswordInput()

    def __init__(self, *args, **kwargs):
        super(AuthForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BaseUser
        fields = ('username', 'password')


class CreateFeedbackForm(forms.ModelForm):

     class Meta:
        model = Feedback
        fields = ('text', 'rating')
