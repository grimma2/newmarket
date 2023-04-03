from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation, ContentType, GenericForeignKey
from django.db import models

from .utils.model_utils import UserChoices
from myproject.settings import AUTH_USER_MODEL


class BaseUser(AbstractUser):
    phone = models.CharField('Телефон', max_length=99)
    reference = models.CharField('Тип пользователя', max_length=99, choices=UserChoices.USER_CHOICES)
    avatar = models.ImageField(upload_to='user/avatar/', blank=True, null=True)
    feedback_set = GenericRelation('mainapp.Feedback')
    slug = models.SlugField('URL', unique=True, max_length=399, null=True)
    refresh = models.CharField(max_length=399, null=True, blank=True)

    def get_specific_user(self):
        if self.reference == 'user company':
            return UserCompany.objects.get(user=self)
        elif self.reference == 'user customer':
            return UserCustomer.objects.get(user=self)
        elif self.reference == 'user courier':
            return UserCourier.objects.get(user=self)


class UserCompany(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    feedback_set = GenericRelation('Feedback')

    def __str__(self):
        return str(self.user.username)


class UserCourier(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    location_link = models.URLField(max_length=499)

    def __str__(self):
        return str(self.user.username)


class UserCustomer(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True)
    favorites = models.ManyToManyField('products.Product', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)


class Feedback(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    text = models.TextField()
    rating = models.SmallIntegerField('Рейтинг от 1 до 5')
    user_who_put = models.ForeignKey(BaseUser, on_delete=models.CASCADE)


class Chat(models.Model):
    users = models.ManyToManyField(BaseUser, related_name='chat_set')


class Message(models.Model):
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
