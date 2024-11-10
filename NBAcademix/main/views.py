from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def landing(request):
    return render(request, 'main/landing.html')

def about(request):
    return render(request, 'main/about.html')

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "Account created successfully!")
                return redirect("login")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, 'main/signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect("admin_home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'main/login.html')

def contact(request):
    return render(request, 'main/contact.html')

@login_required
def admin_home(request):
    return render(request, "main/admin_home.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def profile(request):
    return render(request, 'main/profile.html')

def students(request):
    return render(request, 'main/students.html')
