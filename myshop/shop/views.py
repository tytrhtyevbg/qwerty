from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Product

# Представление для отображения каталога товаров
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# Представление для регистрации пользователя
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

# Представление для добавления товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1
    else:
        cart[str(product_id)] = {'quantity': 1, 'price': str(product.price)}
    request.session['cart'] = cart
    return redirect('cart_detail')

# Представление для просмотра корзины
@login_required
def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'price': item['price']
        })
        total_price += float(item['price']) * item['quantity']
    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items, 'total_price': total_price})

# Представление для удаления товара из корзины
@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')





