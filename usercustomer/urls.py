from django.urls import path

from .views import *


urlpatterns = [
    path('user_customer/<str:slug>/', UserCustomerDetail.as_view(), name='user_customer'),
    path('public_customer/<str:slug>/', CustomerPublicDetail.as_view(), name='public_customer'),
    path('customer_reg/', CustomerForm.as_view(), name='customer_form'),
    path(
        'change_context_customer/<int:product_id>/',
        ChangeContextCustomer.as_view(),
        name='change_context_customer'
    ),
    path('cust/', BasePageCustomer.as_view(), name='index_customer')
]

app_name = 'usercustomer'
