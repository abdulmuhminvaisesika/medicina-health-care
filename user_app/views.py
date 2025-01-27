from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserRegisterForm  # A custom form if needed

# Render the registration form and handle user creation
def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')  # Redirect to the login page
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = CustomUserRegisterForm()
    return render(request, 'user_app/register.html', {'form': form})

# Render the login page and handle user login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')  # Redirect to the home page or dashboard
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'user_app/login.html')




def home_view(request):
    return render(request, 'home.html')
