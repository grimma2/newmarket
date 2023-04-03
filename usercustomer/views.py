from django.shortcuts import render
from django.views.generic import View, DetailView

from mainapp.models import UserCustomer
from mainapp.utils.utils import check_auth, ViewName, ExcludeDict, RegisterMixin
from usercustomer.forms import UserCustomerForm

from .utils import UserDetailContext, RecommendedDependency

from products.models import Product


class CustomerPublicDetail(DetailView):
    model = UserCustomer
    template_name = 'usercustomer/user_customer_public.html'
    slug_field = 'user__slug'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        check_auth(self.request)
        context = super().get_context_data(**kwargs)
        context['buy_products'] = Product.objects.filter(
            on_order_product_set__user_customer=self.object
        ).distinct()

        return context


class UserCustomerDetail(UserDetailContext, DetailView):
    model = UserCustomer
    template_name = 'usercustomer/user_customer.html'
    slug_field = 'user__slug'


class ChangeContextCustomer(UserDetailContext, View):
    model = UserCustomer

    def get(self, request, product_id):
        return render(request, 'usercustomer/user_customer.html', self.get_context_data(product_id))


class CustomerForm(RegisterMixin, View):

    @staticmethod
    def get(request):
        return render(
            request, 'usercustomer/customer_register.html', {'form': UserCustomerForm()}
        )

    def post(self, request):
        form = UserCustomerForm(
            ExcludeDict(request.POST.dict()).exclude('csrfmiddlewaretoken')
        )
        if form.is_valid():
            return self.register_user(form, UserCustomer, ViewName('usercustomer:user_customer'))
        else:
            return render(request, 'usercustomer/customer_register.html', {'form': form})


class BasePageCustomer(View):

    def get(self, request):
        recommended_dependency = RecommendedDependency(self.request)

        return render(
            request, 'usercustomer/index_customer.html',
            {
                'products': recommended_dependency.target_products(),
                'categories': recommended_dependency.target_categories(),
                'companies': recommended_dependency.target_brands()
            }
        )
