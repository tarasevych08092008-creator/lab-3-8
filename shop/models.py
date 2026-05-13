from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва категорії")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва бренду")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва товару")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Фото")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(r.score for r in ratings) / ratings.count(), 1)
        return 0

    def __str__(self):
        return self.name


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    score = models.IntegerField(verbose_name="Оцінка")
    comment = models.TextField(verbose_name="Коментар", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return f"Оцінка {self.score} для {self.product.name}"


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email для розсилки")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Order(models.Model):
    # НОВЕ ПОЛЕ: Зв'язок замовлення з користувачем
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Користувач")
    full_name = models.CharField(max_length=200, verbose_name="ПІБ покупця")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адреса доставки")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата замовлення")

    def __str__(self):
        return f"Замовлення #{self.id} від {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Кількість")

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"