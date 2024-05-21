

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from .models import Product, CustomUser, Cart
from .froms import ProductForm, ProductUpdateForm, CustomUserCreationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

@login_required
def list_products(request):
    products = Product.objects.all()
    return render(request, "list_products.html", {"products": products})

@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def home(request):
    return render(request, 'home.html')

@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':

        product.delete()
        return redirect('product_list')

    return render(request, 'confirm_delete_product.html', {'product': product})

@user_passes_test(lambda u: u.is_superuser)
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list page
    else:
        form = ProductUpdateForm(instance=product)
    return render(request, 'update_product.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('product_list')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the product list page after login
                return redirect('home')
            else:
                # Invalid login
                return render(request, 'registration/login.html', {'form': form, 'error_message': 'Invalid username or password.'})
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# Gestion Cart


@login_required
def add_to_cart(request, product_id, quantity=1):
    product = get_object_or_404(Product, pk=product_id)

    user = request.user

    cart_item, created = Cart.objects.get_or_create(user=user, product=product)

    if not created:
        if 'quantity' in request.POST:
            quantity = int(request.POST['quantity'])
        cart_item.quantity = int(quantity)
        cart_item.save()

    return redirect('my_cart')


@login_required
def get_cart(request):
    user = request.user

    cart_items = Cart.objects.filter(
        user=request.user).select_related('product')

    products_in_cart = [{"id": item.product.id, "name": item.product.name, "price": item.product.price,
                         "quantity": item.quantity, 'total': item.product.price*item.quantity} for item in cart_items]

    total = sum([i["price"]*i["quantity"] for i in products_in_cart])

    return render(request, 'cart.html', {'products': products_in_cart, 'total': total})


@login_required
def delete_from_cart(request, product_id):
    cart_item = get_object_or_404(
        Cart, user_id=request.user.id, product_id=product_id)

    if cart_item.user != request.user:
        return redirect('my_cart')

    cart_item.delete()

    return redirect('my_cart')
