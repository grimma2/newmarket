from django.contrib import admin

from .models import Product, Cart, OnOrderProduct, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'in_stock', 'price', 'photo', 'description', 'parameters', 'rating', 'pk'
    )
    list_display_links = ('pk', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = ('user',)


@admin.register(OnOrderProduct)
class OnOrderProductAdmin(admin.ModelAdmin):

    list_display = (
        'product', 'user_customer', 'user_courier', 'delivery_date', 'completed', 'cancel', 'status', 'pk'
    )
    list_display_links = (
        'product', 'user_customer', 'user_courier', 'delivery_date', 'pk'
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'pk')
    list_display_links = ('name', 'pk')
    prepopulated_fields = {'slug': ('name',)}
