from django.urls import path

from .views import *

urlpatterns = [
    # urls for states of creation product
    *map_paths('create_product/', ProductCreateTest.as_view(), name='createp'),

    path('products/<str:slug>/', ProductDetail.as_view(), name='product_detail'),
    path('products_company/<int:company_pk>/', products_company, name='products_company'),
    path('product_to_cart/<str:slug>/', PutToCart.as_view(), name='product_to_cart'),
    path('cart/', CartDetail.as_view(), name='cart_detail'),
    path('favorites/', favorites, name='favorites'),
    path('add_favorite/', add_favorite, name='add_favorite'),
    path('products/', CategoryProducts.as_view(), name='products'),
    path('products_ajax/', AjaxCategoryProducts.as_view(), name='ajax_products'),
    path('change_feedback/', change_feedback, name='change_feedback'),
    path('create_feedback/', create_feedback, name='create_feedback'),
    path('product_search/', SearchProducts.as_view(), name='product_search'),
    path('get_target_objects/', RecommendedView.as_view(), name='get_target_products')
]

'''
urlpatterns = [
    path('product_search/', SearchProducts.as_view())
]
'''
app_name = 'products'
