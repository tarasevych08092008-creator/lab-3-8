from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def get_base_context():
    # Допоміжна функція, щоб не дублювати запит категорій для меню
    return {'categories': Category.objects.all()}


def index(request):
    context = get_base_context()
    context['products'] = Product.objects.all()[:10]  # Показуємо останні 10 товарів
    return render(request, 'shop/index.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)

    context = get_base_context()
    context['category'] = category
    context['products'] = products
    return render(request, 'shop/category.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    context = get_base_context()
    context['product'] = product
    return render(request, 'shop/product.html', context)