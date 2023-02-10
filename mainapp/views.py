from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, ListView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from .models import Chat, BaseUser
from .utils.utils import AddRefreshSerializer

from products.models import OnOrderProduct

from usercustomer.utils import UserDetailContext

from .forms import SelectTypeUser


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = 'mainapp/login.html'
    success_url = reverse_lazy('base_page')


class SelectTypeView(View):

    @staticmethod
    def get(request):
        return render(request, 'mainapp/select_type_user.html', {'form': SelectTypeUser()})

    @staticmethod
    def post(request):
        form = SelectTypeUser(request.POST)
        if form.is_valid():
            data = form.cleaned_data['user_type']
            if data == 'user company':
                return redirect('usercompany:company_form')
            elif data == 'user customer':
                return redirect('usercustomer:customer_form')
            elif data == 'user courier':
                return redirect('mainapp:login')


class ChangeProductStatus(View, UserDetailContext):

    def get(self, request):
        index = request.GET.dict()['option_index']
        product_id = request.GET.dict()['product_id']
        product = OnOrderProduct.objects.filter(pk=product_id)

        if index == 2:
            messages.info(request, 'You sure what product delivered?')
            return self.get_context_data(product_id=product_id)
        else:
            product.update(status=OnOrderProduct.STATUS_CHOICES[index])
            return self.get_context_data()


def add_message(request, text):
    messages.info(request, text)
    return redirect('usercustomer:user_customer', slug=request.user.slug)


class ChatDetail(DetailView):
    model = Chat
    template_name = 'mainapp/chat.html'
    context_object_name = 'chat'


class ChatList(ListView):
    model = Chat
    template_name = 'mainapp/chats.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chats'] = self.request.user.chat_set.all()

        return context


class ProjectTokenObtainPair(TokenObtainPairView):
    serializer_class = AddRefreshSerializer


class RegisterView(APIView):

    @staticmethod
    def post(request):
        BaseUser.objects.create_user(**request.data)

        return JsonResponse(
            {'username': request.data['username'], 'password': request.data['password']}
        )


class LogoutView(APIView):

    @staticmethod
    def post(request):
        user = BaseUser.objects.get(**request.POST.dict())
        user.refresh = ''
        user.save()

        return Response(status=200)


class GetAuthUser(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        user = BaseUser.objects.get(pk=request.data['user_id'])

        return Response(
            {'user': model_to_dict(user, exclude=['password', 'refresh', 'is_staff', 'user_permissions', 'avatar'])},
            status=200
        )


class GetRefresh(APIView):

    @staticmethod
    def post(request):
        print(request.data)
        refresh = BaseUser.objects.get(pk=request.data['user_id']).refresh
        return Response({'refresh': refresh}, status=200)
