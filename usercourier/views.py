from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View

from mainapp.models import UserCourier
from mainapp.utils.utils import check_auth

from products.models import OnOrderProduct

from usercustomer.utils import UserDetailContext


class CourierPublicDetail(DetailView):
    model = UserCourier
    template_name = 'usercourier/user_courier_public.html'
    slug_field = 'user__slug'

    def get_context_data(self, **kwargs):
        check_auth(self.request)
        return {
            'user': self.object,
            'delivered_count': OnOrderProduct.objects.filter(
                user_courier=self.object, completed=True
            ).count()
        }


class UserCourierDetail(UserDetailContext, DetailView):
    model = UserCourier
    template_name = 'userdetail/user_courier.html'
    slug_field = 'user__slug'


class ChangeContextCourier(UserDetailContext, View):
    model = UserCourier

    def get(self, request, product_id):
        return render(request, 'userdetail/user_courier.html', self.get_context_data(product_id))
