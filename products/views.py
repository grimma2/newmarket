from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Avg
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import View, FormView
from django.urls import path

from usercustomer.utils import RecommendedDependency
from usercustomer.serializers import ProductSerializer, CategorySerializer

import types

from rest_framework.views import APIView
from rest_framework.response import Response

from mainapp.utils.utils import check_auth
from mainapp.forms import CreateFeedbackForm, Feedback

from .models import Product, Cart, Category
from .forms import ProductForm
from .utils import (
    get_feedback_context,
    dict_to_list, ProductsQuery, SeveralQuerySetMixin, SelectedList,
    FinalCreateMixin, del_errors, TransformForm, ParseNewForm, DFFMixin
)

# НЕ НУЖНО
def map_paths(_path, view, name):
    if isinstance(view, types.FunctionType):
        view = view.view_class

    class NewAddObjectView(AddObjectView, view):
        pass

    class NewTransformFormView(TransformFormView, view):
        pass

    class NewFinalCreationView(FinalCreationView, view):
        pass

    return [
        path(_path, NewFinalCreationView.as_view(), name=name),
        path(f'{_path}add/', NewAddObjectView.as_view(), name=f'{name}_add'),
        path(f'{_path}transform/', NewTransformFormView.as_view(), name=f'{name}_transform')
    ]


class AddObjectView:

    def form_valid(self, form):
        class NewCreateForm(form.__class__):
            key = forms.CharField()
            value = forms.CharField()

        new_form = del_errors(NewCreateForm(form.cleaned_data), ['key', 'value'])

        return render(
            self.request, 'products/create_product.html', {'form': new_form}
        )


class TransformFormView(TransformForm):

    def form_valid(self, form):
        return render(
            self.request, 'products/create_product.html',
            {'form': self.transform_to_new_form(form)}
        )


class FinalCreationView(FinalCreateMixin):

    def get(self, request, *args, **kwargs):
        [self.form_class.declared_fields.pop(key) for key in self.media_files_list]
        return render(request, self.template_name, {})


class ProductCreateTest(DFFMixin):
    ''' Suposed class by user '''
    media_files_list = ['photo']
    form_class = ProductForm
    template_name = 'products/create_product.html'


class GetProductDetail(View):

    @staticmethod
    def post(request):
        product = Product.objects.get(slug=request.POST.slug)
        product_rate = product.feedback_set.aggregate(Avg('rating'))['rating__avg']

        return {'product': ProductSerializer(product).data, 'product_rate': product_rate}

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['parameters'] = dict_to_list(self.object.parameters)
    #     context['product_rate'] = self.object.feedback_set.aggregate(Avg('rating'))['rating__avg']
    #     context.update(get_feedback_context(request=self.request, obj=self.object))
    #
    #     return context


class PutToCart(View):

    @staticmethod
    def get(request, slug):
        check_auth(request)

        product = Product.objects.filter(slug=slug)
        product.first().cart.add(Cart.objects.get(user=request.user.get_specific_user()))
        product.update(in_stock=F('in_stock')-1)

        return redirect('products:cart_detail')


class CartDetail(View):

    @staticmethod
    def get(request):
        check_auth(request)
        cart = Cart.objects.filter(user=request.user.get_specific_user())
        context = {'products': cart.first().product_set.all()} if cart.exists() else {}

        return render(request, 'products/cart.html', context=context)


def products_company(request, company_pk):
    return render(request, 'products/products.html', {
        'products': Product.objects.filter(user_company=company_pk)
    })


def favorites(request):
    return render(request, 'products/products.html', {
        'products': request.user.get_specifc_user().favorites.all()
    })


class AddProductToFavorites(APIView):

    @staticmethod
    def post(self, request):
        product = Product.objects.get(slug=request.POST['slug'])
        # добвление продукта в поле 'favorites'
        request.user.get_specific_user().favorites.add(product)
        return Response({})


class GetSelectedProducts(SelectedList, SeveralQuerySetMixin, TemplateView):
    template_name = 'products/products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = ProductsQuery(query=self.request.GET.dict())
        context['category_list'] = self.get_categories_list(query)
        context['company_list'] = self.get_companies_list(query)
        context['products'] = self.get_all_queries(query)

        return context


class AjaxCategoryProducts(SeveralQuerySetMixin, View):

    def get(self, request):
        return JsonResponse({
            'data': list(self.get_all_queries(ProductsQuery(query=self.request.GET.dict())).values())
        })


def create_feedback(request):
    form = CreateFeedbackForm(request.POST)

    if form.is_valid():
        feedback = Feedback.objects.create(
            **form.cleaned_data,
            object_id=int(request.POST.dict()['object_id']),
            content_type=ContentType.objects.get(
                app_label=request.POST.dict()['app_label'],
                model=request.POST.dict()['content_type'].lower()
            ),
            user_who_put=request.user
        )

        return JsonResponse({'pk': feedback.pk, 'text': feedback.text, 'rating': feedback.rating})
    else:
        raise ValidationError(f'invalid form {form.__class__}')


def change_feedback(request):
    request_data = request.POST.dict()
    Feedback.objects.filter(
        pk=request_data['feedback_pk'],
    ).update(text=request_data['text'])

    return JsonResponse({'text': request_data['text']})


class SearchProducts(View):

    @staticmethod
    def post(request):
        products = list(Product.objects.filter(name__icontains=request.GET['input_text'])[:5].values('name', 'price', 'pk'))
        categories = list(Category.objects.filter(name__icontains=request.GET['input_text'])[:5].values('name', 'pk'))

        if not products:
            products = list(Product.objects.order_by('price')[:5].values('name', 'price', 'pk'))

        if not categories:
            categories = list(Category.objects.order_by('level')[:5].values('name', 'pk'))

        return JsonResponse({'products': products, 'categories': categories})


class RecommendedView(APIView):

    @staticmethod
    def post(request):
        recommended_dependency = RecommendedDependency(request=request)

        product_serializer = ProductSerializer(
            recommended_dependency.target_products(), many=True
        )
        category_serializer = CategorySerializer(
            recommended_dependency.target_categories(), many=True
        )

        return Response({'products': product_serializer.data, 'categories': category_serializer.data})
