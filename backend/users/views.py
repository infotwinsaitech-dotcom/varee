from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# ✅ DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response


# ===============================
# 🔐 LOGIN
# ===============================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# ===============================
# 🚪 LOGOUT
# ===============================
def logout_view(request):
    logout(request)
    return redirect('/login/')


# ===============================
# 🧑‍💻 DASHBOARD
# ===============================
@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')


# ===============================
# 📝 REGISTER
# ===============================
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('/register/')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('/register/')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully")
        return redirect('/login/')

    return render(request, 'register.html')


# ===============================
# 👤 PROFILE API (🔥 NEW)
# ===============================
@api_view(['GET'])
def user_profile(request):

    if request.user.is_authenticated:
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })

    return Response({
        "username": "Guest",
        "email": ""
    })