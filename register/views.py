from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login


def register(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_superuser = True
        
        
        
        messages.success(request, 'User created successfully')
        
        return redirect('login')

    return render(request, 'register.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):  # Renamed from 'login' to 'login_view'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Debug: Print the username and password to check what is being received
        print(f"Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        # Debug: Print whether the user is authenticated or not
        print(f"User authenticated: {user is not None}")

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Replace 'home' with your actual redirect URL
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')
  
            

def home_view(request):
    return render (request, 'home.html')

def delete_user(request, id):
    users = get_object_or_404(User, id = id)
    if request.method == 'POST':
        users.delete()
        return redirect('login')
    
    return render(request, 'confirm_delete.html', {'users':users})


def edit_password(request, id):
    password_reset = User.objects.get('password')
    if request.method == 'POST':
        password_reset.password = request.POST.get('password')
        password_reset.save()
        
        return redirect('login')
    
    return render(request, 'reset_password.html', {'password_reset':password_reset})

    