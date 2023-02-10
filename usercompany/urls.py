from django.urls import path

from .views import *


urlpatterns = [
    path('public_company/<str:slug>/', CompanyPublicDetail.as_view(), name='public_company'),
    path('admin/', AdminPanel.as_view(), name='admin'),
    path('company_reg/', CompanyForm.as_view(), name='company_form'),
    path('com/', BasePageCompany.as_view(), name='index_company'),
]

app_name = 'usercompany'
