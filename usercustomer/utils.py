from django.views.generic.base import ContextMixin
from django.db.models import QuerySet

from mainapp.utils.utils import DependencyUser, check_auth
from mainapp.models import UserCustomer, UserCourier, UserCompany

from typing import Tuple, Optional

from products.models import Product, Category


class UserDetailContext(ContextMixin):

    def get_context_data(self, product_id: Optional[int] = None, **kwargs):
        check_auth(self.request)
        dependency_method = self._get_dependency_method(DependencyUser(self.request.user, self.request))
        order_products: Tuple[QuerySet, QuerySet] = dependency_method()
        context = self._get_fill_context(order_products, product_id)

        return context

    def _get_dependency_method(self, dependency: DependencyUser):
        if self.model == UserCustomer:
            return dependency.get_order_customer
        elif self.model == UserCourier:
            return dependency.get_order_courier

    @staticmethod
    def _get_fill_context(ordered: Tuple[QuerySet, QuerySet], pk: Optional[int] = None):
        context_fill = {}

        if pk:
            context_fill['first_product'] = ordered[0].get(pk=pk)
        else:
            context_fill['first_product'] = ordered[0].first()

        context_fill['order_products'] = ordered[0]
        context_fill['completed_products'] = ordered[1]

        return context_fill


class RecommendedDependency:

    def __init__(self, request):
        self.request = request

    def target_products(self):
        return Product.objects.all()[:100]

    def target_categories(self):
        return Category.objects.filter(level='level2')[:50]

    def target_brands(self):
        return UserCompany.objects.all()[:100]
