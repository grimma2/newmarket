from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.base import View, ContextMixin

from mainapp.models import UserCompany
from mainapp.utils.utils import RegisterMixin, ExcludeDict, ViewName, check_user

from products.models import Product, OnOrderProduct
from products.utils import get_feedback_context

from .forms import UserCompanyForm


class CompanyPublicDetail(DetailView):
    model = UserCompany
    template_name = 'usercompany/user_company_public.html'
    slug_field = 'user__slug'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        check_user(self.object, UserCompany)
        context = super().get_context_data(**kwargs)
        context.update(get_feedback_context(self.request, self.object.user))
        print(context)
        context['sell_count'] = OnOrderProduct.objects.filter(
            product__user_company=self.object, completed=True
        ).count()
        context['products_active'] = Product.objects.filter(user_company=self.object)

        return context


class AdminPanel(ContextMixin, View):

    def get(self, request):
        self.specific_user = request.user.get_specific_user()
        if isinstance(self.specific_user, UserCompany):
            return render(request, 'usercompany/admin.html', self.get_context_data(user_type=UserCompany))
        elif isinstance(self.specific_user, ...):
            return render(request, 'usercompany/admin.html', self.get_context_data(user_type=None))

    def get_context_data(self, **kwargs):
        groups = self.specific_user.user.groups.all()
        if groups.count() > 1:
            return render(self.request, 'mainapp/group_select.html')
        else:
            return {'group': groups.first()}


class CompanyForm(RegisterMixin, View):

    @staticmethod
    def get(request):
        return render(
            request, 'usercompany/company_register.html', {'form': UserCompanyForm()}
        )

    def post(self, request):
        form = UserCompanyForm(
            ExcludeDict(request.POST.dict()).exclude('csrfmiddlewaretoken')
        )
        if form.is_valid():
            return self.register_user(form, UserCompany, ViewName('usercompany:admin'))
        else:
            return render(request, 'usercompany/company_register.html', {'form': form})


class BasePageCompany(View):

    @staticmethod
    def get(request):
        return render(request, 'usercompany/index_company.html')

