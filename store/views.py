import random
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from backend.products.models import Product
from backend.orders.models import Order, OrderItem


# ===============================
# REGISTER
# ===============================
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created! Please login")
        return redirect('login')

    return render(request, 'register.html')


# ===============================
# LOGIN
# ===============================
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


# ===============================
# LOGOUT (FIXED)
# ===============================
def logout_view(request):
    logout(request)
    return redirect('/login/')


# ===============================
# HOME
# ===============================
@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# ===============================
# SEND OTP (ONE ONLY)
# ===============================
def send_otp(request, value):
    otp = str(random.randint(100000, 999999))

    request.session['otp'] = otp
    request.session['auth_user'] = value

    print("🔥 OTP:", otp)

    return otp


# ===============================
# FORGOT PASSWORD
# ===============================
def forgot_password(request):
    if request.method == "POST":

        email = request.POST.get("email")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email not found")
            return redirect('forgot_password')

        send_otp(request, email)
        request.session['reset_email'] = email

        return redirect('/verify-otp/')

    return render(request, 'forgot_password.html')


# ===============================
# VERIFY OTP (CLEAN)
# ===============================
def verify_otp(request):

    otp_session = request.session.get("otp")

    if not otp_session:
        return redirect('/login/')

    if request.method == "POST":
        user_otp = request.POST.get("otp")

        if user_otp == otp_session:
            return redirect("/home/")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("/verify-otp/")

    return render(request, "otp.html")


# ===============================
# RESET PASSWORD
# ===============================
def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.session.get('reset_email')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        request.session.flush()

        messages.success(request, "Password updated successfully")
        return redirect('login')

    return render(request, 'reset_password.html')


# ===============================
# OTHER PAGES
# ===============================
def cart_page(request):
    return render(request, 'cart.html')


def orders_page(request):
    return render(request, "orders.html")


def product_detail(request, id):
    return render(request, 'product_detail.html', {'id': id})


def contact(request):
    return render(request, 'contact.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def privacy(request):
    return render(request, 'privacy.html')


@login_required
def user_dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')[:5]
    return render(request, 'user_dashboard.html', {'orders': orders})


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def wishlist(request):
    return render(request, 'wishlist.html')


# ===============================
# SEARCH
# ===============================
def search_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.none()

    return render(request, 'search.html', {
        'products': products,
        'query': query
    })


# ===============================
# PRODUCTS LIST
# ===============================
def product_list(request):
    products = Product.objects.all()

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'products_listing_filter.html', {
        'products': products
    })