from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import AuthenticationForm

def form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматично входить користувач після реєстрації
            return redirect('index')  # перенаправлення на головну сторінку
    else:
        form = RegisterForm()
    
    return render(request, 'form/form.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Перенаправлення на головну сторінку після успішного входу
            else:
                # Якщо аутентифікація не вдалася
                return render(request, 'form/loginForm.html', {'form': form, 'error': 'Невірне ім\'я користувача або пароль.'})
    else:
        form = AuthenticationForm()
    return render(request, 'form/loginForm.html', {'form': form})