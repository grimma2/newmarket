from django import forms


class ProductForm(forms.Form):
    in_stock = forms.IntegerField(label='в наличии товаров')
    name = forms.CharField(label='Название продукта')
    price = forms.DecimalField(label='Цена')
    description = forms.CharField()
    photo = forms.ImageField()

