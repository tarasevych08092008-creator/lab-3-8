from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Rating, Subscriber, Order, OrderItem


# Спеціальна форма реєстрації з обов'язковим Email
class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Електронна пошта", help_text="Необхідна для відновлення пароля")

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


def get_base_context():
    return {'categories': Category.objects.all()}


def index(request):
    context = get_base_context()
    context['products'] = Product.objects.all()[:10]
    return render(request, 'shop/index.html', context)


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    context = get_base_context()
    context['category'] = category
    context['products'] = Product.objects.filter(category=category)
    return render(request, 'shop/category.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST' and 'score' in request.POST:
        Rating.objects.create(
            product=product,
            score=int(request.POST.get('score')),
            comment=request.POST.get('comment', '')
        )
        return redirect('product_detail', product_id=product.id)

    context = get_base_context()
    context['product'] = product
    context['ratings'] = product.ratings.all().order_by('-created_at')
    return render(request, 'shop/product.html', context)


def subscribe(request):
    if request.method == 'POST' and request.POST.get('email'):
        Subscriber.objects.get_or_create(email=request.POST.get('email'))
    return redirect(request.META.get('HTTP_REFERER', 'index'))


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for p_id, quantity in cart.items():
        product = get_object_or_404(Product, id=p_id)
        cost = product.price * quantity
        total_price += cost
        cart_items.append({'product': product, 'quantity': quantity, 'cost': cost})

    context = get_base_context()
    context.update({'cart_items': cart_items, 'total_price': total_price})
    return render(request, 'shop/cart.html', context)


def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart_detail')
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address')
        )
        for p_id, quantity in cart.items():
            product = get_object_or_404(Product, id=p_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        request.session['cart'] = {}
        return render(request, 'shop/success.html', get_base_context())
    return redirect('cart_detail')


def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = ExtendedUserCreationForm()
    context = get_base_context()
    context['form'] = form
    return render(request, 'shop/register.html', context)


@login_required
def profile(request):
    context = get_base_context()
    if request.user.is_staff:
        context['orders'] = Order.objects.all().order_by('-created_at')
        context['is_admin'] = True
    else:
        context['orders'] = Order.objects.filter(user=request.user).order_by('-created_at')
        context['is_admin'] = False
    return render(request, 'shop/profile.html', context)