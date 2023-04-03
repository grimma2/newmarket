from django.urls import path

from .views import *

# 'NAME' АТРИБУТ ОБЯЗАТЕЛЕН ДЛЯ ВСЕХ ПУТЕЙ, ДЛЯ ТОГО, ЧТОБЫ СГЕНЕРИРОВАТЬ ФАЙЛ СО ВСЕМИ ПУТЯМИ
urlpatterns = [
    # urls for states of creation product
    *map_paths('create_product/', ProductCreateTest.as_view(), name='createp'),

    path('product-detail/', GetProductDetail.as_view(), name='product_detail'),
    path('products-company/<int:company_pk>/', products_company, name='products_company'),
    path('product-to-cart/<str:slug>/', PutToCart.as_view(), name='product_to_cart'),
    path('cart/', CartDetail.as_view(), name='cart_detail'),
    path('favorites/', favorites, name='favorites'),
    path('add-product-to-favorites/', AddProductToFavorites.as_view(), name='add_product_to_favorites'),
    path('get-selected-products/', GetSelectedProducts.as_view(), name='get_selected_products'),
    path('products-ajax/', AjaxCategoryProducts.as_view(), name='ajax_products'),
    path('change-feedback/', change_feedback, name='change_feedback'),
    path('create-feedback/', create_feedback, name='create_feedback'),
    path('product-search/', SearchProducts.as_view(), name='product_search'),
    path('get_target-objects/', RecommendedView.as_view(), name='get_target_products')
]


# urlpatterns = [
#     path('product_search/', SearchProducts.as_view())
# ]

app_name = 'products'
