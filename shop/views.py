from django.shortcuts import render

def index(request):
    # Контекст для головної сторінки
    context = {
        'title': 'Головна сторінка',
        'page_content': 'Вітаємо в нашому магазині одягу!',
    }
    return render(request, 'shop/index.html', context)

def catalog(request):
    # Контекст для сторінки каталогу
    context = {
        'title': 'Каталог товарів',
        'page_content': 'Тут скоро з’являться найновіші колекції.',
    }
    return render(request, 'shop/catalog.html', context)