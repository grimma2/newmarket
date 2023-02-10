from django.urls import path

from .views import *


urlpatterns = [
    path('public_courier/<str:slug>/', CourierPublicDetail.as_view(), name='public_courier'),
    path(
        'change_context_courier/<int:product_id>/',
        ChangeContextCourier.as_view(),
        name='change_context_courier'
    ),
    path('user_courier/<str:slug>/', UserCourierDetail.as_view(), name='user_courier'),
]

app_name = 'usercourier'
