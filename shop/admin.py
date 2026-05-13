from django.contrib import admin
from .models import Category, Brand, Product, Subscriber, Order, OrderItem, Rating

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'created_at', 'updated_at')

# ВІДОБРАЖЕННЯ ПІДПИСНИКІВ В АДМІНЦІ
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')

# Відображення коментарів в адмінці
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'score', 'created_at')
    list_filter = ('score', 'product')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'created_at')
    inlines = [OrderItemInline]