import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from backend.cart.models import CartItem 
import requests

from backend.orders.models import Order, OrderItem


from backend.products.models import Product
from backend.orders.models import Order

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
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


# ===============================
# HOME
# ===============================
@login_required
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# ===============================
# LOGOUT
# ===============================
def logout_view(request):
    logout(request)
    return redirect('/')


# ===============================
# FORGOT PASSWORD (SEND OTP)
# ===============================
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():
            messages.error(request, "Email not found")
            return redirect('forgot_password')

        # ✅ OTP generate
        otp = str(random.randint(100000, 999999))

        # ✅ session me save
        request.session['reset_email'] = email
        request.session['otp'] = otp

        print("🔥 OTP:", otp)  # 👉 console me milega

        messages.success(request, "OTP sent (check console)")
        return redirect('verify_otp')

    return render(request, 'forgot_password.html')


# ===============================
# VERIFY OTP
# ===============================
def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if user_otp == session_otp:
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'otp.html')


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

        # session clear
        request.session.flush()

        messages.success(request, "Password updated successfully")
        return redirect('login')

    return render(request, 'reset_password.html')

def cart_page(request):
    return render(request, 'cart.html')

def orders_page(request):
    return render(request, "orders.html")

def product_detail(request, id):
    return render(request, 'product_detail.html', {'id': id})

def checkout_page(request):
    return render(request, "checkout.html")
def contact(request):
    return render(request, 'contact.html')
def dashboard(request):
    return render(request, 'dashboard.html')
def order_detail(request, id):
    return render(request, 'order_detail.html', {'order_id': id})
def order_tracking(request, id):
    try:
        order = Order.objects.get(id=id)
    except Order.DoesNotExist:
        order = None

    return render(request, 'order_tracking.html', {'order': order})


# ===============================
# PRIVACY
# ===============================
def privacy(request):
    return render(request, 'privacy.html')


# ===============================
# USER DASHBOARD
# ===============================
@login_required
def user_dashboard(request):
    return render(request, 'user_dashboard.html')


# ===============================
# PROFILE
# ===============================
@login_required
def profile(request):
    return render(request, 'profile.html')


# ===============================
# WISHLIST
# ===============================
@login_required
def wishlist(request):
    return render(request, 'wishlist.html')

def search_products(request):
    query = request.GET.get('q')

    products = []

    if query:
        products = Product.objects.filter(name__icontains=query)

    return render(request, 'search.html', {
        'products': products,
        'query': query
    })


# ===============================
# SEARCH (🔥 FIXED)
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



@login_required
def checkout(request):

    if request.method == "POST":

        address = request.POST.get("address")
        payment_method = request.POST.get("payment")

        # 🔥 GET CART ITEMS
        response = requests.get("http://127.0.0.1:8000/api/cart/", cookies=request.COOKIES)
        cart_items = response.json()

        if not cart_items:
            print("❌ CART EMPTY")
            return redirect("/cart/")

        total_price = 0

        # ✅ CREATE ORDER (ONLY ONCE)
        order = Order.objects.create(
            user=request.user,
            address=address,
            payment_method=payment_method,
            total_price=0
        )

        # ✅ CREATE ORDER ITEMS
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            price = product['price'] * quantity

            total_price += price

            OrderItem.objects.create(
                order=order,
                product_id=product['id'],
                quantity=quantity,
                price=price
            )

        # ✅ UPDATE TOTAL
        order.total_price = total_price
        order.save()

        print("✅ ORDER CREATED")

        return redirect("/orders/")

    return render(request, "checkout.html")

def terms(request):
    return render(request, 'terms.html')

def shipping(request):
    return render(request, 'shipping.html')

def sustainability(request):
    return render(request, 'sustainability.html')