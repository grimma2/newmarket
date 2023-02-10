from django.urls import path

from .views import *


urlpatterns = [
    path('add_msg/<text>/', add_message, name='add_message'),
    path('select_type_user/', SelectTypeView.as_view(), name='select_type_user'),
    path(
        'change_status/<int:product_id>/<int:option_index>/',
        ChangeProductStatus.as_view(),
        name='change_status'
    ),
    path('chats/', ChatList.as_view(), name='chats'),
    path('chat/<int:pk>/', ChatDetail.as_view(), name='chat_detail'),

    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('token/', ProjectTokenObtainPair.as_view(), name='token_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('get_auth_user/', GetAuthUser.as_view(), name='get_auth_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('get_user_refresh_token/token/', GetRefresh.as_view(), name='get_refresh'),
]

app_name = 'mainapp'
