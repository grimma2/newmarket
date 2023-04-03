from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from mainapp.models import UserCompany, UserCustomer, UserCourier


class Cart(models.Model):
    user = models.ForeignKey(UserCustomer, on_delete=models.CASCADE)


class Category(models.Model):

    HIGH_LEVEL = 'level1'
    MIDDLE_LEVEL = 'level2'
    BOTTOM_LEVEL = 'level3'

    LEVEL_CHOICES = [
        (HIGH_LEVEL, 'высшая категория'),
        (MIDDLE_LEVEL, 'средняя категория'),
        (BOTTOM_LEVEL, 'нижния категория')
    ]

    name = models.CharField(max_length=255)
    level = models.CharField('Категория', max_length=6, choices=LEVEL_CHOICES, null=True)
    categories = models.ManyToManyField('self', symmetrical=False, related_name='categories_below', blank=True)
    slug = models.SlugField('URL', max_length=255, unique=True, null=True)

    def __str__(self):
        return f'name: {self.name}, level: {self.level}'


class Product(models.Model):
    category_set = models.ManyToManyField(Category)
    user_company = models.ForeignKey(UserCompany, on_delete=models.CASCADE, related_name='product_set')
    cart = models.ManyToManyField(Cart, blank=True)
    in_stock = models.PositiveIntegerField('В наличии товаров', default=0)
    name = models.CharField('Название продукта', max_length=399, unique=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, default=0.00)
    photo = models.ImageField('Фото продукта', upload_to='product/photos/')
    description = models.TextField('Описание продукта')
    parameters = models.JSONField(default=dict, blank=True, null=True)  # dict of additional parameters creating by user
    rating = models.DecimalField('Оценка', max_digits=3, decimal_places=2, blank=True, null=True)
    slug = models.SlugField('URL', max_length=399, unique=True)
    feedback_set = GenericRelation('mainapp.Feedback')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})


class OnOrderProduct(models.Model):

    ON_WAIT = 'status on wait'
    ON_WAY = 'status on way'

    STATUS_CHOICES = [
        (ON_WAIT, 'Товар в ожидании'),
        (ON_WAY, 'Товар уже в пути'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='on_order_product_set')
    user_customer = models.ForeignKey(UserCustomer, on_delete=models.CASCADE)
    user_courier = models.ForeignKey(UserCourier, on_delete=models.CASCADE)
    delivery_date = models.DateField('Дата доставки', null=True)
    completed = models.BooleanField('Доставлен', default=False)
    cancel = models.BooleanField('Отменён', default=False)
    status = models.CharField(
        'Статус товара в отправке', max_length=99, choices=STATUS_CHOICES, default=ON_WAIT
    )

    def __str__(self):
        return f'order product: {self.product.name}'
