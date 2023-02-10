from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.db.models import Q
from django import forms
from django.forms import model_to_dict
from django.shortcuts import redirect
from rest_framework_simplejwt import serializers as jwt_serializers

from mainapp.models import BaseUser, UserCompany

from usercompany.forms import UserCompanyForm

from usercustomer.forms import UserCustomerForm

from products.models import OnOrderProduct

from myproject.settings import SIMPLE_JWT

from slugify import slugify


class ViewName(str):

    def __new__(cls, string: str):
        if not len(string.split(':')) == 2:
            raise Exception(f'Invalid view name: {string}')

        return super().__new__(cls, string)


class ExcludeDict(dict):

    def exclude(self, key: str):
        self.pop(key)
        return self


def check_auth(request) -> None:
    if not request.user.is_authenticated:
        raise Exception('User is not authenticated')


def check_user(request, model):
    if not isinstance(request.user.get_specific_user(), model):
        raise Exception('Haven`t user')


def filter_data(base_fields: list, form_data: dict):
    base_dict = {}
    specific_dict = {}

    for key, value in form_data.items():
        if key in base_fields:
            base_dict[key] = value
        else:
            specific_dict[key] = value

    return base_dict, specific_dict


class GetOrderProducts:

    def __init__(self, user: BaseUser, request):
        self.user = user
        self.request = request

    def get_order_customer(self):
        return (
            OnOrderProduct.objects.filter(
                user_customer__user=self.user, completed=False, cancel=False
            ),
            OnOrderProduct.objects.filter(
                Q(user_customer__user=self.user) & Q(completed=True) | Q(cancel=True)
            )
        )

    def get_order_courier(self):
        return (
            OnOrderProduct.objects.filter(
                user_courier__user=self.user, campleted=False, cancel=False
            ),
            OnOrderProduct.objects.filter(
                Q(user_courier__user=self.user) & Q(completed=True) | Q(cancel=True)
            )
        )


class DependencyUser(GetOrderProducts):

    def create_users(self, form: forms.Form, model) -> BaseUser:
        base_dict, specific_dict = filter_data(
            ['username', 'email', 'phone', 'password', 'first_name', 'last_name'], form.cleaned_data
        )
        base_dict['slug'] = slugify(base_dict['username'])
        base_dict['reference'] = self._get_user_type(form)

        base_user = BaseUser.objects.create_user(**base_dict)
        model.objects.create(**specific_dict, user=base_user)
        if model == UserCompany:
            self.company_reg(base_user)

        return base_user

    @staticmethod
    def _get_user_type(form):
        if isinstance(form, UserCompanyForm):
            return 'user company'
        elif isinstance(form, UserCustomerForm):
            return 'user customer'

    @staticmethod
    def company_reg(base_user: BaseUser) -> None:
        group = Group.objects.create(name=base_user.username)
        base_user.groups.add(group)

    def get_redirect_user(self):
        if self.user.reference == 'user company':
            return redirect('usercompany:index_company')
        elif self.user.reference == 'user customer':
            return redirect('usercustomer:index_customer')
        elif self.user.reference == 'user courier':
            return redirect('usercourier:index_courier')


class RegisterMixin:

    def register_user(self, form: forms.Form, model, viewname: ViewName):
        dependency = DependencyUser(self.request, self.request.user)
        base_user = dependency.create_users(form, model)
        login(self.request, base_user)

        return redirect(viewname, slug=base_user.slug)


class SetterAccessMixin:

    @staticmethod
    def _set_access_token(response):
        response.set_cookie(
            'access_token',
            value=response.data['access'],
            max_age=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].seconds,
            httponly=True
        )
        return response


class SetterRefreshMixin:

    @staticmethod
    def _set_refresh_token(response):
        response.set_cookie(
            'refresh_token',
            value=response.data['refresh'],
            max_age=int(SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            httponly=True
        )
        return response


class SetterAuthTokens(SetterAccessMixin, SetterRefreshMixin):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response = self._set_access_token(response)
        response = self._set_refresh_token(response)

        return response


class SetterAccessToCookie(SetterAccessMixin):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response = self._set_access_token(response)

        return response


class AddRefreshSerializer(jwt_serializers.TokenObtainPairSerializer):

    def validate(self, attrs):
        valid_data = super().validate(attrs)
        self.user.refresh = valid_data['refresh']
        self.user.save()
        valid_data['user'] = model_to_dict(self.user, exclude=['password', 'refresh', 'is_staff', 'user_permissions', 'avatar'])

        return valid_data
