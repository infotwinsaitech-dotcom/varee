import email
import os
import random
import requests

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from backend.cart.models import Cart

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

        if not username or not email or not password:
            messages.error(request, "All fields required")
            return redirect('register')

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        except Exception as e:
            print("🔥 ERROR:", e)
            messages.error(request, str(e))
            return redirect('register')

        return redirect('login')

    return render(request, 'register.html')


# ===============================
# LOGIN
# ===============================
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "All fields required")
            return redirect('login')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not found")
            return redirect('login')

        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, "Invalid password")
            return redirect('login')

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
from django.core.mail import send_mail
from django.conf import settings
import random
import threading
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


# ===============================
# ASYNC EMAIL FUNCTION (SAFE)
# ===============================
def send_email_async(subject, message, from_email, recipient_list):
    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=True  # ❗ crash नहीं करेगा
        )
    except Exception as e:
        print("❌ EMAIL ERROR:", e)


# ===============================
# FORGOT PASSWORD (FINAL)
# ===============================
def forgot_password(request):
    if request.method == "POST":

        email = request.POST.get("email")

        if not email:
            messages.error(request, "Email required")
            return redirect('forgot_password')

        # ✅ FIX: MultipleObjectsReturned
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "Email not found")
            return redirect('forgot_password')

        # ✅ OTP generate
        otp = str(random.randint(100000, 999999))

        request.session['otp'] = otp
        request.session['reset_email'] = email

        # 🔥 DEBUG (IMPORTANT)
        print("🔥 OTP:", otp)

        # ✅ EMAIL (background में)
        threading.Thread(
            target=send_email_async,
            args=(
                "Your OTP Code",
                f"Your OTP is {otp}",
                settings.EMAIL_HOST_USER,
                [email],
            ),
        ).start()

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
@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            return redirect('/home/')

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('/home/')

        # अगर already cart में है तो duplicate ना बने
        cart_item = Cart.objects.filter(user=request.user, product=product).first()

        if not cart_item:
            Cart.objects.create(
                user=request.user,
                product=product
            )

        return redirect('/cart/')

    return redirect('/home/')
def checkout(request):
    return render(request, 'checkout.html')