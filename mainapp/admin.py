from django.contrib import admin

from .models import BaseUser, UserCompany, UserCourier, UserCustomer, Feedback, Message, Chat


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'reference', 'pk')
    list_display_links = ('username', 'pk')
    prepopulated_fields = {'slug': ('username',)}


@admin.register(UserCustomer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'pk')
    list_display_links = ('pk',)


@admin.register(UserCourier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('user', 'pk')
    list_display_links = ('pk',)


@admin.register(UserCompany)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('user', 'pk')
    list_display_links = ('pk',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('text', 'rating', 'content_object', 'pk')
    list_display_links = ('pk', 'text')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'chat', 'pk')
    list_display_links = ('pk',)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('pk',)
    list_display_links = ('pk',)

