# adminpage/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, SignupForm
from django.contrib import messages
from .models import UserProfile 
# adminpage/views.py
from django.contrib.auth.models import User  # Import User model

def landing_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, "Invalid username or password.")  # This will display error without redirecting
    else:
        form = LoginForm()
    return render(request, 'adminpage/landing_page.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # assuming password1 contains the raw password
            # Create user and save the password securely in the User model
            user = User.objects.create_user(username=username, password=password)
            # Create UserProfile and store the plain text password
            UserProfile.objects.create(user=user, password=password)
            login(request, user)
            return redirect('homepage')
    else:
        form = SignupForm()
    return render(request, 'adminpage/signup.html', {'form': form})

@login_required
def homepage(request):
    return render(request, 'adminpage/homepage.html')
@login_required
def profile(request):
    return render(request, 'adminpage/profile.html')

def logout_view(request):
    logout(request)
    return redirect('landing_page')
